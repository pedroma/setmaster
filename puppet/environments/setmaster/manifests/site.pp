import "classes/*.pp"

node default {
}

node base_setmaster inherits default {
    include setmaster
    include log_files
}

node 'nw.peddan.com' inherits base_setmaster {
}

