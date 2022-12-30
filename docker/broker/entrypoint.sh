#!/bin/bash

iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

#iptables -A INPUT -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT

# Aceptar lo que venga del router
iptables -A INPUT -s 10.0.1.2 -p tcp --dport 5000 -j ACCEPT


ip route del default
ip route add default via 10.0.1.2 dev eth0 

service ssh start
service rsyslog start

iptables -A INPUT ! -s 10.0.3.3 -p icmp --dport 22 -j DROP
iptables -A INPUT ! -s 10.0.3.3 -p icmp --sport 22 -j DROP

./home/api/apiBroker.py

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
