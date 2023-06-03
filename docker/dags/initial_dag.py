from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from datetime import datetime

def hello():
    print("Hello")
    
def world():
    print("world")
    
with DAG(
    'initial_dag', # Unique id of the DAG
    start_date=datetime(2022, 1, 1), # When to start executing the DAG
    description='A simple tutorial DAG', # What does the DAG do
    schedule="@daily", # when to execute DAG, its a chron expression underneath
    catchup = False # if previous missed DAGs should be triggered 
) as dag:
    
    hello_task = PythonOperator(
        task_id = "hello_task",
        python_callable = hello
    )
    
    world_task = PythonOperator(
        task_id = "word_task",
        python_callable = world
    )
        
    hello_task >> world_task