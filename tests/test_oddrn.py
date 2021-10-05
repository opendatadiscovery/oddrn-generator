import datetime

import pytest
from pydantic import ValidationError

from oddrn.exceptions import WrongPathOrderException, PathDoestExistException, EmptyPathValueException
from tests.helpers import create_host_oddrn_string, create_cloud_oddrn_string
from tests.models import example_generator_settings, ExampleGenerator
from tests.params import parameters_host, parameters_cloud


def check_host_oddrn_paths(gen, settings, path):
    custom_oddrn = create_host_oddrn_string(gen, settings, path)
    generator_oddrn = gen.get_oddrn_by_path(path)
    print()
    print(f"custom_oddrn    = {custom_oddrn}")
    print(f"generator_oddrn = {generator_oddrn}")
    assert custom_oddrn == generator_oddrn


def check_cloud_oddrn_paths(gen, settings, path):
    custom_oddrn = create_cloud_oddrn_string(gen, settings, path)
    generator_oddrn = gen.get_oddrn_by_path(path)
    print()
    print(f"custom_oddrn    = {custom_oddrn}")
    print(f"generator_oddrn = {generator_oddrn}")
    assert custom_oddrn == generator_oddrn


def test_example_generator():
    settings = example_generator_settings
    example_gen = ExampleGenerator(host_settings=example_generator_settings['host_settings'], **settings['paths'])

    # check data source oddrn
    assert example_gen.get_data_source_oddrn()

    # check oddrn parts
    for p in example_gen.available_paths:
        check_host_oddrn_paths(example_gen, settings, p)

    # check change oddrn
    new_path = {'field_1': 'another_field_1'}
    settings['paths'].update(new_path)
    example_gen.set_oddrn_paths(**new_path)
    for p in example_gen.available_paths:
        check_host_oddrn_paths(example_gen, settings, p)

    # check get and update path
    new_path = {'field_3': 'another_field_3'}
    settings['paths'].update(new_path)
    assert create_host_oddrn_string(example_gen, settings, 'field_3') == \
           example_gen.get_oddrn_by_path('field_3', 'another_field_3')

    # check not existing paths
    with pytest.raises(PathDoestExistException):
        example_gen.get_oddrn_by_path("wrong_path")

    # create new generator with empty values
    settings['paths'].pop('field_4')
    settings['paths'].pop('field_5_1')
    settings['paths'].pop('field_5_2')
    test_gen_empty_fields = ExampleGenerator(
        host_settings=settings['host_settings'], **settings['paths']
    )
    # check empty path values
    with pytest.raises(EmptyPathValueException):
        test_gen_empty_fields.get_oddrn_by_path("field_4")
        test_gen_empty_fields.get_oddrn_by_path("field_5_1")
        test_gen_empty_fields.get_oddrn_by_path("field_5_2")

    # test that not empty path works
    check_host_oddrn_paths(example_gen, settings, 'field_3')

    # check wrong path order
    new_path = {'field_5_1': 'new_field_5_1'}
    with pytest.raises(WrongPathOrderException):
        test_gen_empty_fields.set_oddrn_paths(**new_path)

    # check require path
    settings['paths'].pop("field_2")
    with pytest.raises(ValidationError):
        ExampleGenerator(
            host_settings=settings['host_settings'], **settings['paths']
        )

    # check data types
    settings['paths']['field_2'] = datetime.datetime.now()
    with pytest.raises(ValidationError):
        ExampleGenerator(
            host_settings=settings['host_settings'], **settings['paths']
        )

    # check extra field types
    settings['paths']['extra_filed'] = 'some_extra_field'
    with pytest.raises(ValidationError):
        ExampleGenerator(
            host_settings=settings['host_settings'], **settings['paths']
        )


@pytest.mark.parametrize('generator_class, settings', parameters_host)
def test_hostname_generators(generator_class, settings):
    gen = generator_class(host_settings=settings['host_settings'], **settings['paths'])
    # check oddrn parts
    for p in gen.available_paths:
        check_host_oddrn_paths(gen, settings, p)
    assert gen.get_data_source_oddrn()


@pytest.mark.parametrize('generator_class, settings', parameters_cloud)
def test_cloud_generators(generator_class, settings):
    gen = generator_class(cloud_settings=settings['cloud_settings'], **settings['paths'])
    # check oddrn parts
    for p in gen.available_paths:
        check_cloud_oddrn_paths(gen, settings, p)
    assert gen.get_data_source_oddrn()
