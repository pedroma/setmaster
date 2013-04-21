class setmaster {

    include nginx
    include supervisor
    include ssh

	file { "/etc/nginx/sites-enabled/setmaster.conf":
        notify => Service["nginx"],
        ensure => file,
        owner => www-data,
        group => www-data,
        content => template("setmaster/setmaster.conf.erb")
	}

    file { "/etc/supervisor/conf.d/setmaster.conf":
        notify => Service["supervisor"],
        ensure => file,
        owner => root,
        group => root,
        content => template("setmaster/supervisor.conf.erb")
    }

    file { "/etc/nginx/htaccess":
        ensure => file,
        owner => root,
        group => root,
        require => Package["nginx"],
        source => "puppet:///modules/setmaster/htaccess",
    }

    file { "${sm_setmaster_code_dir}/${sm_project_name}/local_settings.py":
        content => template("setmaster/local_settings.py.erb"),
        ensure => file,
        owner => $sm_user,
        group => $sm_user,
    }

    file { "${sm_setmaster_code_dir}/wsgi.py":
        content => template("setmaster/wsgi.erb"),
        ensure => file,
        owner => $sm_user,
        group => $sm_user,
    }

    file { "${sm_setmaster_top_dir}/newrelic.ini":
        source => "puppet:///modules/setmaster/newrelic.ini",
        ensure => file,
        owner => $sm_user,
        group => $sm_user,
    }

    file { "/home/${sm_user}/.ssh/authorized_keys":
        source => "puppet:///modules/setmaster/authorized_keys",
        ensure => file,
        owner => $sm_user,
        group => $sm_user,
    }


    file { "/etc/crontabs":
        ensure => directory,
        owner => root,
        group => root,
    }

    file { "/etc/crontabs/${sm_user}":
        content => template("setmaster/crontab"),
        ensure => file,
        owner => root,
        group => root,
        require => File["/etc/crontabs"],
    }

    file { "/etc/sudoers.d/${sm_user}":
        content => template("setmaster/sudoers"),
        ensure => file,
        owner => root,
        group => root,
        mode => 0440,
    }

    file { "${sm_setmaster_static_dir}":
       ensure => directory,
       owner => $sm_user,
       group => $sm_user,
       mode => 0777,
    }
}
