from oddrn_generator.generators import ApiGenerator


def test_api_generator():
    test_host_name = "www.test_host.com"
    test_resource_name = "test_resource"
    test_field_name = "test_field"

    generator = ApiGenerator(
        host_settings=test_host_name,
        resources=test_resource_name,
        fields=test_field_name,
    )
    assert generator.get_data_source_oddrn() == f"//api/host/{test_host_name}"
    assert (
        generator.get_oddrn_by_path("resources")
        == f"//api/host/{test_host_name}/resources/{test_resource_name}"
    )
    assert (
        generator.get_oddrn_by_path("fields")
        == f"//api/host/{test_host_name}/resources/{test_resource_name}/fields/{test_field_name}"
    )

    test_resource_name_2 = "test_resource_2"
    test_field_name_2 = "test_field_2"
    generator.set_oddrn_paths(resources=test_resource_name_2, fields=test_field_name_2)
    assert (
        generator.get_oddrn_by_path("fields")
        == f"//api/host/{test_host_name}/resources/{test_resource_name_2}/fields/{test_field_name_2}"
    )
