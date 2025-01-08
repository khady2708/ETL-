import os
import pandas as pd
from datetime import datetime
import requests
from flask import Flask, jsonify, request
import sqlite3 as sq
import os
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow import DAG
import requests
from datetime import datetime
import pandas as pd





def data_db():
    # extraction
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin"
    headers =  {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    data = response.json()
    dico = [key for key in data['market_data']['current_price'].keys()]
    return dico
currency =['aed','ars','aud','bch','bdt','bhd','bmd','bnb','brl','btc','cad','chf','clp','cny','czk','dkk','dot','eos','eth','eur','gbp','gel','hkd','huf','idr','ils','inr','jpy','krw','kwd','lkr','ltc','mmk','mxn','myr','ngn','nok','nzd','php','pkr','pln','rub','sar','sek','sgd','thb','try','twd','uah','usd','vef','vnd','xag','xau','xdr','xlm','xrp','yfi','zar','bits','link','sats']

    #definition des donnée dans 
    
def connecti0n(data):

    conn = sq.connect('/opt/airflow/data/cypto.db')
    cursor = conn.cursor()
        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crypto_prices (
            crypto TEXT,
            prix REAL,
            max_prix_24h REAL,
            min_prix_24h REAL,
            date TEXT
        )
                
    ''')
    cursor.execute('''
        INSERT INTO crypto_prices (crypto, prix, max_prix_24h, min_prix_24h, date)
        VALUES (?, ?, ?, ?, ?)
        ''', 
        parameters=(data['crypto'], data['prix'], data['max_prix_24h'], data['min_prix_24h'], data['date'])
        )
    
    
    conn.commit()
    conn.close()

with DAG(
    dag_id='projet_groupe',
    schedule_interval='* * * * *',  # Runs every minute
    start_date=datetime(year=2022, month=2, day=1),
    catchup=False,
    tags=['example']  # Optional: Add tags for better organization in the UI
) as dag:


    task_process_datetime = PythonOperator(
        task_id = 'push',
        python_callable= data_db,

    )

    task_process_datetime 
    
