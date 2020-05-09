# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG, macros
# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
# from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Parse nodes
import json
JSON_MANIFEST_DBT = '/dbt/target/manifest.json'
PARENT_MAP = 'parent_map'

def sanitise_node_names(value):
        segments = value.split('.')
        if (segments[0] == 'model'):
                return value.split('.')[-1]

def get_node_structure():
    with open(JSON_MANIFEST_DBT) as json_data:
        data = json.load(json_data)
    ancestors_data = data[PARENT_MAP]
    tree = {}
    for node in ancestors_data:
            ancestors = list(set(ancestors_data[node]))
            ancestors_2 = []
            for ancestor in ancestors:
                if (sanitise_node_names(ancestor) is not None):
                    ancestors_2.append(sanitise_node_names(ancestor))
                    
            clean_node_name = sanitise_node_names(node)
            if (clean_node_name is not None) and (ancestors_2 is not None):
                    tree[clean_node_name] = {}
                    tree[clean_node_name]['ancestors'] = ancestors_2
                    tree[clean_node_name]['tags'] = data['nodes'][node]['tags']
    
    return tree


# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(5),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}
# [END default_args]

# [START instantiate_dag]
daily_dag = DAG(
    'daily_dbt_models',
    default_args=default_args,
    description='Managing dbt data pipeline',
    schedule_interval = '@daily',
)
daily_operators = {}

snapshot_dag = DAG(
    'snapshot_dbt_models',
    default_args=default_args,
    description='Managing dbt data pipeline',
    schedule_interval = None,
)
snapshot_operators = {}

init_once_dag = DAG(
    'init_once_dbt_models',
    default_args=default_args,
    description='Managing dbt data pipeline',
    schedule_interval = None,
)
init_once_operators = {}

all_operators = {}
# [END instantiate_dag]

nodes = get_node_structure()

for node in nodes:
    if ('daily' in nodes[node]['tags']):
        date_end = "{{ ds }}"
        date_start = "{{ yesterday_ds }}"
        bsh_cmd = 'cd /dbt && dbt run --models {nodeName} --vars \'{{"start_date":"{start_date}", "end_date":"{end_date}"}}\' '.format(nodeName = node, start_date = date_start, end_date = date_end)
        tmp_operator = BashOperator(
            task_id= node,
            bash_command=bsh_cmd,
            dag=daily_dag,
        )
        daily_operators[node] = tmp_operator
        all_operators[node] = tmp_operator

    elif ('snapshot' in nodes[node]['tags']):
        bsh_cmd = 'cd /dbt && dbt run --models {nodeName} '.format(nodeName = node)
        tmp_operator = BashOperator(
            task_id= node,
            bash_command=bsh_cmd,
            dag=snapshot_dag,
        )
        snapshot_operators[node] = tmp_operator
        all_operators[node] = tmp_operator

    elif ('init-once' in nodes[node]['tags']):
        date_end = "{{ ds }}"
        date_start = "{{ yesterday_ds }}"
        bsh_cmd = 'cd /dbt && dbt run --models {nodeName} '.format(nodeName = node)
        tmp_operator = BashOperator(
            task_id= node,
            bash_command=bsh_cmd,
            dag=init_once_dag,
        )
        init_once_operators[node] = tmp_operator
        all_operators[node] = tmp_operator

for node in nodes:
    for parent in nodes[node]['ancestors']:
        if nodes[node]['tags'] == nodes[parent]['tags']:
            all_operators[parent] >> all_operators[node]