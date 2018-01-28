#!/bin/bash

db_conf()
{
    sed -i "s/database01/$database01/g" /etc/my.cnf.d/server_cluster.cnf
    sed -i "s/database02/$database02/g" /etc/my.cnf.d/server_cluster.cnf
    sed -i "s/database03/$database03/g" /etc/my.cnf.d/server_cluster.cnf
}

db_install()
{
    if [ ! -d '/database/mysql' ]; then
        mkdir -p /database/mysql &&
        chown mysql:mysql /database/mysql
    fi

    sleep 1s

    if [ ! -d '/database/mysql/mysql' ]; then
        /usr/bin/mysql_install_db --user=mysql
    fi
}

db_start()
{
    port_ch01=$(echo 'quit' | timeout -s 9 3s telnet "$database01" 3306 | grep -w 'Connected' | wc -l)
    port_ch02=$(echo 'quit' | timeout -s 9 3s telnet "$database02" 3306 | grep -w 'Connected' | wc -l)
    port_ch03=$(echo 'quit' | timeout -s 9 3s telnet "$database03" 3306 | grep -w 'Connected' | wc -l)
    if [ $port_ch01 -eq 0 ] && [ $port_ch02 -eq 0 ] && [ $port_ch03 -eq 0 ]; then
        /usr/sbin/mysqld --wsrep-new-cluster --user=mysql &>> /var/log/MariaDB.log &
    else
        /usr/sbin/mysqld --user=mysql &
    fi
}

db_init()
{
    bash /run/console/mysql_secure_installation
}

main()
{
    db_conf
    db_install

    sleep 2s

    db_start

    sleep 10s

    db_init
}

main

