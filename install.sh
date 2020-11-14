#!/bin/bash

if [ -n "$(command -v yum)" ]
then
    sudo yum update -y
    sudo yum install -y traceroute whois curl python3
    echo "installing traceroute whois curl python3"
elif [ -n "$(command -v apt)" ]
then
    sudo apt update -y
    sudo apt install -y traceroute whois curl python3
    echo "installing traceroute whois curl python3"
else
    >&2 echo "this os not support"
    exit 1
fi

if [ -n "$(command -v python3)" ]
then
    wget -O app.py https://raw.githubusercontent.com/arminmokri/derakintership/main/app.py
    sudo cp app.py /bin/app.py
    sudo chmod +x /bin/app.py
    rm app.py
    echo "injoy this app by typing app.py"
fi
