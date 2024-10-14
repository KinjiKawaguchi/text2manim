# Text2Manim: Video Generator API

## プロジェクト概要

Text2Manim は、大規模言語モデル（LLM）と Manim を使用して、テキスト入力から自動的に数学的なアニメーションビデオを生成する API を提供するプロジェクトです。Docker Compose を使用して簡単にセットアップと実行が可能です。

主な特徴：

- テキスト入力から Manim コードを自動生成
- 生成された Manim コードからビデオアニメーションを作成
- RESTful API による簡単な統合
- Docker Compose による簡単なデプロイ

## セットアップ

### 前提条件

- Docker
- Docker Compose
- Git

### セットアップ手順

1. リポジトリをクローンします：

   ```
   git clone https://github.com/KinjiKawaguchi/text2manim.git
   cd text2manim
   ```

2. 環境変数を設定します：

   - `api/.env.example` を `api/.env` にコピーし、必要な環境変数を設定します。

     ```
     cp api/.env.example api/.env
     ```

     設定項目:

     - `API_KEYS`: カンマ区切りの API キーリスト（例: "key1,key2"）
     - `IP_WHITELIST`: カンマ区切りの許可 IP アドレスリスト（例: "127.0.0.1,127.0.0.2"）
     - `WORKER_PORT`: ワーカーのポート（デフォルト: "50052"）
     - `SERVER_PORT`: API サーバーのポート（デフォルト: "50051"）
     - `LOG_LEVEL`: ログレベル（デフォルト: "INFO"）
     - `DB_TYPE`: データベースタイプ（"postgres" または "memory"）
     - `GRPC_SERVER_ADDRESS`: gRPC サーバーアドレス（デフォルト: "localhost:50051"）

     postgres を選択した場合の追加設定:

     - `DB_HOST`: PostgreSQL データベースホスト
     - `DB_PORT`: PostgreSQL データベースポート
     - `DB_USER`: PostgreSQL データベースユーザー名
     - `DB_PASSWORD`: PostgreSQL データベースパスワード
     - `DB_NAME`: PostgreSQL データベース名

     注意:

     - 実運用環境では、セキュリティのために API キーとデータベース認証情報を変更することを強く推奨します。
     - `DB_TYPE` を "memory" に設定した場合、PostgreSQL 関連の設定は無視されます。

   - `worker/.env.example` を `worker/.env` にコピーし、必要な環境変数を設定します。

     ```
     cp worker/.env.example worker/.env
     ```

     設定項目:
     a. サーバー設定:

     - `WORKER_PORT`: ワーカーのポート番号（デフォルト: 50052）

     b. ストレージ設定:

     - `STORAGE_TYPE`: 使用するストレージタイプ（`local` または `gcp`）
     - `LOCAL_STORAGE_PATH`: ローカルストレージを使用する場合の保存先パス
     - `GCP_BUCKET_NAME`: GCP バケットの名前（GCP 使用時）
     - `GCP_CREDENTIALS_PATH`: GCP サービスアカウントキーファイルのパス（GCP 使用時）

     c. OpenAI 設定:

     - `USE_OPENAI`: OpenAI API の使用（`true` または `false`）
     - `OPENAI_API_KEY`: OpenAI の API キー
     - `OPENAI_MODEL`: 使用する OpenAI モデル（例: "gpt-4"）

     d. Hugging Face Model 設定:

     - `HF_MODEL_NAME`: Hugging Face モデルの名前
     - `HF_TOKEN`: Hugging Face の API トークン
     - `HF_CACHE_DIR`: Hugging Face のキャッシュディレクトリ

     e. モデル生成設定:

     - `MODEL_NAME`: 使用するモデルの名前
     - `MODEL_MAX_LENGTH`: 生成するテキストの最大長
     - `MODEL_TEMPERATURE`: 生成の温度
     - `MODEL_TOP_K`: 生成時に考慮する上位 K 個のトークン
     - `MODEL_TOP_P`: 生成時に考慮する累積確率の閾値

     f. Manim 設定:

     - `MANIM_QUALITY`: Manim の出力品質（`low_quality`, `medium_quality`, `high_quality`）
     - `MANIM_OUTPUT_FILE`: 出力ファイル名

     g. ログ設定:

     - `LOG_LEVEL`: ログレベル（INFO, DEBUG, WARNING, ERROR など）
     - `LOG_FILE`: ログファイルのパス

     h. セキュリティ設定:

     - `ALLOWED_IPS`: アクセスを許可する IP アドレス（カンマ区切りで複数指定可能）

     注意:

     - OpenAI API 使用時は`USE_OPENAI=true`に設定し、`OPENAI_API_KEY`を必ず設定してください。
     - GCP ストレージ使用時は`STORAGE_TYPE=gcp`に設定し、関連設定を行ってください。
     - 実運用環境では`ALLOWED_IPS`を適切に設定してください。

3. Docker イメージをビルドし、コンテナを起動します：

   ```
   docker-compose up --build
   ```

これで、API サーバーとワーカーが起動し、サービスの利用準備が整います。

## 設定

### api/.env

このファイルでは、API キーと許可する IP アドレス、その他の API 設定を環境変数として定義します。

- `API_KEYS`: カンマ区切りの API キーリスト
- `IP_WHITELIST`: カンマ区切りの許可 IP アドレスリスト
- `WORKER_PORT`: ワーカーのポート番号
- `SERVER_PORT`: API サーバーのポート番号
- `LOG_LEVEL`: ログレベル
- `DB_TYPE`: データベースタイプ（"postgres" または "memory"）
- `DB_HOST`: PostgreSQL データベースホスト
- `DB_PORT`: PostgreSQL データベースポート
- `DB_USER`: PostgreSQL データベースユーザー名
- `DB_PASSWORD`: PostgreSQL データベースパスワード
- `DB_NAME`: PostgreSQL データベース名
- `GRPC_SERVER_ADDRESS`: gRPC サーバーアドレス

### worker/.env

このファイルでは、ワーカーの設定を行います。主な設定項目は以下の通りです：

- `WORKER_PORT`: ワーカーのポート番号
- `STORAGE_TYPE`: ストレージタイプ（local または gcp）
- `USE_OPENAI`: OpenAI API を使用するかどうか
- `MODEL_NAME`: 使用する言語モデルの名前
- `MANIM_QUALITY`: Manim の出力品質
- `LOG_LEVEL`: ログレベル

詳細な設定オプションについては、`.env.example` ファイルを参照してください。

## 使用方法

API を使用してビデオを生成するには、以下のように curl コマンドを使用して POST リクエストを送信します：

```bash
curl -X POST http://localhost:8080/v1/generations \
     -H "Content-Type: application/json" \
     -H "x-api-key: key1" \
     -d '{"prompt": "比例と反比例について説明する動画を作成してください。"}'
```

成功した場合、API は生成されたビデオの URL を含むレスポンスを返します。

## 開発

開発者向けの情報は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

## トラブルシューティング

- **Q: Docker コンテナが起動しない**
  A: Docker 及び Docker Compose が正しくインストールされているか確認してください。また、ポートの競合がないか確認してください。

- **Q: API にアクセスできない**
  A: `api/config/config.yaml`の`ip_whitelist`設定を確認し、クライアントの IP アドレスが許可されているか確認してください。

- **Q: ビデオ生成に失敗する**
  A: `docker-compose logs worker`コマンドでワーカーのログを確認し、エラーメッセージを確認してください。

問題が発生した場合は、[GitHub Issues](https://github.com/KinjiKawaguchi/text2manim/issues)をご確認ください。同様の問題がすでに報告されているかもしれません。新しい問題を見つけた場合は、イシューを作成してください。

## コントリビューション

プロジェクトへの貢献を歓迎します！詳細は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
