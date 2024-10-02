# Text2Manim: Video Generator API

## プロジェクト概要

Text2Manimは、大規模言語モデル（LLM）とManimを使用して、テキスト入力から自動的に数学的なアニメーションビデオを生成するAPIを提供するプロジェクトです。Docker Composeを使用して簡単にセットアップと実行が可能です。

主な特徴：

- テキスト入力からManimコードを自動生成
- 生成されたManimコードからビデオアニメーションを作成
- RESTful APIによる簡単な統合
- Docker Composeによる簡単なデプロイ

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

2. 設定ファイルを準備します：
   - `api/config/config.yaml` を必要に応じて編集します。
     デフォルトの設定:

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

     注意: 実運用環境では、セキュリティのためにAPIキーを変更することを強く推奨します。

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
     - `GCP_BUCKET_NAME`: GCPバケットの名前（GCP使用時）
     - `GCP_CREDENTIALS_PATH`: GCPサービスアカウントキーファイルのパス（GCP使用時）

     c. OpenAI設定:
     - `USE_OPENAI`: OpenAI APIの使用（`true` または `false`）
     - `OPENAI_API_KEY`: OpenAIのAPIキー
     - `OPENAI_MODEL`: 使用するOpenAIモデル（例: "gpt-4"）

     d. Hugging Face Model設定:
     - `HF_MODEL_NAME`: Hugging Faceモデルの名前
     - `HF_TOKEN`: Hugging FaceのAPIトークン
     - `HF_CACHE_DIR`: Hugging Faceのキャッシュディレクトリ

     e. モデル生成設定:
     - `MODEL_NAME`: 使用するモデルの名前
     - `MODEL_MAX_LENGTH`: 生成するテキストの最大長
     - `MODEL_TEMPERATURE`: 生成の温度
     - `MODEL_TOP_K`: 生成時に考慮する上位K個のトークン
     - `MODEL_TOP_P`: 生成時に考慮する累積確率の閾値

     f. Manim設定:
     - `MANIM_QUALITY`: Manimの出力品質（`low_quality`, `medium_quality`, `high_quality`）
     - `MANIM_OUTPUT_FILE`: 出力ファイル名

     g. ログ設定:
     - `LOG_LEVEL`: ログレベル（INFO, DEBUG, WARNING, ERRORなど）
     - `LOG_FILE`: ログファイルのパス

     h. セキュリティ設定:
     - `ALLOWED_IPS`: アクセスを許可するIPアドレス（カンマ区切りで複数指定可能）

     注意:
     - OpenAI API使用時は`USE_OPENAI=true`に設定し、`OPENAI_API_KEY`を必ず設定してください。
     - GCPストレージ使用時は`STORAGE_TYPE=gcp`に設定し、関連設定を行ってください。
     - 実運用環境では`ALLOWED_IPS`を適切に設定してください。

3. Dockerイメージをビルドし、コンテナを起動します：

   ```
   docker-compose up --build
   ```

これで、APIサーバーとワーカーが起動し、サービスの利用準備が整います。

## 設定

### api/config/config.yaml

このファイルでは、APIキーと許可するIPアドレスを設定します。

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

### worker/.env

このファイルでは、ワーカーの設定を行います。主な設定項目は以下の通りです：

- `WORKER_PORT`: ワーカーのポート番号
- `STORAGE_TYPE`: ストレージタイプ（local または gcp）
- `USE_OPENAI`: OpenAI APIを使用するかどうか
- `MODEL_NAME`: 使用する言語モデルの名前
- `MANIM_QUALITY`: Manimの出力品質
- `LOG_LEVEL`: ログレベル

詳細な設定オプションについては、`.env.example` ファイルを参照してください。

## 使用方法

APIを使用してビデオを生成するには、以下のようにcurlコマンドを使用してPOSTリクエストを送信します：

```bash
curl -X POST http://localhost:8080/v1/generations \
     -H "Content-Type: application/json" \
     -H "x-api-key: key1" \
     -d '{"prompt": "比例と反比例について説明する動画を作成してください。"}'
```

成功した場合、APIは生成されたビデオのURLを含むレスポンスを返します。

## 開発

開発者向けの情報は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

## トラブルシューティング

- **Q: Dockerコンテナが起動しない**
  A: Docker及びDocker Composeが正しくインストールされているか確認してください。また、ポートの競合がないか確認してください。

- **Q: APIにアクセスできない**
  A: `api/config/config.yaml`の`ip_whitelist`設定を確認し、クライアントのIPアドレスが許可されているか確認してください。

- **Q: ビデオ生成に失敗する**
  A: `docker-compose logs worker`コマンドでワーカーのログを確認し、エラーメッセージを確認してください。

問題が発生した場合は、[GitHub Issues](https://github.com/KinjiKawaguchi/text2manim/issues)をご確認ください。同様の問題がすでに報告されているかもしれません。新しい問題を見つけた場合は、イシューを作成してください。

## コントリビューション

プロジェクトへの貢献を歓迎します！詳細は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
