import os
import pandas as pd
from datetime import datetime
from fuzzywuzzy import fuzz
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor  

# Function to save the datetime to a CSV file
#EXtrére  la base dedonnée

def read_csv():
    df = pd.read_csv('data/point_apports_poubelles.csv')
    volume_total_par_type = df.groupby(["commune","type_conteneur"])["volume_m3"].sum().reset_index()
    nombre_par_type = df[["commune","type_conteneur"]].value_counts().reset_index()
    donne = pd.merge(volume_total_par_type, nombre_par_type ,on=["commune","type_conteneur"])
    donne.columns= ['commune','type_poubelle', 'volume_total_par_type', 'nombre_par_type']

    population_par_per= pd.read_csv('data/population_per_commune.csv')
    df = pd.merge(donne,population_par_per,on=["commune"])
    df['nombre_total_type'] = df.groupby('commune')['nombre_par_type'].transform('sum')
    df['pop_per_poub'] = ((df['population']*df['nombre_par_type'])/ df['nombre_total_type'])
    poubelles = df.drop(['nombre_total_type'], axis=1)


# Define the DAG
with DAG(
    dag_id='Projet_poubelle',
    schedule_interval='* * * * *',  # Runs every minute
    start_date=datetime(year=2022, month=2, day=1),
    catchup=False,
    tags=['example']  # Optional: Add tags for better organization in the UI
) as dag:
    
      
    # 3. File Sensor 
    wait_for_file = FileSensor(
        task_id='file_sensor',
        filepath='point_apports_poubelles.csv', 
        fs_conn_id='fs_default', 
        poke_interval=5,  
        timeout=600,  
    )
    
    
    # 1. Get current datetime
    task_get_datetime = BashOperator(
        task_id='get_datetime',
        bash_command='date',
        do_xcom_push=True  # Push the output to XCom
    )
    
    # 2. Save datetime to CSV
    task_process_datetime = PythonOperator(
        task_id='read_csv',
        python_callable=read_csv,
    )
    
    # Define task dependencies
    wait_for_file >> task_get_datetime >> task_process_datetime 
