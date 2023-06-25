# PokemonFlow

This is a personal project for testing out Airflow.

## Setup
Clone the project and navigate under Docker folder. Create launch docker instances with docker compose (see bellow).
```
docker-compose up -d 
```
In theory, that is it. You can visit http://localhost:1996 and see Airflow up and running. Default login credentials are airflow/airflow.

## Explanation
### Data
By default, data should be cloned into Data folder. Data originates from [Kaggle](https://www.kaggle.com/datasets/abcsds/pokemon). If you change the data, look at the create_table and _store_pokemon DAGs.

### Docker
All of the Docker items are kept under Docker folder. Compose file originates from official [Airflow example](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).
Container airflow-init-1 will stop after some time. This is normal, container is only used for setup. 
You can access PostgreSQL with DBever. After DAGs are executed, Databases -> Airflow -> Schemas -> Public -> Tables and PokeData table should be there.
<p align="center">
  <img src="https://raw.githubusercontent.com/ZanZver/PokemonFlow/main/Img/DBever.jpg" />
</p>

### DAGs
Folder DAGs contains instructions on what to execute. At the moment, there is only one DAG (big_dag.py), but there could be more. Tasks of the DAG can be seen bellow.
<p align="center">
  <img src="https://raw.githubusercontent.com/ZanZver/PokemonFlow/main/Img/Steps.gif" />
</p>