from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow import settings
from airflow.models import Connection

from datetime import datetime
  
def _create_conn():
    session = settings.Session() # get the session
    conn_id = "pokemon_db"
    
    # Check if connection with conn_id already exists
    existing_conn = session.query(Connection).filter(Connection.conn_id == conn_id).first()
    
    if existing_conn is None:
        # Create a new connection object
        conn = Connection(
            conn_id=conn_id,
            conn_type="postgres",
            host="postgres",
            login="airflow",
            password="airflow",
            port="5432"
        )
        
        # Add and commit the new connection object
        session.add(conn)
        session.commit()

def _store_pokemon():
    hook = PostgresHook(postgres_conn_id='pokemon_db')
    hook.copy_expert(
        sql="COPY PokeData FROM stdin WITH DELIMITER as ','",
        filename='/Data/Pokemon.csv'
    )
    
def _drop_duplicates():
    # Create a PostgresHook using the predefined connection
    hook = PostgresHook(postgres_conn_id='pokemon_db')
    
    # Execute the SQL query to drop duplicates
    query = "DELETE FROM PokeData WHERE ctid NOT IN (SELECT min(ctid) FROM PokeData GROUP BY id);"
    hook.run(query)

with DAG('pokemon_processing', start_date=datetime(2022, 1, 1), 
        schedule_interval='@daily', catchup=False) as dag:
    
    create_conn = PythonOperator(
        task_id='create_connection',
        python_callable=_create_conn
    )
    
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='pokemon_db',
        sql='''
            CREATE TABLE IF NOT EXISTS PokeData (
                ID TEXT NOT NULL,
                Name TEXT NOT NULL,
                Type_1 TEXT NOT NULL,
                Type_2 TEXT NULL,
                Total TEXT NOT NULL,
                Hit_Points TEXT NOT NULL,
                Attack TEXT NOT NULL,
                Defense TEXT NOT NULL,
                Special_Attack TEXT NOT NULL,
                Special_Defense TEXT NOT NULL,
                Speed TEXT NOT NULL,
                Generation TEXT NOT NULL,
                Legendary TEXT NOT NULL
            );
        '''
    )
    
    store_pokemon = PythonOperator(
        task_id='store_pokemon',
        python_callable=_store_pokemon
    )
    
    remove_duplicates = PythonOperator(
        task_id='remove_duplicates',
        python_callable=_drop_duplicates
    )
    
    create_conn >> create_table >> store_pokemon >> remove_duplicates