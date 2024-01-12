# data_representation_project_2023

**Version 1.0.0**
***

## Description
Big Project for Data Representation Module

## A list of items in this repository in a Project Folder:
1. OneAPI Folder

*This folder includes the below files & folders:*

    - csaDAO.py file - to get the dataset from CSO website and save it as a JSON file
    - dataDAO.py file - database sql queries
    - server.py file - flask server application program
    - dbconfig.py file
    - requirements.txt
    - templates folder, which runs this application from the client perspective
        - client login page
        - client main page to perform CRUD operations
        - client failed login page

2. TwoAPIs Folder

*This folder includes a flask server application to try to run two API's together. Debugging excersice still need to be done*

3. Codes check

*This folder includes different files, which were used for creating, changing and testing codes*
***


## Instructions on running the application
1. The repository can be downloaded from my Github account: https://github.com/Anna20041983/data_representation_project_2023
2. Click the download button to save a copy of the repository on your machine.
3. In CMDER or any other command line activate the virtual environment using the below commands:
 - python -m venv venv - to create a blank virtual environment
 - .\venv\Scripts\activate.bat - to activate this environment
 - pip freeze
 - pip install flask
 - pip install flask-cors Flask requests
 - pip install mysql-connector-python
 - pip freeze > requirements.txt - create a list of requirements needed to run the application
 - cat requirements.txt - to show the above requirements
 - python server.py - to run the application in the development environment on http://127.0.0.1:5000
 - to stop the application use ctrl + C and deactivate.bat

***

## Author

Anna Kozakiewicz
***