from oddrn_generator.generators import MetabaseGenerator


def test_metabase_generator():
    generator = MetabaseGenerator(host_settings="host")
    generator.set_oddrn_paths(collections="1", dashboards="1")

    assert generator.get_data_source_oddrn() == "//metabase/host/host"

    assert (
        generator.get_oddrn_by_path("dashboards")
        == "//metabase/host/host/collections/1/dashboards/1"
    )

    generator.set_oddrn_paths(cards="2")
    assert (
        generator.get_oddrn_by_path("cards")
        == "//metabase/host/host/collections/1/cards/2"
    )
