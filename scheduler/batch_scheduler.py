"""
A scheduler that periodically fethes the CircleCI config.yml

Createe By: Jettin Joy
Created on: 06/12/2021
"""

import asyncio
import base64
import os
import requests
from requests.api import post
import yaml
import aiohttp
import schedule
from github import Github
from github.GithubException import BadCredentialsException
from requests.exceptions import ConnectionError



class ScheduleGitOps:
    """
    A scheduler that periodically fetches CircleCI config file
    Attriutes:
        period (int): schedule task every "period"
    """
    def __init__(self, period):
        """Initialze the scheduler class"""
        self.period = period
        self.all_conf_contents = []
        self.org_name = self._get_org_name()
        self.org_cred = os.environ.get(self.org_name, '') or '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'
        self.enterprise_host = os.environ.get('GITHOSTNAME', '')
        self.g_info = self._get_github_info()
        self.repos = self._get_repositories()

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
            url = f"https://api.github.com/repos/{self.org_name}/{repo}/contents/.env"
            print(url)
            async with session.get(url, headers=headers) as response:
                try:
                    print("status", response.status)
                    result_data = await response.json()
                    content = result_data.get('content')
                    encoded_content = base64.b64decode(content)
                    content_data = encoded_content.decode()
                    print("content", content_data)
                except (AttributeError, KeyError, TypeError) as e_rr:
                   content_data = {}
            #return content_data
            api_url = 'http://backend:5000/create'
            post_data = {
                "organization": self.org_name,
                "repository": repo,
                "config": content_data,
                "user": "user"
            }
            if post_data.get('config',{}):
                async with session.post(api_url, json = post_data) as request:
                    print(request.status)


def main():
    s = ScheduleGitOps(1)
    asyncio.run(s.get_config_data())
schedule.every(5).seconds.do(main)
while True:
   schedule.run_pending()