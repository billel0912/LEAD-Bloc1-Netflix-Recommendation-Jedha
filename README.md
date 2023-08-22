# LEAD-Bloc1-Netflix-Recommendation-Jedha
## ![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/f17d64a9-3922-4cee-87dc-9b881085659c) Netflix-recommendation-engine ![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/f17d64a9-3922-4cee-87dc-9b881085659c)
![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/2f002cd8-a41b-4e93-a357-b8eba4d86e69)

This Repository (located in Github) / Word file (located in Google Drive), contains all resources related to the project presentation on the Netflix recommendation engine.

## All resources:

The slide deck for the presentation can be accessed in the file named Présentation_Certification_Bloc _1_Netflix_reco_en.pptx. 
Additional resources, including the model and training data, are located at this link: https://drive.google.com/drive/folders/14qz8C2JKb7AuaLz6VbQjgEoHbhNFNw5S?usp=drive_link. 
The project’s topic can be found here: https://app.jedha.co/course/final-projects-l/netflix-automation-engine-l. A description of the contents and objectives of each folder in this repository is provided below.
If you have any questions or need more information about this project, please don’t hesitate to contact the repository owner on GitHub: billel0912 (billel_abbas@yahoo.fr).

## ![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/54ed3921-f6f6-4603-92b7-89904323f64d) Folder Preprocessing and Model training: ![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/3b255f3b-1bc7-4eb1-9c02-512b41a4839b)

This directory, named Preprocessing_Netflix, contains a script called data_preprocessing.ipynb. This script performs data integration from Kaggle and constructs the training dataset for the recommendation model. 
The data folder holds the raw data, which was sourced from https://www.kaggle.com/code/laowingkin/netflix-movie-recommendation
In addition, this directory also includes information related to model training. The model folder contains a serialized version of the trained recommendation model, stored as a pickle file named “model.pkl”. This model is used to generate movie predictions.
The output files, data_cleaned.csv and data_reco.csv, model.pkl which contain the preprocessed, cleaned data and model training are available on Google Drive.

## Folder Airflow![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/9679373f-f151-4117-9696-7a712769d2e4), Kafka![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/8a330337-5048-4ce4-9e7b-7e24e0362887) and FASTAPI![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/92dbeb3f-bb06-442a-81f9-e661b7754ada):
In folder “**Project_Final_Kafka**”, we find:

**airflow.cfg**: is a configuration file for Apache Airflow, a platform for creating, scheduling, and monitoring workflows. It contains Airflow’s settings and can be edited to change them.
**airflow.db**: is the database used by Airflow to manage its DAGs and tasks. This file is in SQLite3 format and can be used throughout development, but it is strongly recommended to switch to another type (such as PostgreSQL or MySQL) when moving to production.
**dags**: this folder in Airflow is the directory where your Airflow pipelines, or DAGs (Directed Acyclic Graphs), are stored1. The location of this folder is specified in the airflow.cfg file, which is located in your $AIRFLOW_HOME directory2. You can find the path to the dags folder by checking the dags_folder parameter in the airflow.cfg file.
In this **folder dags**, we find: 
1. **Script “dag.py”**:  is a Python script that defines a Directed Acyclic Graph (DAG) in Apache Airflow, a platform for programmatically authoring, scheduling, and monitoring workflows. A DAG is the core concept of Airflow and collects tasks together, organized with dependencies and relationships to specify how they should run. In this script, three tasks are defined: run_start, run_all, and run_end. The most important task is run_all, which should launch three scripts: app.py (FastAPI), producer.py, and consumer.py. These scripts are launched using a Bash command in the bash_command parameter of the BashOperator. The tasks are organized in a sequence using the >> operator, so that run_start is executed first, followed by run_all, and finally run_end.

2. **Folder “FASTAPI”**:  In the FASTAPI folder, you have the app.py script, the data folder containing the data_reco file, and the model folder containing the prediction model model.pkl. The app.py script is a FastAPI application that provides an API for making movie recommendations for a given user. The API has two endpoints: /, which returns a simple “Hello world!” message, and /suggested_movies, which returns the top 10 suggested movies for a given user ID. The model used for making predictions is loaded using the joblib library and the predictions are made by applying the model’s predict method to the movie IDs in the data_reco.csv file.
3. **Folder ‘kafka_netflix”**: we find in this folder:
   
**ccloud_lib.py**: is a Python script that provides helper functions for interacting with Confluent Cloud, a fully managed Apache Kafka service. The script includes classes for defining Avro schemas and records, as well as functions for parsing command line arguments, reading Confluent Cloud configuration files, and creating Kafka topics.

**python.config**: is a configuration file that is used to store settings for a Python application that interacts with Confluent Cloud, a fully managed Apache Kafka service. The file contains the required connection configurations for Kafka producer, consumer, and admin, as well as the required connection configurations for Confluent Cloud Schema Registry. The settings include the bootstrap servers, security protocol, SASL mechanisms, SASL username and password, session timeout, schema registry URL, and basic authentication credentials.

**Script “producer.py** “: This script is a Kafka producer that sends data to a Kafka topic in Confluent Cloud. The script reads the Confluent Cloud configuration from the python.config file and creates a Producer instance using these settings. The script also includes a function, movie_api_get, that sends a GET request to an API and processes the response into a pandas DataFrame. The data from this DataFrame is then sent to the Kafka topic as a JSON string using the produce method of the Producer instance. The script includes a callback function, acked, that is called when a message has been successfully delivered or permanently failed delivery. The script runs in an infinite loop, sending data to the Kafka topic every 20 seconds until it is interrupted by the user.

**Script “consumer.py”**: This script is a Kafka consumer that receives data from a Kafka topic in Confluent Cloud and processes it. The script reads the Confluent Cloud configuration from the python.config file and creates a Consumer instance using these settings. The script subscribes to the Kafka topic and polls for new messages in an infinite loop. When a new message is received, the script decodes the message value, which is a JSON string, and converts it into a pandas DataFrame. The script then extracts the user ID from this DataFrame and sends a GET request to a local FastAPI application to get the top 10 suggested movies for this user. The resulting data is then inserted into a PostgreSQL database using the to_sql method of the pandas DataFrame.

**Remark**: Before proceeding to install and run the three scripts (app.py, producer.py, and consumer.py), it's essential to establish the right environment with the necessary dependencies. To achieve this, follow these steps:
1.	**Install Miniconda**: Begin by installing Miniconda, a minimal Conda installer, by downloading the installer script from the Miniconda website and following the platform-specific installation instructions.
2.	**Open Terminal**: Open a terminal on your Ubuntu system.
3.	**Create Conda Environment**: Use the terminal to create a new Conda environment named "kafka_airflow_fasapi" with Python version 3.10: 
**conda create -n kafka_airflow_fasapi python=3.10**
4.	**Activate Environment**: Activate the newly created environment: 
**conda activate kafka_airflow_fasapi**
5.	**Install Libraries**: In the activated environment, install the required libraries using Conda and Pip. The libraries that have been installed in the environment include argparse, sys, confluent_kafka, confluent_kafka.avro, confluent_kafka.admin, uuid, joblib, pandas, io, requests, datetime, time, psycopg2, and sqlalchemy : 
**conda install -c conda-forge argparse pandas
pip install confluent-kafka confluent-kafka[avro] joblib requests psycopg2 sqlalchemy**

## How to launch: Airflow dags, FASTAPI and Kafka streaming:

### Steps to launch:

a.	**Check Python Version:** Verify your Python version. If it's Python 3.10, use that version in the following steps. For example: python3.10 –version


b.	**Install Apache Airflow:** Install Apache Airflow 2.6.3 using pip with the specified Python version and constraints: 
**pip install 'apache-airflow==2.6.3' --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.6.3/constraints-3.10.txt**


c.	**Set AIRFLOW_HOME:** Set the AIRFLOW_HOME environment variable to the current directory: 
**export AIRFLOW_HOME=.**

d.	**Initialize Airflow Database:** Initialize the Airflow database: airflow db init

e.	**Start Airflow Web Server:** Start the Airflow web server to manage your DAGs locally. Choose a port number (e.g., 8080): airflow webserver -p 8080 (Access the Airflow UI by visiting http://localhost:8080 in your web browser.)

![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/4e788f86-8ad0-4fc0-bbd1-4cdb01a1f9ef)

f.	**Create Admin User:** Create an admin user for authentication in the Airflow UI: **airflow users create --username admin --firstname FIRST_NAME --lastname LAST_NAME --password admin --role Admin --email admin@example.org**

g.	**Start Airflow Scheduler:** Launch the Airflow scheduler to handle DAG scheduling: airflow scheduler
After starting the scheduler, open your web browser and navigate to http://localhost:8080 to access the Airflow UI. Once the UI is open, you should see the daily_dag listed among your DAGs. This allows you to monitor, trigger, and manage the execution of your daily_dag from the Airflow UI.


![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/1b320555-3699-4259-988b-26d063f890eb)

h.	**Run daily_dag from Airflow UI:** After accessing the Airflow UI at http://localhost:8080, locate and trigger the daily_dag from the UI. This will execute the DAG according to its schedule and defined tasks.


![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/2879e135-a0e9-40dc-982d-0902ea8e898d)


i.	**DAG Definition:** The **daily_dag** is defined in the **dag.py** script. This DAG includes tasks such as **run_start**, **run_all**, and **run_end**. The **run_all** task is responsible for executing the three scripts. It starts by launching **app.py** (FASTAPI) first. To accommodate the large size of the FASTAPI model, there is a 500-second delay to ensure that the FASTAPI launches successfully before the **consumer.py** script starts. This delay is crucial to prevent the **consumer.py** script from failing as it depends on the **FASTAPI**. Furthermore, the **producer.py** and **consumer.py** scripts are launched in the background within the Ubuntu shell.

If we launch in shell **python3 producer.py**:

![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/c89156bc-1647-4a21-8cf8-1e2be66a73d2)

If we launch in shell **python3 consumer.py**:

![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/6998b725-ed37-4e69-b612-44f799b1af37)


This allows them to operate simultaneously without blocking each other, enhancing the overall efficiency of the data streaming process.
During the execution of the **daily_dag**, the **app.py** (FASTAPI) script can be accessed via a web browser by navigating to **http://localhost:4000**. This allows you to interact with the FastAPI application and make movie recommendations for a given user ID.
While these scripts are executing, you can observe the progress and interactions in Confluent Kafka. The corresponding producer and consumer graphs will be displayed, showcasing the real-time data flow and communication between the components. This graphical representation provides valuable insights into the functionality and performance of your data streaming system



![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/782096a2-ee46-466d-9617-5b99fb2ef2cb)



j. **Data Storage:**
The data generated by the Kafka producer and processed by the Kafka consumer will be managed in two ways:

•	**Amazon S3 Storage:** Using Amazon S3 Sink, the data produced by your Kafka producer will be efficiently stored in an Amazon S3 bucket (AWS). This scalable storage solution ensures that your data is preserv ed and easily accessible for future analysis and processing.

•	**PostgreSQL Database Storage:** On the consumer side, the processed data will be stored in a PostgreSQL database. This relational database offers structured storage for your data, making it suitable for various querying and reporting needs.

• **Monitor DAG Execution:** Monitor the execution of our DAG in the Airflow UI. We should be able to see the progress of each task and their status.


![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/809820da-c434-4f41-8aea-d569b5480694)

## Global Kafka Confluent Streaming Diagram:

The Kafka Confluent data flow involves real-time data generation from the Jedha API, processed by producer.py to be published in Kafka topics. Kafka Confluent, integrated with Amazon S3 Sink, stores data in an S3 bucket. The consumer.py script consumes data, FastAPI predicts movie recommendations, and PostgreSQL stores results. DataClips visualize data, while Zapier automates email notifications for new predictions.
This orchestrated flow enables efficient data streaming, processing, and storage, enhancing the Netflix recommendation engine's functionality and user experience

![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/61c6c3d9-3dc4-4a77-977b-b8810176341d)



# ![image](https://github.com/billel0912/LEAD-Bloc1-Netflix-Recommendation-Jedha/assets/114284427/6386d9f5-74d6-4105-8cc2-a52700a3521d) Remark: 
**Due to GitHub's file size limitations (files over 25 MB cannot be uploaded), the original large files data_cleaned.csv and model.pkl have been replaced with smaller sample versions named data_cleaned_sample.csv and model_sample.pkl. These sample files are available in the corresponding Preprocessing_Netflix_Sample_GitHub and Project_Final_Kafka_Sample_GitHub directories on GitHub. For the full-sized files, refer to the Google Drive directories.**
