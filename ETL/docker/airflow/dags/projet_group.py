import requests
import pandas as pd
from datetime import datetime
import sqlite3
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor



def get_currency():

    url_curr = f"https://api.coingecko.com/api/v3/coins/bitcoin"

    headers = {"accept": "application/json"}

    rep_curr = requests.get(url_curr, headers=headers)

    req_curr = rep_curr.json()

    dico = [key for key in req_curr['market_data']['current_price'].keys()]

    return dico

currency =['aed','ars','aud','bch','bdt','bhd','bmd','bnb','brl','btc','cad','chf','clp','cny','czk','dkk','dot','eos','eth','eur','gbp','gel','hkd','huf','idr','ils','inr','jpy','krw','kwd','lkr','ltc','mmk','mxn','myr','ngn','nok','nzd','php','pkr','pln','rub','sar','sek','sgd','thb','try','twd','uah','usd','vef','vnd','xag','xau','xdr','xlm','xrp','yfi','zar','bits','link','sats']


def get_price():

    current_price, nom_crypto, max_24h, min_24h, date, currency = [], [], [], [], [], []

    liste_coins = ['bitcoin', 'ethereum', 'cardano', 'solana']



    for coin in liste_coins:

        for curr in get_currency():



            url = f"https://api.coingecko.com/api/v3/coins/markets?ids={coin}&vs_currency={curr}&x_cg_demo_api_key=CG-3quhvTg3SdhM5LCo7ZAf1zkG"

            headers = {"accept": "application/json"}

            rep = requests.get(url, headers=headers)

            if rep.status_code == 200 and rep.content:

                req = rep.json()

                if req:

                    current_price.append(req[0]['current_price'])

                    nom_crypto.append(req[0]['id'])

                    max_24h.append(req[0]['high_24h'])

                    min_24h.append(req[0]['low_24h'])

                    date.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                    currency.append(curr)

                else:

                    continue

            else:

                continue



    df_coin = pd.DataFrame({

        'date' : date,

        'nom_crypto' : nom_crypto,

        'currency' : currency,

        'current_price' : current_price,

        'max_24h' : max_24h,

        'min_24h' : min_24h

    })



    return df_coin



def push_sql():

    conn = sqlite3.connect('/opt/airflow/data/coins.db')

    df = get_price()

    df.to_sql(name='price', con=conn, if_exists='append', index=False)

    conn.close()





with DAG(

    dag_id = 'projet_group',

    schedule = '*/10 * * * *',

    start_date = datetime(24,11,7),

    catchup=False,

) as dag:
      # 1. Get current datetime
    task_get_datetime = BashOperator(
        task_id='get_datetime',
        bash_command='date',
        do_xcom_push=True  # Push the output to XCom
    )



    task_process_datetime = PythonOperator(

        task_id = 'push',

        python_callable=push_sql

    )

task_get_datetime >> task_process_datetime 

