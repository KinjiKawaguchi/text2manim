.PHONY: all build test proto lint clean

all: build

build:
    go build -o bin/api ./api/cmd/main.go
    pip install -r worker/requirements.txt

test:
    go test ./api/...
    python -m pytest worker/

proto:
    protoc --go_out=. --go-grpc_out=. ./proto/text2manim/v1/*.proto
    python -m grpc_tools.protoc -I./proto --python_out=./worker --grpc_python_out=./worker ./proto/text2manim/v1/*.proto

lint:
    golangci-lint run ./api/...
    flake8 worker/
    black worker/
    isort worker/

clean:
    rm -rf bin/
    find . -type d -name __pycache__ -exec rm -rf {} +