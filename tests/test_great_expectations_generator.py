from oddrn_generator.generators import GreatExpectationsGenerator


def test_great_expectations_generator():
    generator = GreatExpectationsGenerator(
        host_settings="local", suites="suite", types="value_in_set", runs="23012023"
    )
    assert (
        generator.get_oddrn_by_path("runs")
        == "//great_expectations/host/local/suites/suite/types/value_in_set/runs/23012023"
    )
