# Open Data Discovery Resource Name Generator
## Requirements
Python >= 3.7
## Installation
```
poetry install
```
## Usage and configuration
### Available generators
* postgresql - PostgresqlGenerator
* mysql - MysqlGenerator
* glue - GlueGenerator
* kafka - KafkaGenerator
* kafkaconnect - KafkaConnectGenerator
* snowflake - SnowflakeGenerator
* airflow - AirflowGenerator
* hive - HiveGenerator
* dynamodb - DynamodbGenerator
* odbc - OdbcGenerator
* mssql - MssqlGenerator
* oracle - OracleGenerator
* redshift - RedshiftGenerator
* clickhouse - ClickHouseGenerator
* athena - AthenaGenerator
* quicksight - QuicksightGenerator
* dbt - DbtGenerator
### Work in progress generators
* tableau - TableauGenerator
* kubeflow - KubeflowGenerator
* dvc - DVCGenerator
* great_expectations - GreatExpectationsGenerator

### Generator properties
* base_oddrn - Get base oddrn (without path)
* available_paths - Get all available path of generator 

### Generator methods
* get_oddrn_by_path(path_name, new_value=None) - Get oddrn string by path. You also can set value for this path using 'new_value' param
* set_oddrn_paths(**kwargs) - Set or update values of oddrn path
* get_data_source_oddrn() - Get datasouce oddrn 

### Generator parameters:
* host_settings: str - optional. Hostname configuration
* cloud_settings: dict - optional.  Cloud configuration
* **kwargs - path's name and values

### Example usage
```python
# postgresql
from oddrn_generator import PostgresqlGenerator
oddrn_gen = PostgresqlGenerator(
  host_settings='my.host.com:5432', 
  schemas='schema_name', databases='database_name', tables='table_name'
)

oddrn_gen.base_oddrn
# //postgresql/host/my.host.com:5432/
oddrn_gen.available_paths
# ('schemas', 'databases', 'tables', 'columns')

oddrn_gen.get_data_source_oddrn()
# //postgresql/host/my.host.com:5432/schemas/schema_name/databases/database_name

oddrn_gen.get_oddrn_by_path("schemas")
# //postgresql/host/my.host.com:5432/schemas/schema_name

oddrn_gen.get_oddrn_by_path("databases")
# //postgresql/host/my.host.com:5432/schemas/schema_name/databases/database_name

oddrn_gen.get_oddrn_by_path("tables")
# //postgresql/host/my.host.com:5432/schemas/schema_name/databases/database_name/tables/table_name

# you can set or change path:
oddrn_gen.set_oddrn_paths(tables='another_table_name', columns='new_column_name')
oddrn_gen.get_oddrn_by_path("columns")
# //postgresql/host/my.host.com:5432/schemas/schema_name/databases/database_name/tables/another_table_name/columns/new_column_name

# you can get path wih new values:
oddrn_gen.get_oddrn_by_path("columns", new_value="another_new_column_name")
# //postgresql/host/my.host.com:5432/schemas/schema_name/databases/database_name/tables/another_table_name/columns/another_new_column_name


# glue
from oddrn_generator import GlueGenerator
oddrn_gen = GlueGenerator(
  cloud_settings={'account': 'acc_id', 'region':'reg_id'}, 
  databases='database_name', tables='table_name', columns='column_name', 
  jobs='job_name', runs='run_name', owners='owner_name'
)

oddrn_gen.available_paths
# ('databases', 'tables', 'columns', 'owners', 'jobs', 'runs')

oddrn_gen.get_oddrn_by_path("databases")
# //glue/cloud/aws/account/acc_id/region/reg_id/databases/database_name

oddrn_gen.get_oddrn_by_path("tables")
# //glue/cloud/aws/account/acc_id/region/reg_id/databases/database_name/tables/table_name'

oddrn_gen.get_oddrn_by_path("columns")
# //glue/cloud/aws/account/acc_id/region/reg_id/databases/database_name/tables/table_name/columns/column_name

oddrn_gen.get_oddrn_by_path("jobs")
# //glue/cloud/aws/account/acc_id/region/reg_id/jobs/job_name

oddrn_gen.get_oddrn_by_path("runs")
# //glue/cloud/aws/account/acc_id/region/reg_id/jobs/job_name/runs/run_name

oddrn_gen.get_oddrn_by_path("owners")
# //glue/cloud/aws/account/acc_id/region/reg_id/owners/owner_name

```

### Exceptions
* WrongPathOrderException - raises when trying set path that depends on another path
```python
from oddrn_generator import PostgresqlGenerator
oddrn_gen = PostgresqlGenerator(
    host_settings='my.host.com:5432', 
    schemas='schema_name', databases='database_name',
    columns='column_without_table'
)
# WrongPathOrderException: 'columns' can not be without 'tables' attribute
```
* EmptyPathValueException - raises when trying to get a path that is not set up
```python
from oddrn_generator import PostgresqlGenerator
oddrn_gen = PostgresqlGenerator(
    host_settings='my.host.com:5432', schemas='schema_name', databases='database_name',
)
oddrn_gen.get_oddrn_by_path("tables")

# EmptyPathValueException: Path 'tables' is not set up
```
* PathDoestExistException - raises when trying to get not existing oddrn path
```python
from oddrn_generator import PostgresqlGenerator
oddrn_gen = PostgresqlGenerator(
    host_settings='my.host.com:5432', schemas='schema_name', databases='database_name',
)
oddrn_gen.get_oddrn_by_path("jobs")

# PathDoestExistException: Path 'jobs' doesn't exist in generator
```