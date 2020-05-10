from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.dates import days_ago
from datetime import datetime

# [START default_args]
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}
# [END default_args]

# [START instantiate_dag]
load_initial_data_dag = DAG(
    '1_load_initial_data',
    default_args=default_args,
    schedule_interval = None,
)

t1 = PostgresOperator(task_id='create_schema',
                      sql="CREATE SCHEMA IF NOT EXISTS dbt_raw_data;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t2 = PostgresOperator(task_id='drop_table_aisles',
                      sql="DROP TABLE IF EXISTS aisles;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t3 = PostgresOperator(task_id='create_aisles',
                      sql="create table if not exists dbt_raw_data.aisles (aisle_id integer, aisle varchar(100) );",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t4 = PostgresOperator(task_id='load_aisles',
                      sql="COPY dbt_raw_data.aisles FROM '/sample_data/aisles.csv' DELIMITER ',' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t5 = PostgresOperator(task_id='drop_table_departments',
                      sql="DROP TABLE IF EXISTS departments;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t6 = PostgresOperator(task_id='create_departments',
                      sql="create table if not exists dbt_raw_data.departments (department_id integer, department varchar(100));",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t7 = PostgresOperator(task_id='load_departments',
                      sql="	COPY dbt_raw_data.departments FROM '/sample_data/departments.csv' DELIMITER ',' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)                     

t8 = PostgresOperator(task_id='drop_table_products',
                      sql="DROP TABLE IF EXISTS aisles;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t9 = PostgresOperator(task_id='create_products',
                      sql="create table if not exists dbt_raw_data.products (product_id integer, product_name varchar(200),	aisle_id integer, department_id integer);",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t10 = PostgresOperator(task_id='load_products',
                      sql="	COPY dbt_raw_data.products FROM '/sample_data/products.csv' DELIMITER ',' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)  

t11 = PostgresOperator(task_id='drop_table_orders',
                      sql="DROP TABLE IF EXISTS orders;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t12 = PostgresOperator(task_id='create_orders',
                      sql="create table if not exists dbt_raw_data.orders ( order_id integer,user_id integer, eval_set varchar(10), order_number integer,order_dow integer,order_hour_of_day integer, days_since_prior_order real);",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t13 = PostgresOperator(task_id='load_orders',
                      sql="	COPY dbt_raw_data.orders FROM '/sample_data/orders.csv' DELIMITER ',' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag) 

t14 = PostgresOperator(task_id='drop_table_order_products__prior',
                      sql="DROP TABLE IF EXISTS order_products__prior;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t15 = PostgresOperator(task_id='create_order_products__prior',
                      sql="create table if not exists dbt_raw_data.order_products__prior(order_id integer, product_id integer, add_to_cart_order integer, reordered integer);",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t16 = PostgresOperator(task_id='load_order_products__prior',
                      sql="	COPY dbt_raw_data.order_products__prior FROM '/sample_data/order_products__prior.csv' DELIMITER ',' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)   

t17 = PostgresOperator(task_id='drop_table_order_products__train',
                      sql="DROP TABLE IF EXISTS order_products__train;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t18 = PostgresOperator(task_id='create_order_products__train',
                      sql="create table if not exists dbt_raw_data.order_products__train(order_id integer, product_id integer, add_to_cart_order integer, reordered integer);",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)

t19 = PostgresOperator(task_id='load_order_products__train',
                      sql="	COPY dbt_raw_data.order_products__train FROM '/sample_data/order_products__train.csv' DELIMITER ',' CSV HEADER;",
                      postgres_conn_id='dbt_postgres_instance_raw_data',
                      autocommit=True,
                      database="dbtdb",
                      dag=load_initial_data_dag)       

t1 >> t2 >> t3 >> t4
t1 >> t5 >> t6 >> t7
t1 >> t8 >> t9 >> t10
t1 >> t11 >> t12 >> t13
t1 >> t14 >> t15 >> t16
t1 >> t17 >> t18 >> t19