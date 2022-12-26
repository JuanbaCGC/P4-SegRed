build:
	docker build --rm -f docker/Dockerfile --tag midebian docker/
	docker build --rm -f docker/router/Dockerfile --tag midebian-router docker/router
	docker build --rm -f docker/jump/Dockerfile --tag midebian-jump docker/jump
	docker build --rm -f docker/work/Dockerfile --tag midebian-work docker/work
	docker build --rm -f docker/broker/Dockerfile --tag midebian-broker docker/broker

network:
	-docker network create -d bridge --subnet 10.0.1.0/24 dmz
	-docker network create -d bridge --subnet 10.0.3.0/24 dev

containers: build network
	docker run --privileged --rm -ti -d --name router --hostname router midebian-router
	docker network connect dmz router
	docker network connect dev router

	docker run --privileged --rm -ti -d \
		--name jump --hostname jump --ip 10.0.1.3 --network dmz midebian-jump

	docker run --privileged --rm -ti -d \
		--name work --hostname work --ip 10.0.3.3 --network dev \
		midebian-work

	docker run --privileged --rm -ti -d \
		--name broker --hostname broker --ip 10.0.1.4 --network dmz \
		midebian-broker

remove:
	-docker stop router work jump broker
	-docker network prune -f

clean:
	find . -name "*~" -delete
