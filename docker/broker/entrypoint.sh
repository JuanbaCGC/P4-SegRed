#!/bin/bash

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

ip route del default
ip route add default via 10.0.1.2 dev eth0 

service ssh start
service rsyslog start

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
