# Video Generator API

This project provides an API for generating videos using LLM and Manim.

## Setup


クローンする
https://github.com/KinjiKawaguchi/text2manim.git
api/config/config.yamlを設定する。
デフォルトは
```yaml
api_keys:
  key1:
    service: 'service1'
    permissions: ['read', 'write']
  key2:
    service: 'service2'
    permissions: ['read']

ip_whitelist:
  - '192.168.1.0/24'
  - '10.0.0.1'
  - '172.18.0.4'
```

api_keysには、APIキーとサービス名、権限を設定する。
ip_whitelistには、許可するIPアドレスを設定する。

/worker/.env.exampleを.envにリネームして、設定する。
```
# .env.example

# Server Settings
WORKER_PORT=50052

# Storage Settings
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=/tmp/text2manim

# GCP Storage Settings (if using GCP)
GCP_BUCKET_NAME=your-bucket-name
GCP_CREDENTIALS_PATH=/path/to/your/service-account-key.json

# OpenAI Settings
USE_OPENAI=false
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o

# # Hugging Face Model Settings
# HF_MODEL_NAME=your-username/your-model-name
# HF_TOKEN=your_huggingface_api_token
# HF_CACHE_DIR=/path/to/huggingface/cache

# Model Generation Settings
MODEL_NAME=your-username/your-model-name
MODEL_MAX_LENGTH=1000
MODEL_TEMPERATURE=0.7
MODEL_TOP_K=50
MODEL_TOP_P=0.95

# Manim Settings
MANIM_QUALITY=medium_quality
MANIM_OUTPUT_FILE=scene.mp4

# Logging Settings
LOG_LEVEL=INFO
LOG_FILE=/path/to/log/file.log

# Security Settings
ALLOWED_IPS=127.0.0.1,192.168.1.0/24
```

STORAGE_TYPEには、localかgcpを設定する。
LOCAL_STORAGE_PATHには、ローカルの保存先を設定する。
GCPの場合は、GCP_BUCKET_NAMEとGCP_CREDENTIALS_PATHを設定する。

USE_OPENAIには、OpenAIを使うかどうかを設定する。
OPENAI_API_KEYには、OpenAIのAPIキーを設定する。
OPENAI_MODELには、OpenAIのモデルを設定する。

MODEL_NAMEには、Hugging Faceのモデルを設定する。
MODEL_MAX_LENGTHには、最大の長さを設定する。
MODEL_TEMPERATUREには、温度を設定する。
MODEL_TOP_Kには、トップKを設定する。
MODEL_TOP_Pには、トップPを設定する。

MANIM_QUALITYには、Manimの品質を設定する。
MANIM_OUTPUT_FILEには、出力ファイル名を設定する。

LOG_LEVELには、ログレベルを設定する。
LOG_FILEには、ログファイルのパスを設定する。

ALLOWED_IPSには、許可するIPアドレスを設定する。



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
