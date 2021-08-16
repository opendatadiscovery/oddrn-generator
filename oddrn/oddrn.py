import enum
import copy

from collections import OrderedDict
from typing import List

from oddrn.mixins import DatabaseMixin, DatabaseSchemaMixin, OwnerMixin
from oddrn.clouds import cloud_map


class SourceType(enum.Enum):
    POSTGRESQL = "postgres"
    MYSQL = "mysql"


class Generator:
    source = None

    def __new__(cls, *args, **kwargs):
        subclass_map = {subclass.source: subclass for subclass in cls.__subclasses__()}
        try:
            subclass = subclass_map[kwargs["data_source"]]
        except Exception:
            raise Exception("data_source is invalid")
        instance = super(Generator, subclass).__new__(subclass)
        return instance

    def __init__(self, data_source: SourceType, cloud: dict=None, prefix: str=None,
                 prefixes:  List[str]=None, host: str=None, hosts: List[str]=None):
        self._validate_params(cloud, prefix, prefixes, host, hosts)
        self._cloud = self._validate_cloud(cloud)
        self._prefix = self._get_prefix(prefix, prefixes)
        self._source = data_source
        self._hosts = self._get_hosts(host, hosts)
        parts = [part for part in [self._prefix, self._source, self._hosts] if part]
        self._base_oddrn = "//" + "/".join(parts)

    @staticmethod
    def _validate_params(cloud, prefix, prefixes, host, hosts):
        # Maybe convert to dataclass or pydantic/schema?
        if prefixes and prefix:
            raise ValueError("You must specify only one parameter: 'prefix' or 'prefixes'")
        if cloud and (prefixes or prefix):
            raise ValueError("You must specify only one parameter: 'cloud' or 'prefix/prefixes'")
        if host and hosts:
            raise ValueError("You must specify only one parameter: 'host' or 'hosts'")
        return None

    @staticmethod
    def _validate_cloud(cloud=None):
        if cloud:
            # TODO - make it better!
            cloud_copy = {
                "cloud": cloud["type"],
                "region": cloud["region"],
                "account": cloud["account"],
            }
            try:
                cloud_type = cloud_copy.pop("cloud")
                cloud_dataclass = cloud_map[cloud_type]
                return cloud_dataclass(**cloud_copy)
            except Exception as e:
                raise ValueError(f"Cloud validation error {str(e)}")
        else:
            return None

    def _get_prefix(self, prefix: str, prefixes: List[str]) -> str:
        if self._cloud:
            oddrn = self._cloud.get_oddrn()
        elif prefix:
            oddrn = prefix
        elif prefixes:
            oddrn = ",".join(prefixes)
        else:
            oddrn = ""
        return oddrn

    @staticmethod
    def _get_hosts(host: str, hosts: List[str]) -> str:
        return host if host else ",".join(hosts) if hosts else ""

    @classmethod
    def create_full_oddrn(cls, data: OrderedDict) -> str:
        data_str = cls._concat_dict(data)
        return f"//{data_str}"

    @staticmethod
    def _concat_dict(data: OrderedDict) -> str:
        entities = [f"{key}/{value}" for key, value in data.items()]
        return "/".join(entities)

    def get_base(self) -> str:
        return self._base_oddrn

    def get_oddrns(self, data: List[OrderedDict]) -> List[str]:
        return [self.get_oddrn(obj) for obj in data]

    def get_oddrn(self, data: OrderedDict) -> str:
        oddrn = self._concat_dict(data)
        return f"{self._base_oddrn}/{oddrn}"


class PostgresGenerator(Generator, DatabaseSchemaMixin):
    source = "postgresql"


class MysqlGenerator(Generator, DatabaseMixin):
    source = "mysql"


class KafkaGenerator(Generator):
    source = "kafka"


class GlueGenerator(Generator, DatabaseMixin, OwnerMixin):
    source = "glue"

    def get_job(self, job_name: str) -> str:
        data = OrderedDict({"jobs": job_name})
        return self.get_oddrn(data)


class SnowflakeGenerator(Generator, OwnerMixin):
    source = "snowflake"

    def get_warehouse(self, warehouse_name: str) -> str:
        data = OrderedDict({"warehouses": warehouse_name})
        return self.get_oddrn(data)

    def get_database(self, warehouse_name: str, database_name: str) -> str:
        data = OrderedDict({
            "warehouses": warehouse_name,
            "databases": database_name
        })
        return self.get_oddrn(data)

    def get_schema(self, warehouse_name: str, database_name: str, schema_name: str) -> str:
        data = OrderedDict({
            "warehouses": warehouse_name,
            "databases": database_name,
            "schemas": schema_name
        })
        return self.get_oddrn(data)

    def get_table(self, warehouse_name: str, database_name: str, schema_name: str, table_name: str) -> str:
        data = OrderedDict({
            "warehouses": warehouse_name,
            "databases": database_name,
            "schemas": schema_name,
            "tables": table_name
        })
        return self.get_oddrn(data)

    def get_view(self, warehouse_name: str, database_name: str, schema_name: str, view_name: str) -> str:
        data = OrderedDict({
            "warehouses": warehouse_name,
            "databases": database_name,
            "schemas": schema_name,
            "views": view_name

        })
        return self.get_oddrn(data)

    def get_column(self, warehouse_name: str, database_name: str,
                   schema_name: str, table_name: str, column_name) -> str:
        data = OrderedDict({
            "warehouses": warehouse_name,
            "databases": database_name,
            "schemas": schema_name,
            "tables": table_name,
            "column": column_name
        })
        return self.get_oddrn(data)


class AirflowGenerator(Generator):
    source = "airflow"

    def get_dag(self, dag_id: str) -> str:
        data = OrderedDict({"dags": dag_id})
        return self.get_oddrn(data)

    def get_task(self, dag_id: str, task_id: str) -> str:
        data = OrderedDict({
            "dags": dag_id,
            "tasks": task_id

        })
        return self.get_oddrn(data)

    def get_task_run(self, dag_id: str, task_id: str, run_id: str) -> str:
        data = OrderedDict({
            "dags": dag_id,
            "tasks": task_id,
            "runs": run_id
        })
        return self.get_oddrn(data)


class TableauGenerator(Generator, DatabaseSchemaMixin):
    source = "tableau"

    def get_workbook(self, workbook_name: str) -> str:
        data = OrderedDict({"workbooks": workbook_name})
        return self.get_oddrn(data)

    def get_worksheet(self, workbook_name: str, worksheet_name: str) -> str:
        data = OrderedDict({
            "workbooks": workbook_name,
            "worksheets": worksheet_name
        })
        return self.get_oddrn(data)


class HiveGenerator(Generator, DatabaseMixin, OwnerMixin):
    source = "hive"


class DynamodbGenerator(Generator, DatabaseSchemaMixin):
    source = "dynamodb"


class KuberflowGenerator(Generator):
    source = "kuberflow"

    def get_pipeline(self, pipeline_id: str) -> str:
        data = OrderedDict({"pipelines": pipeline_id})
        return self.get_oddrn(data)

    def get_experiment(self, experiment_id: str) -> str:
        data = OrderedDict({"experiments": experiment_id})
        return self.get_oddrn(data)

    def get_experiment_run(self, experiment_id: str, run_id: str) -> str:
        data = OrderedDict({
            "experiments": experiment_id,
            "runs": run_id
        })
        return self.get_oddrn(data)


class OdbcGenerator(Generator, DatabaseSchemaMixin):
    source = "odbc"


class MssqlGenerator(Generator, DatabaseSchemaMixin):
    source = "mssql"


class OracleGenerator(Generator, DatabaseSchemaMixin):
    source = "oracle"


class RedshiftGenerator(Generator, DatabaseSchemaMixin):
    source = "redshift"


class ClickHouseGenerator(Generator, DatabaseMixin):
    source = "clickhouse"


class DVCGenerator(Generator):
    source = "dvc"

    def get_stage(self, name: str) -> str:
        data = OrderedDict({"stages": name})
        return self.get_oddrn(data)

    def get_dataset(self, file_path: str) -> str:
        folders = [f"folder/{path}" for path in file_path.split("/")]
        oddrn = "/".join(folders)
        return f"{self._base_oddrn}/{oddrn}"


class GreatExpectationsGenerator(Generator):
    source = "great_expectations"

    def get_qt(self, suit_name: str, expectation_type: str) -> str:
        data = OrderedDict({
            "suits": suit_name,
            "types": expectation_type
        })
        return self.get_oddrn(data)

    def get_qt_run(self, run_name: str, expectation_type: str) -> str:
        data = OrderedDict({
            "runs": run_name,
            "types": expectation_type
        })
        return self.get_oddrn(data)

# TODO	Add Kafka support
#	Add inputs to kuberflow

