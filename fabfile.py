import os, re
import datetime
from functools import wraps
from contextlib import contextmanager

from fabric.api import env, cd, prefix, sudo as _sudo, run as _run, hide
from fabric.contrib.files import exists, upload_template
from fabric.colors import yellow, green, blue, red
from fabric.tasks import Task
from hosts import *

class PlatformSettings(Task):
    def __init__(self, name, platform, *args, **kwargs):
        super(PlatformSettings, self).__init__(*args, **kwargs)
        self.name = name
        self.platform = platform

    def run(self, *args, **kwargs):
        # set this platform's attributes as fabric environment variables
        settings = ["hosts", "user", "repo_url"]
        # set the platform name from gsettings
        setattr(env, "target_platform", self.name)

        for setting in settings:
            setattr(env, setting, self.platform.get(setting, None))
            #Reset the host_config to wipe out any changes from the previous platforms
        env.host_config = {}
        for key, value in PLATFORMS[self.name].items():
            env.host_config[key] = value

# for each platform in gsettings create a task with the platforms name
for key, value in PLATFORMS.items():
    setattr(__import__(__name__), key, PlatformSettings(key, value))

######################################
# Context for virtualenv and project #
######################################

@contextmanager
def virtualenv():
    """
    Run commands within the project's virtualenv.
    """
    with cd(env.host_config["setmaster_venv_dir"]):
        with prefix("source %s/bin/activate" % env.host_config["setmaster_venv_dir"]):
            yield


@contextmanager
def project():
    """
    Run commands within the project's directory.
    """
    with virtualenv():
        with cd(env.host_config["setmaster_top_dir"]):
            yield


###########################################
# Utils and wrappers for various commands #
###########################################

def _print(output):
    print
    print output
    print


def print_command(command):
    _print(blue("$ ", bold=True) +
           yellow(command, bold=True) +
           red(" ->", bold=True))


@task
def run(command, show=True):
    """
    Run a shell comand on the remote server.
    """
    if show:
        print_command(command)
    with hide("running"):
        return _run(command)


@task
def sudo(command, show=True):
    """
    Run a command as sudo.
    """
    if show:
        print_command(command)
    with hide("running"):
        return _sudo(command)


def log_call(func):
    @wraps(func)
    def logged(*args, **kawrgs):
        header = "-" * len(func.__name__)
        _print(green("\n".join([header, func.__name__, header]), bold=True))
        return func(*args, **kawrgs)
    return logged


def get_templates():
    """
    Return each of the templates with env vars injected
        """
    injected = {}
    for name, data in templates.items():
        injected[name] = dict([(k, v % env) for k, v in data.items()])
    return injected


def upload_template_and_reload(name):
    """
    Upload a template only if it has changed, and if so, reload a
    related service.
    """
    template = get_templates()[name]
    local_path = template["local_path"]
    remote_path = template["remote_path"]
    reload_command = template.get("reload_command")
    owner = template.get("owner")
    mode = template.get("mode")
    remote_data = ""
    if exists(remote_path):
        with hide("stdout"):
            remote_data = sudo("cat %s" % remote_path, show=False)
    with open(local_path, "r") as f:
        local_data = f.read()
        # Escape all non-string-formatting-placeholder occurrences of '%':
        local_data = re.sub(r"%(?!\(\w+\)s)", "%%", local_data)
        if "%(db_pass)s" in local_data:
            env.db_pass = db_pass()
        local_data %= env
    clean = lambda s: s.replace("\n", "").replace("\r", "").strip()
    if clean(remote_data) == clean(local_data):
        return
    upload_template(local_path, remote_path, env, use_sudo=True, backup=False)
    if owner:
        sudo("chown %s %s" % (owner, remote_path))
    if mode:
        sudo("chmod %s %s" % (mode, remote_path))
    if reload_command:
        sudo(reload_command)


def db_pass():
    """
    Prompt for the database password if unknown.
    """
    return env.db_pass


@task
def apt(packages):
    """
    Install one or more system packages via apt.
    """
    return sudo("apt-get install -y -q " + packages)


@task
def pip(packages):
    """
    Install one or more Python packages within the virtual environment.
    """
    with virtualenv():
        return run("pip install %s" % packages)


def postgres(command):
    """
    Runs the given command as the postgres user.
    """
    show = not command.startswith("psql")
    return run("sudo -u root sudo -u postgres %s" % command, show=show)


@task
def psql(sql, show=True):
    """
    Run SQL against the project's database.
    """
    out = run('mysql -uroot -e "%s"' % sql, show=False)
    if show:
        print_command(sql)
    return out


@task
def backup(filename):
    """
    Backs up the database.
    """
    return postgres("pg_dump -Fc %s > %s" % (env.proj_name, filename))


@task
def restore(filename):
    """
    Restores the database.
    """
    return postgres("pg_restore -c -d %s %s" % (env.proj_name, filename))

@task
def manage(command):
    """
    Run a Django management command.
    """
    with virtualenv():
        puts("%s/manage.py %s" % (env.host_config["setmaster_code_dir"], command))
        return run("%s/manage.py %s" % (env.host_config["setmaster_code_dir"], command))


#########################
# Install and configure #
#########################

@task
@log_call
def install():
    """
    Install the base system-level and Python requirements for the
    entire server.
    """
    locale = "LC_ALL=%s" % env.locale
    with hide("stdout"):
        if locale not in sudo("cat /etc/default/locale"):
            sudo("update-locale %s" % locale)
            run("exit")
    sudo("apt-get update -y -q")
    apt("nginx libjpeg-dev python-dev python-setuptools git-core "
        "mysql-server mysql-client libmysqlclient-dev libpq-dev memcached supervisor python-virtualenv")
    sudo("usermod -a -G www-data %s" % env.user)
    with settings(warn_only=True):
        sudo("mkdir /var/www")
        sudo("mkdir %s/logs" % env.host_config["setmaster_venv_dir"])
    set_static_permissions()


@task
@log_call
def create():
    """
    Create a virtual environment, pull the project's repo from
    version control, add system-level configs for the project,
    and initialise the database with the live host.
    """

    # Create virtualenv
    with cd(env.venv_home):
        if exists(env.proj_name):
            prompt = raw_input("\nVirtualenv exists: %s\nWould you like "
                               "to replace it? (yes/no) " % env.proj_name)
            if prompt.lower() != "yes":
                print "\nAborting!"
                return False
            remove()
        run("virtualenv %s --distribute" % env.proj_name)
        vcs = "git" if env.repo_url.startswith("git") else "hg"
        run("%s clone %s %s" % (vcs, env.repo_url, env.host_config["setmaster_top_dir"]))

    # Create DB and DB user.
    pw = db_pass()
    user_sql_args = (env.proj_name, pw.replace("'", "\'"))
    user_sql = "CREATE USER '%s'@'%%' IDENTIFIED BY '%s';" % user_sql_args
    with settings(warn_only=True):
        # user must already exist
        psql(user_sql, show=False)
    shadowed = "*" * len(pw)
    print_command(user_sql.replace("'%s'" % pw, "'%s'" % shadowed))

    with settings(warn_only=True):
        # user must already exist
        psql("CREATE DATABASE %s" % env.proj_name)
    psql("GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost';" % (env.proj_name, env.proj_name))

    # Set up project.
    upload_template_and_reload("settings")

    with virtualenv():
        run("easy_install -U distribute")

    if env.reqs_path:
        pip("-r %s/%s" % (env.host_config["setmaster_top_dir"], env.reqs_path))
    pip("gunicorn setproctitle south "
        "django-compressor python-memcached")
    manage("createdb --noinput")
    if env.admin_pass:
        pw = env.admin_pass
        user_py = ("from django.contrib.auth.models import User;"
                   "u, _ = User.objects.get_or_create(username='admin');"
                   "u.is_staff = u.is_superuser = True;"
                   "u.set_password('%s');"
                   "u.save();" % pw)
        shadowed = "*" * len(pw)
        print_command(user_py.replace("'%s'" % pw, "'%s'" % shadowed))

    return True


@task
@log_call
def remove():
    """
    Blow away the current project.
    """
    if exists(env.host_config["setmaster_venv_dir"]):
        sudo("rm -rf %s" % env.host_config["setmaster_venv_dir"])
    for template in get_templates().values():
        remote_path = template["remote_path"]
        if exists(remote_path):
            sudo("rm %s" % remote_path)
    with settings(warn_only=True):
        # its ok if database and/or user already exist
        psql("DROP DATABASE %s;" % env.proj_name)
    with settings(warn_only=True):
        psql("DROP USER %s;" % env.proj_name)

##############
# Deployment #
##############

@task
@log_call
def restart():
    """
    Restart gunicorn worker processes for the project.
    """
    pid_path = "%s/gunicorn.pid" % env.host_config["setmaster_code_dir"]
    if exists(pid_path):
        sudo("kill -HUP `cat %s`" % pid_path)
    else:
        sudo("supervisorctl restart setmaster:*")


@task
@log_call
def deploy():
    """
    Deploy latest version of the project.
    Check out the latest version of the project from version
    control, install new requirements, sync and migrate the database,
    collect any new static assets, and restart gunicorn's work
    processes for the project.
    """
    if not exists(env.host_config["setmaster_venv_dir"]):
        prompt = raw_input("\nVirtualenv doesn't exist: %s\nWould you like "
                           "to create it? (yes/no) " % env.proj_name)
        if prompt.lower() != "yes":
            print "\nAborting!"
            return False
        create()
    #for name in get_templates():
    #    upload_template_and_reload(name)
    with project():
        run("git pull -f")
        pip("-r %s/requirements/project.txt" % (env.host_config["setmaster_top_dir"]))
        manage("syncdb --noinput")
        migrate()
        manage("collectstatic -v 0 --noinput")
        set_static_permissions()
    restart()
    return True

def collect_static():
    manage("collectstatic -v 0 --noinput")
    set_static_permissions()

def migrate():
    with project():
        manage("migrate --noinput")


@task
@log_call
def all():
    """
    Installs everything required on a new system and deploy.
    From the base software, up to the deployed project.
    """
    install()
    if create():
        deploy()

@task
def push_branch(branch=None):
    if branch is None:
        branch = "master"
    with cd(env.host_config["setmaster_top_dir"]):
        run("git fetch")
        run("git checkout %s" % branch)
        run("git pull")
    restart()

@task
def restore_database(password=None):
    with cd(env.host_config["setmaster_top_dir"]):
        psql("DROP DATABASE %s" % env.proj_name)
        psql("CREATE DATABASE %s" % env.proj_name)
        run("mysql -u%s -p%s %s < setmaster_dump.sql" % (env.db_username, env.db_pass, env.proj_name))

@task
def pull_backup(password=None):
    with cd(env.host_config["setmaster_top_dir"]):
        run("mysqldump -u%s -p%s %s > setmaster_dump.sql" % (env.db_username, env.db_pass, env.proj_name))
        get("setmaster_dump.sql", ".")
        run("git checkout setmaster_dump.sql")

@task
def set_static_permissions():
    sudo("chown -R www-data:www-data /var/www")
    sudo("chmod g+rwx -R /var/www")

@task
def gen_bootstrap():
    with project():
        run("lessc --compress lib/bootstrap/bootstrap.less > newnet_theme/static/css/bootstrap.min.css")

@task
def get_statics():
    local("rsync --progress -avzr {0}@setmaster.pt:/var/www/setmaster_static/media/ static/media/".format(env.host_config["user"]))

@task
def update_machine():
    if not exists("/usr/bin/puppet"):
        execute(install_puppet)
    execute(push_host_config)
    execute(update_puppet_manifest)
    execute(puppet_update)

@task
def update_puppet_manifest():
    """ Push puppet manifests to host """
    local("tar zcf nlpuppet.tgz puppet")
    put("nlpuppet.tgz", "/tmp")
    local("rm nlpuppet.tgz")
    sudo("rm -Rf /etc/puppet")
    sudo("cd /etc/; tar zxf /tmp/nlpuppet.tgz")
    sudo("rm /tmp/nlpuppet.tgz")

@task
def puppet_update(debug=False):
    """ Apply a puppet manifest """
    flags = "--verbose --environment setmaster"
    if debug:
        flags += ' --debug'
    sudo("puppet apply {flags} /etc/puppet/environments/setmaster/manifests/site.pp".format(**locals()))

@task
def install_puppet():
    """ Perform initial config on a host that has had the following done to it::

    + installation of base OS
    + SSH installed
    + administrator account created; SSH public key installed
    """
    require("host")
    with settings(warn_only=True):
        sudo("apt-get update -y")
    sudo("apt-get upgrade -y")
    sudo("apt-get install -y python-software-properties")

    #install key for the puppetlabs repo
    sudo("gpg --homedir=/root --keyserver=keys.gnupg.net --recv-key 4BD6EC30")
    sudo("gpg --homedir=/root -a --export 4BD6EC30 > /tmp/puppet.key")
    sudo("apt-key add /tmp/puppet.key")
    sudo("rm /tmp/puppet.key")
    sources_file = "/etc/apt/sources.list.d/puppetlabs.list"
    if not exists(sources_file, use_sudo=True):
        sudo("echo \"deb http://apt.puppetlabs.com oneiric main\" > {sources_file}".format(**locals()))
        sudo("echo \"deb-src http://apt.puppetlabs.com oneiric main\" >> {sources_file}".format(**locals()))

    with settings(warn_only=True):
        sudo("apt-get update -y")
        # ensure that latest version is installed if an older one already on
    # the host
    sudo("apt-get install -y puppet -o DPkg::Options=\"-force-confold\"")
    sudo("apt-get upgrade -y puppet")

@task
def push_host_config(ofile=None):
    """ If ofile is set to a path the config is created at that point and
not pushed to the remote machines. This mode is for testing only. """
    if ofile:
        TESTING = True
    else:
        TESTING = False
        ofile = '/tmp/host_config'

    if not env.has_key("host_config"):
        raise Exception("no host_conf settings made")

    o = open(ofile, 'wt')
    o.write("# AUTO GENERATED ON DEPLOY\n")
    o.write("# %s\n" % datetime.datetime.now().strftime("%m %b %Y %H:%M:%S"))

    for k, v in env.host_config.items():
        o.write("%s %s\n" % (k, v))

    o.close()

    if not TESTING:
        put(ofile, "/etc/default/setmasterserver.conf", use_sudo=True)
        os.remove(ofile)
