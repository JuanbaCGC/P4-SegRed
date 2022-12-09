#!bin/bash

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -i icmp -j ACCEPT

iptables -A INPUT -p tcp --dport 22 -s 10.0.1.2 -j ACCEPT # router
iptables -A INPUT -p tcp --dport 22 -s 10.0.3.3 -j ACCEPT # work
#iptables -A INPUT -p tcp --dport 22 -s 10.0.3.0/24 -j ACCEPT
iptables -A INPUT -p tcp --sport 22 -s 10.0.3.0/24 -j ACCEPT # desde la red de work

service ssh start

ip route del default
ip route add default via 10.0.1.2 dev eth0

if [ -z "@" ]; then
	exec /bin/bash
else
	exec $@
fi