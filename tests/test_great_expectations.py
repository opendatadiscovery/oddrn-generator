from oddrn_generator.generators import GreatExpectationsGenerator


def test_great_expectations():
    generator = GreatExpectationsGenerator()

    suite_name = "suite"
    expectation_type = "column_not_to_be_null"
    run_id = "42"

    generator.set_oddrn_paths(suites=suite_name, types=expectation_type, runs=run_id)
    assert (
        generator.get_oddrn_by_path("runs")
        == f"//great_expectations/filesystem/suites/{suite_name}/types/{expectation_type}/runs/{run_id}"
    )
