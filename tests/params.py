from oddrn_generator.generators import (
    PostgresqlGenerator, MysqlGenerator, SnowflakeGenerator, AirflowGenerator, HiveGenerator, GlueGenerator,
    DynamodbGenerator, OdbcGenerator, MssqlGenerator, OracleGenerator, RedshiftGenerator, ClickHouseGenerator,
    KafkaConnectGenerator, KafkaGenerator
)

parameters_host = [
    (
        PostgresqlGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'schemas': 'some_schema',
                'databases': 'some_database',
                'tables': 'some_table',
                'columns': 'some_column',
            },
            'aliases': {}
        }
    ),
    (
        MysqlGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'databases': 'some_database',
                'tables': 'some_table',
                'columns': 'some_column',
            },
            'aliases': {}
        }
    ),
    (
        SnowflakeGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'warehouses': 'some_warehouse',
                'databases': 'some_database',
                'schemas': 'some_schema',
                'tables': 'some_table',
                'views': 'some_view',
                'columns': 'some_column',
                'owners': 'some_owner',
            },
            'aliases': {}
        }
    ),
    (
        AirflowGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'dags': 'some_dag',
                'tasks': 'some_task',
                'runs': 'some_run',
            },
            'aliases': {}
        }
    ),
    (
        HiveGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'databases': 'some_database',
                'tables': 'some_table',
                'columns': 'some_column',
                'owners': 'some_owner',
            },
            'aliases': {}
        }
    ),
    (
        OdbcGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'databases': 'some_database',
                'schemas': 'some_schema',
                'tables': 'some_table',
                'columns': 'some_column',
            },
            'aliases': {}
        }
    ),
    (
        MssqlGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'databases': 'some_database',
                'schemas': 'some_schema',
                'tables': 'some_table',
                'columns': 'some_column',
            },
            'aliases': {}
        }
    ),
    (
        OracleGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'databases': 'some_database',
                'schemas': 'some_schema',
                'tables': 'some_table',
                'columns': 'some_column',
            },
            'aliases': {}
        }
    ),
    (
        RedshiftGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'databases': 'some_database',
                'schemas': 'some_schema',
                'tables': 'some_table',
                'columns': 'some_column',
            },
            'aliases': {}
        }
    ),
    (
        ClickHouseGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'databases': 'some_database',
                'tables': 'some_table',
                'columns': 'some_column',
            },
            'aliases': {}
        }
    ),
    (
        KafkaGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'units': 'some_unit',
                'topics': 'some_topics',
            },
            'aliases': {}
        }
    ),
    (
        KafkaConnectGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'connectors': 'some_connector',
            },
            'aliases': {}
        }
    ),
]

parameters_cloud = [
    (
        GlueGenerator,
        {
            'cloud_settings': {
                'account': '21232132',
                'region': 'us-west',
            },
            'paths': {
                'databases': 'some_database',
                'tables': 'some_table',
                'columns': 'some_column',
                'owners': 'some_owner',
                'jobs': 'some_jobs',
                'runs': 'some_runs',
            },
            'aliases': {}
        }
    ),
    (
        DynamodbGenerator,
        {
            'cloud_settings': {
                'account': '21232132',
                'region': 'us-west',
            },
            'paths': {
                'schemas': 'some_schema',
                'databases': 'some_database',
                'tables': 'some_table',
                'columns': 'some_column',
            },
            'aliases': {}
        }
    ),
]
