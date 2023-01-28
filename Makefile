key:
	ssh-keygen -t rsa
	cat ${HOME}/.ssh/id_rsa.pub >> docker/assets/authorized_keys.op
	cat ${HOME}/.ssh/id_rsa.pub >> docker/jump/authorized_keys

	cat ${HOME}/.ssh/id_rsa.pub > docker/assets/authorized_keys.dev
	cat ${HOME}/.ssh/id_rsa.pub > docker/assets/authorized_keys.dev.pub
	cat ${HOME}/.ssh/id_rsa.pub > docker/assets/authorized_keys.op.pub
	cat ${HOME}/.ssh/id_rsa.pub > docker/jump/authorized_keys.dev.pub
	cat ${HOME}/.ssh/id_rsa.pub > docker/jump/authorized_keys.dev
	cat ${HOME}/.ssh/id_rsa.pub > docker/jump/authorized_keys.op
	cat ${HOME}/.ssh/id_rsa.pub > docker/jump/authorized_keys.op.pub


DNS:
	if ! grep -q "172.17.0.2 myserver.local" /etc/hosts; then \
		sudo bash -c "echo '172.17.0.2 myserver.local' >> /etc/hosts"; \
	fi

certificates:
	openssl req -x509 -newkey rsa:4096 -nodes -keyout docker/assets/brokerkey.pem -out docker/assets/brokercert.pem -days 365 -subj "/CN=myserver.local"
	openssl req -x509 -newkey rsa:4096 -nodes -keyout docker/assets/authkey.pem -out docker/assets/authcert.pem -days 365 -subj "/CN=10.0.2.3"
	openssl req -x509 -newkey rsa:4096 -nodes -keyout docker/assets/fileskey.pem -out docker/assets/filescert.pem -days 365 -subj "/CN=10.0.2.4"
	
	sudo cp docker/assets/brokercert.pem /usr/local/share/ca-certificates/dockerBroker.crt
	sudo cp docker/assets/authcert.pem /usr/local/share/ca-certificates/dockerAuth.crt
	sudo cp docker/assets/filescert.pem /usr/local/share/ca-certificates/dockerFiles.crt

	cp docker/assets/brokerkey.pem docker/broker/brokerkey.pem
	cp docker/assets/brokercert.pem docker/broker/brokercert.pem
	cp docker/assets/authcert.pem docker/broker/authcert.pem
	cp docker/assets/filescert.pem docker/broker/filescert.pem

	cp docker/assets/authkey.pem docker/auth/authkey.pem
	cp docker/assets/authcert.pem docker/auth/authcert.pem
	cp docker/assets/filescert.pem docker/auth/filescert.pem

	cp docker/assets/fileskey.pem docker/files/fileskey.pem
	cp docker/assets/filescert.pem docker/files/filescert.pem
	cp docker/assets/authcert.pem docker/files/authcert.pem

	sudo update-ca-certificates

build:
	docker build --rm -f docker/Dockerfile --tag midebian docker/
	docker build --rm -f docker/router/Dockerfile --tag midebian-router docker/router
	docker build --rm -f docker/jump/Dockerfile --tag midebian-jump docker/jump
	docker build --rm -f docker/work/Dockerfile --tag midebian-work docker/work
	docker build --rm -f docker/broker/Dockerfile --tag midebian-broker docker/broker
	docker build --rm -f docker/auth/Dockerfile --tag midebian-auth docker/auth
	docker build --rm -f docker/files/Dockerfile --tag midebian-files docker/files

network:
	-docker network create -d bridge --subnet 10.0.1.0/24 dmz
	-docker network create -d bridge --subnet 10.0.3.0/24 dev
	-docker network create -d bridge --subnet 10.0.2.0/24 srv

containers:
	docker run --privileged --rm -ti -d --name router --hostname router midebian-router
	docker network connect dmz router
	docker network connect dev router
	docker network connect srv router

	docker run --privileged --rm -ti -d \
		--name jump --hostname jump --ip 10.0.1.3 --network dmz midebian-jump

	docker run --privileged --rm -ti -d \
		--name work --hostname work --ip 10.0.3.3 --network dev midebian-work

	docker run --privileged --rm -ti -d \
		--name broker --hostname broker --ip 10.0.1.4 --network dmz midebian-broker

	docker run --privileged --rm -ti -d \
		--name auth --hostname auth --ip 10.0.2.3 --network srv midebian-auth

	docker run --privileged --rm -ti -d \
		--name files --hostname files --ip 10.0.2.4 --network srv midebian-files

all: DNS certificates build network containers

remove:
	-docker stop router work jump broker auth files
	-docker network prune -f

clean:
	find . -name "*~" -delete
