#!/bing/bash

cd dsa-airflow

# set the .env
curl -Lf 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml' > docker-compose.yaml
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

# NOTE: Run the airflow-init before running `docker-compose up`:
docker-compose up airflow-init