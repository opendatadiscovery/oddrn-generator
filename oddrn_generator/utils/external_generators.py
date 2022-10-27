from abc import abstractmethod
from pydantic import BaseSettings
from typing import Type, Optional
from oddrn_generator.generators import (
    Generator,
    PostgresqlGenerator,
    MssqlGenerator,
    MysqlGenerator,
    PrestoGenerator,
    TrinoGenerator,
    AthenaGenerator,
    CassandraGenerator,
    ClickHouseGenerator,
    HiveGenerator,
    MongoGenerator,
    Neo4jGenerator,
    OdbcGenerator,
    OracleGenerator,
    RedshiftGenerator,
    VerticaGenerator,
    SnowflakeGenerator,
)


class ExternalGeneratorMappingError(Exception):
    """
    Raise an exception if undefined source was found during mapping.
    """

    def __init__(self, source_name: str):
        super().__init__(f"Datasource {source_name} wasn't implemented yet")


class ExternalDbSettings(BaseSettings):
    """
    Stores connection settings and db name for an external source.
    """

    host: str
    port: Optional[int]
    database_name: str


class ExternalDbGenerator:
    """
    A class to get specific generator for different path names.
    ...

    Attributes
    ----------
    db_settings : ExternalDbSettings
        connection settings for database
    generator_cls : Generator
        specific generator for this source
    database_path_name : str
        name of level of database representation from path_models for specific generator
    schema_path_name : str
        name of level of schema representation from path_models for specific generator
    table_path_name : str
        name of level of table representation from path_models for specific generator

    """

    def __init__(self, db_settings: ExternalDbSettings):
        """
        Construct db settings attribute

        Parameters
        ----------

            db_settings: ExternalDbSettings
        """
        self.db_settings = db_settings

    generator_cls: Type[Generator]
    database_path_name: str
    schema_path_name: str
    table_path_name = "tables"

    def get_generator_for_database_lvl(self) -> Generator:
        """
        Get generator with predefined database only.
        takes database name from db settings

        Parameters
        ----------

        Returns
        -------
        Generator
        """
        return self.generator_cls(
            **{
                "host_settings": self.db_settings.host,
                self.database_path_name: self.db_settings.database_name,
            }
        )

    @abstractmethod
    def get_generator_for_schema_lvl(self, schema_name: str) -> Generator:
        """
        Get generator with predefined database and schema.

        Parameters
        ----------
            schema_name: str
                schema name for a source

        Returns
        -------
        Generator
        """
        pass

    def get_generator_for_table_lvl(
        self, schema_name: str, table_name: str
    ) -> Generator:
        """
        Get generator with predefined database and schema and table as well.

        Parameters
        ----------
            schema_name: str
                schema name for a source
            table_name: str
                table name for a source

        Returns
        -------
        Generator
        """
        gen = self.get_generator_for_schema_lvl(schema_name)
        gen.get_oddrn_by_path(self.table_path_name, table_name)
        return gen


class ExternalGeneratorBuilder:
    """
    A class to get specific external generator.
    ...

    Attributes
    ----------
     external_generator: Type[ExternalDbGenerator]
        external generator class
     type: str
        how this source is named in a specific adapter

    """

    external_generator: Type[ExternalDbGenerator]
    type: str

    @abstractmethod
    def build_db_settings(self) -> ExternalDbSettings:
        """
        Get db settings

        Parameters
        ----------
        Returns
        -------
        ExternalDbSettings
        """
        pass

    def get_external_generator(self) -> ExternalDbGenerator:
        """
        Get external generator

        Parameters
        ----------

        Returns
        -------
        ExternalDbGenerator
        """
        return self.external_generator(self.build_db_settings())


class DeepLvlGenerator(ExternalDbGenerator):
    """
    A class to get external generator for sources with 3 level structure.
    (databases-schema-table) for example Mssql, Postgres so on.
    ...

    """

    def get_generator_for_schema_lvl(self, schema_name: str) -> Generator:
        gen = self.get_generator_for_database_lvl()
        gen.get_oddrn_by_path(self.schema_path_name, schema_name)
        return gen


class ShallowLvlGenerator(ExternalDbGenerator):
    """
    A class to get external generator for sources with 2 level structure.
    (databases-table) for example Mysql.
    ...

    """

    def get_generator_for_schema_lvl(self, schema_name: str) -> Generator:
        return self.get_generator_for_database_lvl()


class ExternalPostgresGenerator(DeepLvlGenerator):
    generator_cls = PostgresqlGenerator
    database_path_name = "databases"
    schema_path_name = "schemas"


class ExternalMssqlGenerator(DeepLvlGenerator):
    generator_cls = MssqlGenerator
    database_path_name = "databases"
    schema_path_name = "schemas"


class ExternalMysqlGenerator(ShallowLvlGenerator):
    generator_cls = MysqlGenerator
    database_path_name = "databases"


class ExternalPrestoGenerator(DeepLvlGenerator):
    generator_cls = PrestoGenerator
    database_path_name = "catalogs"
    schema_path_name = "schemas"


class ExternalTrinoGenerator(ExternalPrestoGenerator):
    generator_cls = TrinoGenerator


class ExternalAthenaGenerator(DeepLvlGenerator):
    generator_cls = AthenaGenerator
    database_path_name = "catalogs"
    schema_path_name = "databases"


class ExternalCassandraGenerator(ShallowLvlGenerator):
    generator_cls = CassandraGenerator
    database_path_name = "keyspaces"


class ExternalClickHouseGenerator(ShallowLvlGenerator):
    generator_cls = ClickHouseGenerator
    database_path_name = "databases"


class ExternalHiveGenerator(ShallowLvlGenerator):
    generator_cls = HiveGenerator
    database_path_name = "databases"


class ExternalMongoGenerator(ShallowLvlGenerator):
    generator_cls = MongoGenerator
    database_path_name = "databases"
    table_path_name = "collections"


class ExternalNeo4jGenerator(ShallowLvlGenerator):
    generator_cls = Neo4jGenerator
    database_path_name = "databases"
    table_path_name = "nodes"


class ExternalOdbcGenerator(DeepLvlGenerator):
    generator_cls = OdbcGenerator
    database_path_name = "databases"
    schema_path_name = "schemas"


class ExternalOracleGenerator(DeepLvlGenerator):
    generator_cls = OracleGenerator
    database_path_name = "schemas"
    schema_path_name = "databases"


class ExternalRedshiftGenerator(DeepLvlGenerator):
    generator_cls = RedshiftGenerator
    database_path_name = "databases"
    schema_path_name = "schemas"


class ExternalVerticaGenerator(DeepLvlGenerator):
    generator_cls = VerticaGenerator
    database_path_name = "databases"
    schema_path_name = "schemas"


class ExternalSnowflakeGenerator(DeepLvlGenerator):
    generator_cls = SnowflakeGenerator
    database_path_name = "databases"
    schema_path_name = "schemas"
