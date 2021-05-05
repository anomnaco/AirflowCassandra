from datetime import timedelta
from textwrap import dedent
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.providers.apache.cassandra.sensors.record import CassandraRecordSensor
from airflow.providers.apache.cassandra.sensors.table import CassandraTableSensor
from airflow.providers.apache.cassandra.hooks.cassandra import CassandraHook
import pprint


default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

hook = CassandraHook('cassandra_default')
pp = pprint.PrettyPrinter(indent=4)

def check_table_exists(keyspace_name, table_name):
    print("Checking for existence of "+keyspace_name+"."+table_name)
    hook.keyspace = keyspace_name
    return hook.table_exists(table_name)

def execute_query(query):
    pp.pprint( hook.get_conn().execute(query).current_rows )

select_all_query = "SELECT * FROM test.users;"

with DAG(
    'cass_hooks_tutorial',
    default_args=default_args,
    description='An example Cassandra DAG using cassandra hooks',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['tutorial'],
) as dag:

    table_check = PythonOperator(
        task_id = 'table_check',
        python_callable=check_table_exists,
        op_args = ['test', 'users']
    )

    select_all = PythonOperator(
        task_id = 'select_all',
        python_callable=execute_query,
        op_args=[select_all_query]
    )

    table_check >> select_all