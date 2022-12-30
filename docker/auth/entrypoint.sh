#!/bin/bash

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

ip route del default
ip route add default via 10.0.2.2 dev eth0 

# Aceptar TCP que venga del broker y del files
iptables -A INPUT -s 10.0.1.4 -p tcp --dport 5000 -j ACCEPT
iptables -A INPUT -s 10.0.2.4 -p tcp --sport 5000 -j ACCEPT
iptables -A INPUT -s 10.0.2.4 -p tcp --dport 5000 -j ACCEPT

service ssh start
service rsyslog start

iptables -A INPUT ! -s 10.0.3.3 -p icmp --dport 22 -j DROP
iptables -A INPUT ! -s 10.0.3.3 -p icmp --sport 22 -j DROP


./apiAuth.py

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
