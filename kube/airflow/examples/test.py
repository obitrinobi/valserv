from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

def print_hello():
 return 'Hello Wolrd'

def print_hello2():
 return 'Hello world 2'

dag = DAG('hello_world', description='Hello world example', schedule_interval='0 12 * * *', start_date=datetime(2017, 3, 20), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries = 3, dag=dag)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)

hello_op2 = PythonOperator(task_id='hello_task2', python_callable=print_hello2, dag=dag)
dummy_operator >> [hello_operator, hello_op2] 

