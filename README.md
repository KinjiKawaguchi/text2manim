# Video Generator API

This project provides an API for generating videos using LLM and Manim.

## Setup

1. Clone the repository
2. Install dependencies:
   - Go 1.22+
   - Python 3.12+
3. Run `make build` to build the project
4. Set up environment variables (see `.env.example`)

## Usage

1. Start the API server: `./bin/api`
2. Start the worker: `python worker/main.py`
3. Send requests to `http://localhost:8080/v1/generations`

## Development

- Run tests: `make test`
- Generate protobuf: `make proto`
- Lint code: `make lint`

For more details, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
