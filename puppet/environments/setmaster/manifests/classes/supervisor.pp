class supervisor {

    package { "supervisor":
        ensure => installed
    }

    service { "supervisor":
        ensure  => "running",
        enable  => "true",
        require => Package["supervisor"],
    }
}
