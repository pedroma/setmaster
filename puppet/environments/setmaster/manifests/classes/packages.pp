class packages {
    include apt

    $package_list = [
        "build-essential",
        "git-core",
        "mongodb"
    ]

    package { $package_list:
        ensure => installed,
    }

    apt::ppa { 'ppa:chris-lea/node.js':
    }

    package { "nodejs":
        ensure => installed,
        require => Apt::Ppa['ppa:chris-lea/node.js'],
    }
}