from oddrn_generator.generators import (
    PostgresqlGenerator,
    MysqlGenerator,
    SnowflakeGenerator,
    AirflowGenerator,
    HiveGenerator,
    GlueGenerator,
    DynamodbGenerator,
    OdbcGenerator,
    MssqlGenerator,
    OracleGenerator,
    RedshiftGenerator,
    ClickHouseGenerator,
    KafkaConnectGenerator,
    KafkaGenerator,
    AthenaGenerator,
    QuicksightGenerator,
    TableauGenerator,
    PrefectGenerator,
    Neo4jGenerator,
    S3Generator,
    ElasticSearchGenerator,
    FeastGenerator,
    KinesisGenerator,
    MongoGenerator
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
                'views': 'some_view',
                'tables_columns': 'some_table_column',
                'views_columns': 'some_view_column',
            },
            'aliases': {
                'tables_columns': 'columns',
                'views_columns': 'columns',
            }
        }
    ),
    (
        MysqlGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'databases': 'some_database',
                'tables': 'some_table',
                'views': 'some_view',
                'tables_columns': 'some_table_column',
                'views_columns': 'some_view_column',
            },
            'aliases': {
                'tables_columns': 'columns',
                'views_columns': 'columns',
            }
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
                'tables_columns': 'some_table_column',
                'views_columns': 'some_view_column',
                'owners': 'some_owner',
            },
            'aliases': {
                'tables_columns': 'columns',
                'views_columns': 'columns',
            }
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
                'views': 'some_view',
                'tables_columns': 'some_table_column',
                'views_columns': 'some_view_column',
                'owners': 'some_owner',
            },
            'aliases': {
                'tables_columns': 'columns',
                'views_columns': 'columns',
            }
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
                'views': 'some_view',
                'tables_columns': 'some_table_column',
                'views_columns': 'some_view_column',
            },
            'aliases': {
                'tables_columns': 'columns',
                'views_columns': 'columns',
            }
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
                'views': 'some_view',
                'tables_columns': 'some_table_column',
                'views_columns': 'some_view_column',
            },
            'aliases': {
                'tables_columns': 'columns',
                'views_columns': 'columns',
            }
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
                'views': 'some_view',
                'tables_columns': 'some_table_column',
                'views_columns': 'some_view_column',
            },
            'aliases': {
                'tables_columns': 'columns',
                'views_columns': 'columns',
            }
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
                'views': 'some_view',
                'tables_columns': 'some_table_column',
                'views_columns': 'some_view_column',
            },
            'aliases': {
                'tables_columns': 'columns',
                'views_columns': 'columns',
            }
        }
    ),
    (
        ClickHouseGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'databases': 'some_database',
                'tables': 'some_table',
                'views': 'some_view',
                'tables_columns': 'some_table_column',
                'views_columns': 'some_view_column',
            },
            'aliases': {
                'tables_columns': 'columns',
                'views_columns': 'columns',
            }
        }
    ),
    (
        KafkaGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
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
    (
        TableauGenerator,
        {
            'host_settings': 'dub01.online.tableau.com',
            'paths': {
                'sites': 'some_site',
                'databases': 'some_database',
                'schemas': 'some_schema',
                'tables': 'some_table',
                'columns': 'some_column',
                'workbooks': 'some_workbook',
                'sheets': 'some_sheet',
            },
            'aliases': {}
        }
    ),
    (
        PrefectGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'flows': 'some_flow',
                'tasks': 'some_task',
                'runs': 'some_run',
            },
            'aliases': {}
        }
    ),
    (
        Neo4jGenerator,
        {
            'host_settings': '127.0.0.1:9687',
            'paths': {
                'databases': 'some_database',
                'nodes': 'some_node',
                'fields': 'some_field',
            },
            'aliases': {}
        }
    ),
    (
        ElasticSearchGenerator,
        {
            'host_settings': '127.0.0.1:9200',
            'paths': {
                'indexes': 'some_index',
                'fields': 'some_field',
            },
            'aliases': {}
        }
    ),
    (
        FeastGenerator,
        {
            'host_settings': 'some_unit_id',
            'paths': {
                'featureviews': 'some_feature_view_name',
                'features': 'some_feature_name',
                'subfeatures': 'some_subfeature_name',
            },
            'aliases': {}
        }
    ),
    (
        MongoGenerator,
        {
            'host_settings': '127.0.0.1:5034',
            'paths': {
                'databases': 'some_database',
                'schemas': 'some_schemas',
                'collections': 'some_collections',
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
                'tables': 'some_table',
                'columns': 'some_column',
            },
            'aliases': {}
        }
    ),
    (
        AthenaGenerator,
        {
            'cloud_settings': {
                'account': '21232132',
                'region': 'us-west',
            },
            'paths': {
                'catalogs': 'some_catalog',
                'databases': 'some_database',
                'tables': 'some_table',
                'views': 'some_view',
                'tables_columns': 'some_table_column',
                'views_columns': 'some_view_column',
            },
            'aliases': {
                'tables_columns': 'columns',
                'views_columns': 'columns',
            }
        }
    ),
    (
        QuicksightGenerator,
        {
            'cloud_settings': {
                'account': '21232132',
                'region': 'us-west',
            },
            'paths': {
                'datasets': 'some_dataset',
                'analyses': 'some_analysis',
                'dashboards': 'some_dashboard',
                'data_sources': 'some_data_sources',
            },
            'aliases': {}
        }
    ),
    (
        S3Generator,
        {
            'cloud_settings': {
                'account': '21232132',
                'region': 'us-west',
            },
            'paths': {
                'buckets': 'some_bucket',
                'keys': 'some_key',
                'columns': 'some_column',
            },
            'aliases': {}
        }
    ),
    (
        KinesisGenerator,
        {
            'cloud_settings': {
                'account': '21232132',
                'region': 'us-west',
            },
            'paths': {
                'streams': 'some_stream',
                'shards': 'some_shard',
                'data_records': 'some_data_record',
            },
            'aliases': {},
        },
    ),
]
