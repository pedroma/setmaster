class ssh {

    package { "mysql-server":
        ensure => installed
    }

    package { "mysql-client":
        ensure => installed
    }

    service { "mysql":
        ensure  => "running",
        enable  => "true",
        require => Package["mysql-server"],
    }
}
