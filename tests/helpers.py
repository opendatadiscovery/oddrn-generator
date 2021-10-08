

def create_paths_oddrn(generator, generator_settings, target):
    aliases = generator_settings['aliases']
    paths = generator_settings['paths']
    path_dict = {}
    for dep in generator.paths_obj.__config__.dependencies_map[target]:
        path_dict[aliases.get(dep, dep)] = paths[dep]
    return path_dict


def create_host_oddrn_string(generator, generator_settings, target):
    host = generator_settings['host_settings']
    path_dict = create_paths_oddrn(generator, generator_settings, target)
    return f"//{generator.source}/host/{host}/" + '/'.join([f'{k}/{v}' for k, v in path_dict.items()])


def create_cloud_oddrn_string(generator, generator_settings, target):
    cloud_str = f'cloud/aws/' + '/'.join([f'{k}/{v}' for k, v in generator_settings['cloud_settings'].items()])
    path_dict = create_paths_oddrn(generator, generator_settings, target)
    return f"//{generator.source}/{cloud_str}/" + '/'.join([f'{k}/{v}' for k, v in path_dict.items()])
