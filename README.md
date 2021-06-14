Endpoints:



GET / : Checks whether the API is Up and Running


POST /create : to create a pipeline step



    payload = {
        "organization": "Name of org",
        "repository": "repo name",
        "config": dict() # pipeline step as dict,
        "user": "user who creates this"
    }



GET /retrieve/all: Get all the pipeline steps which for which  report is not generated


GET /retrieve/{repo}: Get pipeline steps for a repo for which report is not generated


PUT /update/{repo}: Update the pipeline step with new data


    payload = {
        "conf": dict() # new pipeline to be updated with,
        "user": "user who updates this"
    }



DELETE /delete/{repo}: Delete the details for a repo


PATCH /patch/{repo}: Updates the status of (COMPLAINT/NON-COMPLAINT)
    
    
    payload = {
        "Status": "Status to be updated with",
        "user": "User who updates it"
    }


POST /steps: A list of Steps that we can check if they are present in the pipeline or not


GET /getsteps: Retrieves the latest steps which has to verified


GET /report: Gets the latest report containing status of each repo



Notes:



Steps for running locally:



1) Clone the repo


2) Keep your organization name in the organization.yml  under scheduler directory sfile in the specified format



3)Keep all the env variables in .env file. env varibales and description
    
    
    -   POSTGRES_DB=postgres
    -   POSTGRES_USER=postgres
    -   POSTGRES_PASSWORD=postgres
    -   DB_SERVICE=db
    -   DB_PORT=5432
    -   your_org_name_specified_in_yml_file=your_git_secret
    -   GITHOSTNAME='' # set it to your if you have a enterprise version of the github
    -   INTERVAL=900 # Scheduler interval if not set defaults to 900s



4) docker-compose up --build



5) check http://localhost:8001 to see if service is running



NB: To generate report do a post request to  /steps with all the mandatory pipeline steps to be checked


    To check the report hit /report with get request



Assumptions: Assumes that All the pipeline steps to be checked are under 'jobs' section of the circleci yml file



Future Enhancement:

1) Auto commit the updated changes in pipeline steps with scripts


2) Remove inconsistencies in report


3) Automate emailing of the report
