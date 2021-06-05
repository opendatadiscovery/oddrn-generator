# OpenDataDiscovery ODDRN
## Requirements
Python >= 3.7
## Installation
```
    pip install oddrn
```
## Usage and configuration
```python
from oddrn import Generator
oddrn_gen = Generator(data_source="postgresql", cloud={"type":"aws", "region":"reg_id", "account": "acc_id"})
oddrn_gen.get_column("db_name","schema_name","table_name", "column_name")
```
### Generator parameters:
* "data_source" - required. Can be one of:
```python
["postgresql", "mysql", "kafka", "glue", "snowflake", "airflow", "tableau", "hive", "dynamodb", "kuberflow", "odbc", "mssql", "oracle", "redshift"]
```
* cloud: dict - optional. At now support only AWS. Mutually exclusive with "prefix" or "prefixes" params)
* host: str or hosts: list[str] - optional. 
* prefix: str or prefixes: list[str] - optional. Mutually exclusive with "cloud" param

### Methods list:
* postgresql:
    * get_database(database_name)
    * get_schema(database_name, schema_name)
    * get_table(database_name, schema_name, table_name)
    * get_column(database_name, schema_name, table_name, column_name)
* mysql
    * get_database(database_name)
    * get_table(database_name, table_name)
    * get_column(database_name, table_name, column_name)
* kafka
    * Work in progress
* glue
    * get_owner(owner_name)
    * get_database(database_name)
    * get_table(database_name, table_name)
    * get_column(database_name, table_name, column_name)
    * get_job(job_name)
* snowflake
    * get_owner(owner_name)
    * get_warehouse(warehouse_name)
    * get_database(warehouse_name, database_name)
    * get_schema(warehouse_name, database_name, schema_name)
    * get_table(warehouse_name, database_name, schema_name, table_name)
    * get_view(warehouse_name, database_name, schema_name, view_name)
    * get_column(warehouse_name, database_name, schema_name, table_name, column_name)
* airflow
    * Work in progress
* tableau
    * get_database(database_name)
    * get_schema(database_name, schema_name)
    * get_table(database_name, schema_name, table_name)
    * get_column(database_name, schema_name, table_name, column_name)
    * get_workbook(workbook_name)
    * get_worksheet(workbook_name, worksheet_name)
* hive
    * get_owner(owner_name)
    * get_database(database_name)
    * get_table(database_name, table_name)
    * get_column(database_name, table_name, column_name)
* dynamodb
    * get_database(database_name)
    * get_schema(database_name, schema_name)
    * get_table(database_name, schema_name, table_name)
    * get_column(database_name, schema_name, table_name, column_name)
* kuberflow
    * get_pipeline(pipeline_id)
    * get_experiment(experiment_id)
    * get_experiment_run(experiment_id, run_id)
* odbc
    * get_database(database_name)
    * get_schema(database_name, schema_name)
    * get_table(database_name, schema_name, table_name)
    * get_column(database_name, schema_name, table_name, column_name)
* mssql
    * get_database(database_name)
    * get_schema(database_name, schema_name)
    * get_table(database_name, schema_name, table_name)
    * get_column(database_name, schema_name, table_name, column_name)
* oracle
    * get_database(database_name)
    * get_schema(database_name, schema_name)
    * get_table(database_name, schema_name, table_name)
    * get_column(database_name, schema_name, table_name, column_name)
* redshift
    * get_database(database_name)
    * get_schema(database_name, schema_name)
    * get_table(database_name, schema_name, table_name)
    * get_column(database_name, schema_name, table_name, column_name)

If you need to generate full custom oddrn, use method create_full_oddrn(data: OrderedDict)
Example:
```python
from oddrn import Generator
from collections import OrderedDict
data = OrderedDict({
    "sources": "CustomSource",
    "hosts": "localhost:3333",
    "databases": "test_db",
    "tables": "test_table"
})
Generator.create_full_oddrn(data)
'//sources/CustomSource/hosts/localhost:3333/databases/test_db/tables/test_table'
``` 
### Cloud support:
To add new cloud, you need to add new dataclass with method get_oddrn to clouds.py and add it to cloud_map variable

### Adapter support:
To add new adapter, simply add new class to oddrn.py. Parameter "source" is required.
