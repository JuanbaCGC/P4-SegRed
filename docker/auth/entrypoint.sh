#!/bin/bash

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

ip route del default
ip route add default via 10.0.2.2 dev eth0 

iptables -A INPUT -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT

# Aceptar TCP que venga del broker y del files
iptables -A INPUT -s 10.0.1.4 -p tcp --dport 5000 -j ACCEPT
iptables -A INPUT -s 10.0.2.4 -p tcp --dport 5000 -j ACCEPT
iptables -A INPUT -s 10.0.1.2 -p tcp --dport 5000 -j ACCEPT

#iptables -A INPUT -p tcp -s 10.0.1.0/24 -j ACCEPT


service ssh start
service rsyslog start

./home/api/apiAuth.py

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi