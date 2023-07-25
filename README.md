### Task Manager ###
Task management web application on Django. 

[![CI](https://github.com/Dzigr/python-project-52/actions/workflows/CI.yml/badge.svg)](https://github.com/Dzigr/python-project-52/actions/workflows/CI.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/49e72fc91e2ce73b7cd3/maintainability)](https://codeclimate.com/github/Dzigr/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/49e72fc91e2ce73b7cd3/test_coverage)](https://codeclimate.com/github/Dzigr/python-project-52/test_coverage)


### Project description ###

Task Manager web-application based on the Django framework, that allows to set tasks with assign performers, change tasks statuses and labels. Authentication are required to work with the system.

The interface of the project realized with uses the Bootstrap framework and built by the DjangoTemplates backend.

[You may try demo here](https://task-manager-qnel.onrender.com)


**Stack:**
* Python
* Django
* Bootstrap
* PostgreSQL

### Local deployment ###
###### Note: Required Python & Poetry ######
1. Clone the repository
    ```comandline
    git clone git@github.com:Dzigr/python-project-52 && cd python-project-52
    ```
2. Initiate configuration with Makefile command
    ```commandline
    make setup
    ```
   This will create .env file with secret key, install required packages from pyproject.toml and migrates all models inside SQLite database


3. Run application with gunicorn web-server by
    ```commandline
    make start
    ```
    Or on local web-server in development mode
    ```commandline
    make local
    ```
