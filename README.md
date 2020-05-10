# Requirements 
* Install [Docker](https://www.docker.com/products/docker-desktop)
* Install [Docker Compose](https://docs.docker.com/compose/install/)
* Download the [Kaggle Instacart eCommerce dataset](https://www.kaggle.com/c/instacart-market-basket-analysis/data) 

# Setup
* Clone the repository
* Extract the CSV files within ./sample_data directory

# Initialisation
Change directory within the repository and run `docker-compose up`. This will perform the following:
* Based on the definition of `docker-compose.yml` will download the necessary images to run the project. This includes a Postgres DB for Airflow to connect, Adminer (a lightweight DB client). Finally a Python 3.7-based image to host Airflow.
* 3 containers in total will be build and all necessary files will load.
* Within the Postgres service, all the CSV files will be loaded (this will take 2-3 minutes depending on your hardware).

# Connections
* Adminer UI: http://localhost:8080
* Airflow UI: http://localhost:8000

# Docker Compose Commands
* Enable the services: `docker-compose up` or `docker-compose up -d` (detatches the terminal from the services' log)
* Disable the services: `docker-compose down` Non-destructive operation.
* Delete the services: `docker-compose rm` Ddeletes all associated data. The database will be empty on next run.
* Delete the services: `docker-compose build` Re-builds the containers based on the docker-compose.yml definition. Since only the Airflow service is based on local files, this is the only image that is re-build (useful if you apply changes on the `./scripts_airflow/init.sh` file. 