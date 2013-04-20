from fabric.api import *

PLATFORMS = {}
PLATFORM_DEFAULTS = {
    "authmode": "open",
    "debug": "off",
    "log_dir": "/var/log/",
    "mysql_database_name": "setmaster",
    "user": "setmaster",
    "db_pass": "root",
    "site_id": 2,
    "db_username": "root",
    "project_name": "setmaster",
    "setmaster_repo_url": "git@github.com:pedroma/setmaster.git",
    "gunicorn_port": 8030,
    "setmaster_static_dir": "/var/www/setmaster_static/",
    "setmaster_code_dir": "/home/setmaster/setmaster/setmaster/setmaster",
    "setmaster_top_dir": "/home/setmaster/setmaster/setmaster",
    "setmaster_venv_dir": "/home/setmaster/setmaster",
    "setmaster_nginx_server_name": "mage.peddan.com"
}


def _add_platform(name, mode, **kwargs):
    """
    Add a new platform, using sensible defaults
    :param name: Name of platform to add
    :param mode: The server mode
    :param kwargs: Key/Value pairs of settings to be overridden
    :return: None
    """
    config = PLATFORM_DEFAULTS.copy()
    config['mode'] = mode
    config['platform'] = name
    config.update(kwargs)
    for variable_name in [key for key in config.keys() if key.endswith('_dir')]:
        if not config[variable_name].endswith('/'):
            config[variable_name] += '/'
    PLATFORMS[name] = config

_add_platform(
    'develop', mode='dev', authmode='closed',
    target_platform='develop',
    db_pass="",
    hosts=['nw.peddan.com']
)
