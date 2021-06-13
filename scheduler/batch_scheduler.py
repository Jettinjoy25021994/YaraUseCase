"""
A scheduler that periodically fethes the CircleCI config.yml

Createe By: Jettin Joy
Created on: 06/12/2021
"""

import asyncio
import base64
import os
import json
import requests
import yaml
import aiohttp
import schedule
from github import Github
from github.GithubException import BadCredentialsException
from requests.exceptions import ConnectionError



class ScheduleGitOps:
    """
    A scheduler that periodically fetches CircleCI config file
    """
    def __init__(self):
        """Initialze the scheduler class"""
        self.all_conf_contents = []
        self.org_name = self._get_org_name()
        self.org_cred = os.environ.get(self.org_name, '')
        self.enterprise_host = os.environ.get('GITHOSTNAME', '')
        self.g_info = self._get_github_info()
        self.repos = self._get_repositories()
        self.all_repo_conf = self.retrieve_all_repo_conf()
        self.mand_steps = self._get_all_mand_steps()

    def _get_org_name(self):
        """
        Read the oraganization name for which the config
        file should be retrived for the repos
        Parameters: None
        Returns:
            repositories (list): a list of public repos in the org
        """
        org_name = ''
        try:
            with open("organization.yml", 'r') as org_file:
                org_details_json = yaml.load(org_file)
                org_name = org_details_json.get('githubOrganization')[0]
        except (KeyError, FileNotFoundError, IndexError) as e_rr:
            print(str(e_rr))
        return org_name

    def _get_github_info(self):
        """Get github details"""
        g_info = ''
        try:
            if self.enterprise_host and self.org_cred:
                url = f"https://{self.enterprise_host}/api/v3"
                g_info = Github(base_url=url, login_or_token=self.org_cred)
            elif self.org_cred:
                g_info = Github(self.org_cred)
        except  (BadCredentialsException, ConnectionError):
            pass
        return g_info

    def _get_repositories(self):
        """
        Get all the repositories for the organization
        Parameters: None
        Returns:
            repo_names (list): a list of public repo names
        """
        repos = list()
        try:
            repos = [repo.name for repo in
                        self.g_info.get_user().get_repos()]
        except (AttributeError, KeyError) as e_rr:
            print(str(e_rr))
            repos = list()
        return repos

    def retrieve_all_repo_conf(self):
        """Retrieve all the repo which has status pending, 
            not outdated and not verified
        """
        all_repo_conf_details = []
        try:
            api_url = 'http://backend:5000/retrieve/all'
            response = requests.get(api_url)
            all_repo_conf_details = response.json().get('All Repo details', [])
        except (AttributeError, KeyError, ConnectionError) as e_rr:
            print(str(e_rr))
        return all_repo_conf_details

    def _get_all_mand_steps(self):
        """Get the mandatory steps for checking"""
        steps = []
        try:
            url = 'http://backend:5000/getsteps'
            response = requests.get(url)
            steps = response.json().get('MandSteps')
        except (AttributeError, KeyError, ConnectionError) as e_rr:
            print(str(e_rr))
        return steps

    def is_complaint(self, conf):
        """
        checks whether the repo is complaint or not
        """
        status = "PENDING"
        if not self.mand_steps:
            return status
        if not conf:
            status = "NON-COMPLAINT"
        for step in self.mand_steps:
            if step not in conf.get('jobs', {}):
                status = "NON-COMPLAINT"
                return status
        status = "COMPLAINT"
        return status

    def get_report(self):
        """Get the report for all the repo"""
        report = []
        url = 'http://backend:5000/report'
        try:
            response = requests.get(url)
            report = response.json()
        except (AttributeError, KeyError, ConnectionError) as e_rr:
            print(str(e_rr))
        return report
     
    async def get_config_data(self):
            """Get the configuration data for CircleCI pipeline"""
            async with aiohttp.ClientSession() as session:
                tasks = []
                for repo in self.repos:
                    task = asyncio.ensure_future(self.get_and_post_conf_file_data(repo, session))
                    tasks.append(task)
                await asyncio.gather(*tasks)
    
    async def get_and_post_conf_file_data(self, repo, session):
            """Get the config cile content"""
            conf_content = {}
            headers = {'Authorization': self.org_cred}
            url = f"https://api.github.com/repos/{self.org_name}/{repo}/contents/.circleci/config.yml"
            async with session.get(url, headers=headers) as response:
                try:
                    result_data = await response.json()
                    content = result_data.get('content')
                    encoded_content = base64.b64decode(content)
                    content_data = encoded_content.decode()
                except (AttributeError, KeyError, TypeError) as e_rr:
                   content_data = {}
            api_url = 'http://backend:5000/create'
            post_data = {
                "organization": self.org_name,
                "repository": repo,
                "config": yaml.load(content_data) if content_data else {},
                "user": "user"
            }
            async with session.post(api_url, json = post_data) as request:
                try:
                    print(request.status)
                except AttributeError as e_rr:
                    print(str(e_rr))

    async def analyze_repo_conf(self):
           """
           For all the repos update the status as complaint / non-complaint
           """
           async with aiohttp.ClientSession() as session:
                tasks = []
                for repo_conf in self.all_repo_conf:
                    task = asyncio.ensure_future(self.set_repo_conf_status(repo_conf.get('repository', ''),
                                                                                repo_conf.get('conf',{}),
                                                                                session))
                    tasks.append(task)
                await asyncio.gather(*tasks)

    async def set_repo_conf_status(self, repo, repo_conf, session):
            """Get the config cile content"""
            conf_content = {}
            complaint_status = self.is_complaint(repo_conf)
            print('status',complaint_status)
            api_url = f'http://backend:5000/statupdate/{repo}'
            headers = {'Content-Type': 'application/json'}
            patch_data = json.dumps({"Status": complaint_status, 'user': "user"}).encode('utf-8')
            async with session.patch(api_url, data = patch_data, headers=headers) as request:
                status = await request.json()
                print(status)


def main():
    s = ScheduleGitOps()
    asyncio.run(s.get_config_data())
    asyncio.run(s.analyze_repo_conf())
    print(s.get_report())

schedule_interval = int(os.environ.get('INTERVAL',900))
schedule.every(schedule_interval).seconds.do(main)
while True:
   schedule.run_pending()