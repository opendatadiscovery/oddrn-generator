from oddrn_generator.generators import PostgresqlGenerator, GlueGenerator, TableauGenerator, AirflowGenerator, PrefectGenerator


def postgres_generator_example():
    postgres = PostgresqlGenerator(
        host_settings='127.0.0.1:5034',
        schemas='some_schema', databases='some_database', tables='some_table', columns='some_column'
    )
    print(postgres.get_oddrn_by_path("schemas"))
    print(postgres.get_oddrn_by_path("databases"))
    print(postgres.get_oddrn_by_path("tables"))
    print(postgres.get_oddrn_by_path("columns"))

    print(postgres.get_oddrn_by_path("schemas", "another_schema"))
    print(postgres.get_oddrn_by_path("columns"), "another_column")
    print(postgres.get_data_source_oddrn())
    print()
    postgres2 = PostgresqlGenerator(
        host_settings='127.0.0.1:5034',
        schemas='some_schema', databases='some_database',
    )
    postgres2.set_oddrn_paths(tables='newnewnew', columns='asjsjsjsj')
    print(postgres2.get_oddrn_by_path("tables"))
    print(postgres2.get_oddrn_by_path("columns"))
    print(postgres2.get_oddrn_by_path("columns", 'asdsadsddddddddd'))
    print()


def glue_generator_example():
    glue = GlueGenerator(
        cloud_settings={
            'account': '21232132',
            'region': 'us-west'
        },
        databases='some_database',
        tables='some_table',
        columns='some_column',
        jobs='some_job',
        owners='some_owner'
    )
    print(glue.get_oddrn_by_path("databases"))
    print(glue.get_oddrn_by_path("tables"))
    print(glue.get_oddrn_by_path("columns"))
    print(glue.get_oddrn_by_path("jobs"))
    print(glue.get_oddrn_by_path("owners"))
    print(glue.get_data_source_oddrn())

    print()
    print(glue.get_oddrn_by_path(path="databases", new_value="new_db"))
    print(glue.get_oddrn_by_path(path="tables", new_value="new_table"))
    print(glue.get_oddrn_by_path(path="columns", new_value="new_column"))
    print(glue.get_oddrn_by_path(path="jobs", new_value="new_job"))
    print(glue.get_oddrn_by_path(path="owners", new_value="new_owner"))
    print(glue.get_oddrn_by_path(path="columns", new_value="11111"))
    print()

    glue2 = GlueGenerator(
        cloud_settings={
            'account': '21232132',
            'region': 'us-west',
        },
        databases='some_database', tables='some_table', columns='some_column', jobs='some_job'
    )
    print(glue2.get_oddrn_by_path("jobs"))
    print(glue2.get_oddrn_by_path("columns"))
    print(glue2.get_oddrn_by_path("columns", "another_column"))
    print()


def tableau_generator_example():
    tableau = TableauGenerator(
        host_settings='dub01.online.tableau.com',
        sites='some_site',
        databases='some_database',
        schemas='some_schema',
        tables='some_table',
        columns='some_column',
        workbooks='some_workbook',
        sheets='some_sheet'
    )
    print(tableau.get_oddrn_by_path("databases"))
    print(tableau.get_oddrn_by_path("schemas"))
    print(tableau.get_oddrn_by_path("tables"))
    print(tableau.get_oddrn_by_path("columns"))
    print(tableau.get_oddrn_by_path("workbooks"))
    print(tableau.get_oddrn_by_path("sheets"))
    print(tableau.get_data_source_oddrn())

    print()

    tableau_no_schema = TableauGenerator(
        sites='some_site',
        host_settings='dub01.online.tableau.com',
        databases='some_database',
        tables='some_table',
        columns='some_column',
    )

    print(tableau_no_schema.get_oddrn_by_path("tables"))
    print(tableau_no_schema.get_oddrn_by_path("columns"))
    print()


def airflow_generator_example():
    airflow = AirflowGenerator(
        host_settings='hostname.airflow.com',
        dags='some_dag',
        runs='some_run',
        tasks='some_task',
    )
    print(airflow.get_oddrn_by_path("dags"))
    print(airflow.get_oddrn_by_path("runs"))
    print(airflow.get_oddrn_by_path("tasks"))
    print(airflow.get_data_source_oddrn())

    print()

def prefect_generator_example():
    prefect = PrefectGenerator(
        host_settings='hostname.prefect.com',
        flows='some_flow',
        runs='some_run',
        tasks='some_task',
    )
    print(prefect.get_oddrn_by_path("flows"))
    print(prefect.get_oddrn_by_path("runs"))
    print(prefect.get_oddrn_by_path("tasks"))
    print(prefect.get_data_source_oddrn())

    print()
# def ge_generator_example():
#     ge = GreatExpectationsGenerator(
#         cloud_settings={
#             'account': '21232132',
#             'region': 'us-west',
#         },
#         runs='some_runs',
#         suits='some_suits',
#         runs_types='some_runs_types',
#         suits_types='some_suits_types',
#     )
#     for path in ge.available_paths:
#         print(ge.get_oddrn_by_path(path))
#     ge.set_oddrn_paths(runs_types='another_runs_type', suits_types='another_suits_types')
#     print(ge.get_oddrn_by_path('runs_types'))
#     print(ge.get_oddrn_by_path('suits_types'))
#
#     print(ge.get_oddrn_by_path('suits_types', 'asdsa'))
#     print(ge.get_oddrn_by_path('runs_types'))
#     print(ge.get_oddrn_by_path('suits_types'))


if __name__ == "__main__":
    postgres_generator_example()
    glue_generator_example()
    tableau_generator_example()
    airflow_generator_example()
    # ge_generator_example()

