from oddrn_generator.generators import CubeJsGenerator


def test_cubejs_generator():
    generator = CubeJsGenerator(host_settings="localhost")
    generator.set_oddrn_paths(cubes="my_cube")

    assert generator.get_data_source_oddrn() == "//cubejs/host/localhost"
    assert (
        generator.get_oddrn_by_path("cubes") == "//cubejs/host/localhost/cubes/my_cube"
    )
