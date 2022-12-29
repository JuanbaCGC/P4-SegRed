#!/bin/bash

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

# Aceptar lo que venga de la interfaz de fuera
iptables -A INPUT -i eth0 -p tcp --dport 5000 -j ACCEPT
iptables -A INPUT -s 10.0.2.3 -p tcp --dport 5000 -j ACCEPT
iptables -A INPUT -s 10.0.2.3 -p tcp --sport 5000 -j ACCEPT
iptables -A INPUT -s 10.0.2.4 -p tcp --dport 5000 -j ACCEPT
iptables -A INPUT -s 10.0.2.4 -p tcp --sport 5000 -j ACCEPT

ip route del default
ip route add default via 10.0.1.2 dev eth0 

service ssh start
service rsyslog start

./apiBroker.py

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi