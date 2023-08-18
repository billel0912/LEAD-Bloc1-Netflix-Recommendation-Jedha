from datetime import datetime
import json
import pandas as pd
import requests
from airflow import DAG
from airflow.operators.bash_operator import BashOperator


default_args = {
    "owner": "airflow",
}

dag = DAG(
    dag_id='daily_dag',
    start_date=datetime(2023, 8, 15),
    schedule_interval=None
)

with dag:

    run_start = BashOperator(
        task_id='run_start',
        bash_command="echo 'START'",
        cwd=dag.folder
    )
    

    
    run_all = BashOperator(
        task_id='run_all',
        bash_command='python3 ../dags/FASTAPI/app.py & sleep 500 && (python3 ../dags/kafka_netflix/producer.py & python3 ../dags/kafka_netflix/consumer.py)',
        trigger_rule= 'always',
        cwd=dag.folder
    )
    

    
    run_end = BashOperator(
        task_id='run_end',
        bash_command="echo 'end'",
        cwd=dag.folder
    )

    
    
    run_start >> run_all >> run_end
   