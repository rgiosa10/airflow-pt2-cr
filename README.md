# Code Review: Airflow pt 2

#### By [Ruben Giosa](https://www.linkedin.com/in/rubengiosa/)

#### This repo showcases the creation of a DAG that uses FileSensor and XComs to check when a CSV has been uploaded to your local filesystem, then finds the flavor with the most votes.

<br>

## Technologies Used

* Airflow
* Docker
* Python
* Git
* Markdown
* `.gitignore`
* `requirements.txt`

</br>

## Description

For this project, I made a very simple DAG (`votes.py`) that a user can run on the Airflow graphical interface. It uses a file sensor to check whether the `votes.csv` file has been uploaded to the `data/` folder of this repository. 

Then it uses a `@task` that reads each row in `votes.csv`, and checks whether that value is in the `flavors_choices` list. If it is, it appends it to a new list called `valid_votes`. This task then returns the `valid_votes` list.

In another `@task`, it uses a Python function that takes a list as an argument (passes the `return_value` XCom from first task as argument), and prints the item that appear the most times in that list. Below is the XCom `return_value` from the Airflow GUI:

<img src="imgs/return_value.png" alt="return_value" width="640"/>

Below is the log of the `tally_votes_task` showing the expected output:
<img src="imgs/print_high_vote.png" alt="final output" width="640"/>


#### DAG Structure:
<img src="imgs/votes_dag.png" alt="DAG diagram" width="640"/>

<br>

## Setup/Installation Requirements

* Go to https://github.com/rgiosa10/airflow_pt2_cr.git to find the specific repository for this website.
* Then open your terminal. I recommend going to your Desktop directory:
    ```bash
    cd Desktop
    ```
* Then clone the repository by inputting: 
  ```bash
  git clone https://github.com/rgiosa10/airflow_pt2_cr.git
  ```
* Go to the new directory or open the directory folder on your desktop:
  ```bash
  cd airflow_pt2_cr
  ```
* open the directory in VS Code:
  ```bash
  code .
  ```
* Once VS Code is open, then run the setup file:
  ```bash
  ./setup.sh
  ```

    The contents of the `setup.sh` include the below to install 1) relevant version of python 2) create virtual env 3) installing Airflow in virtual env and 4) requirements.txt:
    ```bash
    #/bin/bash
    # this script will setup the environment and install all necessary components 

    # install/upgrade virtualenv
    python3.7 -m pip install --upgrade virtualenv

    # create and run a python3.7 virtual env
    python3.7 -m venv venv
    source venv/bin/activate
    # install/upgrade pip
    python3.7 -m pip install --upgrade pip setuptools wheel

    # install Airflow in the virtual env
    AIRFLOW_VERSION=2.3.2
    PYTHON_VERSION=3.7
    CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
    pip install "apache-airflow[async,postgres,google]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

    # pip install pypi packages
    pip install -r requirements.txt
    ```

* Then run the airflow setup file:

  ```bash
  ./airflow_setup.sh
  ```
    
    The contents of the `airflow_setup.sh` include the below to 1) creating ./logs and ./plugins directories in the dsa-airflow directory 2) download the `docker_compose.yaml` 3) create the .env and 4) initialize airflow
    
```bash
    #!/bin/bash
    # Move into the dsa-airflow directory and make subdirs
    cd dsa-airflow

    # download the docker-compose.yaml and set the .env
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
    echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env


    # initialize airflow 
    docker-compose up airflow-init
```

* Then go to the airflow GUI. Once there click Admin -> Connections and then create a new connection with the below config:

<img src="imgs/conn_setup.png" alt="connection setup" width="640"/>

click save

* Once setups have been completed, you will want to be using the below commands to manage airflow and docker:
    1. Once airflow has been initialized, use the below command line tool that allows you to initialize the rest of the Docker containers:
        ```bash
        docker-compose up
        ```
    2. In order to shut down hit `^Ctrl C` to stop Airflow on the local host and then run the below to stop the containers and remove old volumes:
        ```bash
        docker-compose down --volumes --remove-orphans 
        ```

</br>

## Known Bugs

* No known bugs

<br>

## License

MIT License

Copyright (c) 2022 Ruben Giosa

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

</br>