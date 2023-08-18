from confluent_kafka import Consumer
import json
import ccloud_lib
import time
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import requests

# Kafka config
CONF = ccloud_lib.read_ccloud_config("../dags/kafka_netflix/python.config")
TOPIC = "netflix_recommendation" 
consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
consumer_conf['group.id'] = 'netflix_prediction'
consumer_conf['auto.offset.reset'] = 'latest'
consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC])



def predict(user_id):
    prediction = requests.get(f'http://localhost:4000/suggested_movies?Cust_Id={user_id}').json()
    return prediction

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            print("Waiting for message or event/error in poll()")
            continue
        elif msg.error():
            print(f'error: {msg.error()}')
        else:
            print("processing message...")
            record_key = msg.key()
            record_value = msg.value().decode('utf-8')
            print("loading json...")
            record_value_df = pd.read_json(record_value)
            print(f"received value = {record_value}")
            # process latest movies the user is currently watching
            user_curr_watching = record_value_df.copy() 
            # get user id
            user_id = user_curr_watching['customerID'][0]
           
            best_movie = pd.DataFrame(predict(user_id))
            best_movie['Cust_id'] = user_id
            print(best_movie)
            # Specify your PostgreSQL database, and credentials
            engine = create_engine('postgresql+psycopg2://ntkaybccubsmpt:c006bee3e63118363c9dbe825f8f3f5e26a62f026aec335dbfea5ebb922325fd@ec2-63-34-69-123.eu-west-1.compute.amazonaws.com:5432/dbvuj6r9nah6ju', echo = False)

            # Use pandas to_sql() function to insert the DataFrame data into the table
            # user_pred.to_sql('netflix_predictions', engine, if_exists='append', index=False)
            best_movie.to_sql('top_movies', engine, if_exists='append', index=False)

            
except KeyboardInterrupt:
    pass
finally:
    consumer.close()