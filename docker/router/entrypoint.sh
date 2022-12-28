#!/bin/bash

echo 1 > /proc/sys/net/ipv4/ip_forward

iptables -P INPUT DROP
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT

iptables -A INPUT -p icmp -j ACCEPT
iptables -A FORWARD -p icmp -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -p icmp -j MASQUERADE

iptables -A FORWARD -i eth0 -o eth1 -p tcp --syn --dport 22 -m state --state NEW -j ACCEPT
iptables -A FORWARD -i eth0 -o eth1 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 22 -j DNAT --to-destination 10.0.1.3
iptables -t nat -A POSTROUTING -o eth1 -p tcp --dport 22 -s 172.17.0.0/16 -d 10.0.1.3 -j SNAT --to-source 10.0.1.2

iptables -A FORWARD -i eth1 -o eth2 -p tcp --dport 22 -j ACCEPT
iptables -A FORWARD -i eth2 -o eth1 -p tcp --sport 22 -j ACCEPT
iptables -A FORWARD -i eth2 -o eth1 -p tcp --dport 22 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth2 -p tcp --sport 22 -j ACCEPT

iptables -A INPUT -p tcp --dport 22 -i eth2 -s 10.0.3.3 -j ACCEPT

# Aceptar http del broker
iptables -A INPUT -p tcp --sport 5000 -s 10.0.1.4 -j ACCEPT
iptables -A FORWARD -s 10.0.1.4 -d 10.0.2.0/24 -j ACCEPT


iptables -A INPUT -p tcp --sport 5000 -s 10.0.2.3 -j ACCEPT

# #Redirigir las peticiones del broker al auth
# iptables -t nat -A PREROUTING -p tcp -s 10.0.1.4 --sport 5000 -j DNAT --to-destination 10.0.2.0/24
# iptables -t nat -A POSTROUTING -p tcp --dport 5000 -s 10.0.1.4 -d 10.0.2.0/24 -j SNAT --to-source 10.0.1.4

service ssh start
service rsyslog start

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
