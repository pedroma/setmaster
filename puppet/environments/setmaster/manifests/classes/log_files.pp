class log_files {

    file { "/var/log/setmaster-gunicorn.log":
        ensure => present,
        mode => 0777,
    }

}
