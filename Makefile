build:
	@echo "*** build"
	docker build --rm -f docker/Dockerfile --tag debian-base docker/
	docker build --rm -f docker/router/Dockerfile --tag debian-router docker/router/
	docker build --rm -f docker/jump/Dockerfile --tag debian-jump docker/jump/
	docker build --rm -f docker/work/Dockerfile --tag debian-work docker/work/
	
network:
	@echo "*** network"
	-docker network create -d bridge --subnet 10.0.1.0/24 dmz
	-docker network create -d bridge --subnet 10.0.3.0/24 dev

containers: network
	@echo "*** containers"
	docker run --privileged -ti -d --name router --hostname router debian-router
	docker network connect dmz router
	docker network connect dev router
	
	docker run --privileged -ti -d --name jump --hostname jump\
		--network dmz --ip 10.0.1.3 debian-jump
	docker run --privileged -ti -d --name work --hostname work\
		--network dev --ip 10.0.3.3 debian-work

remove:
	@echo "*** remove"
	-docker stop router jump work
	docker network prune -f
	docker rm -f router jump work

clean:
	find . -name "*~" -delete