PROJECT_NAME=learn2slither
DOCKER_IMAGE=$(PROJECT_NAME):latest

all: build dev

build:
	@docker build -t $(DOCKER_IMAGE) .

dev:
	@docker run -it --rm \
		--name $(PROJECT_NAME) \
		-v $(PWD):/app \
		-e DISPLAY=$$DISPLAY \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		$(DOCKER_IMAGE)

clean:
	@yes | docker system prune -a -f

.PHONY: build dev clean normi all