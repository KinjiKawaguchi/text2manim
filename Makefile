.PHONY: all build test proto lint clean

# Go parameters
GOCMD=go
GOBUILD=$(GOCMD) build
GOCLEAN=$(GOCMD) clean
GOTEST=$(GOCMD) test
GOGET=$(GOCMD) get

# Python parameters
PYTHON=python3
PIP=$(PYTHON) -m pip

# Main targets
all: build

build: build-go build-python

test: test-go test-python

lint: lint-go lint-python lint-proto

clean: clean-go clean-python

# Go targets
build-go:
	$(GOBUILD) -o bin/api ./api/cmd/main.go

test-go:
	$(GOTEST) ./api/...

lint-go:
	golangci-lint run ./api/...

clean-go:
	$(GOCLEAN)
	rm -f bin/api

# Python targets
build-python:
	$(PIP) install -r worker/requirements.txt

test-python:
	$(PYTHON) -m pytest worker/

lint-python:
	flake8 worker/
	black --check worker/
	isort --check-only worker/

clean-python:
	find . -type d -name __pycache__ -exec rm -rf {} +

proto:
	cd proto && buf generate

lint-proto:
	buf lint

# Additional targets
setup:
	$(GOGET) -u github.com/golangci/golangci-lint/cmd/golangci-lint
	$(PIP) install -r worker/requirements.txt
	$(PIP) install flake8 black isort pytest
	go install github.com/bufbuild/buf/cmd/buf@latest

format:
	gofmt -w ./api
	black worker/
	isort worker/

check: lint test