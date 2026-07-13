# text2manim v1 リアーキテクチャ設計

## ゴール

**誰でもすぐデプロイして使える** テキスト→Manim動画生成エンジンをOSSとして提供する。

- インストールから初回動画生成まで、APIキー1つと1コマンドで到達できる
- セルフホスト前提（BYOK: 利用者が自分のLLM APIキーを使う）
- ポートフォリオ用Webアプリは別リポジトリ `text2manim-demo` が担い、本体はエンジンに徹する

## 非ゴール

- マルチテナントSaaS運用（課金・ユーザー管理は扱わない）
- 自前モデルのfine-tuning（旧 `model/` の路線は廃止。LLMはAPI利用に一本化）
- Go/gRPC/grpc-gateway/protoスタックの維持（Pythonに一本化）

## 提供形態

```
text2manim (PyPIパッケージ)
├── CLI           uvx text2manim "比例と反比例の説明" → out.mp4
├── ライブラリ     from text2manim import generate_video
└── サーバーモード  text2manim serve → REST API + ジョブキュー + SSE
```

配布は PyPI 一本。レンダリング用イメージは manimcommunity 公式のものを実行時に pull する。
自前のオールインワンイメージは配布しない。LLM 呼び出しに必要なネットワークと API キーが
生成コードと同じコンテナ境界に入り、レンダリングサンドボックスの隔離が無意味になるため。
利用者の前提条件は Python 3.14 (uv が解決) と Docker の2つ。

CLIファースト。サーバーやDBのセットアップを初回体験に要求しない。

## 言語・ツールチェーン

- **Python 3.14ベースライン**（`requires-python >= 3.14`）に一本化する
  - レンダリングがManim（Python）である以上、コアを別言語にすると2言語+境界RPCが復活し、リアーキテクトの主目的に反する
  - manim本体はライブラリ依存にせずサンドボックス内のsubprocessとして起動するため、
    本体のPythonバージョンはmanimの対応バージョンに縛られない
  - CLI配布は `uvx text2manim` で解決。サーバー性能はLLM/レンダリングが支配的でAPI層の言語は誤差
  - コントリビューター層（Manimユーザー = Python書き）と一致させる
- プロジェクト管理: **uv**
- 型安全を最優先する: 型チェックは **pyrefly（preset = all）**、lintは **ruff（select = ALL）**。
  イミュータブルなfrozen dataclassとユニオン型 + match文による網羅性チェックを基本形とする
- Webフレームワーク: FastAPI（サーバーモード実装時）

## アーキテクチャ

### コアパイプライン

```
prompt
  → LLMでManimスクリプト生成
  → 静的検証 (ast): 構文 / Sceneクラスの存在 / 禁止import
  → サンドボックスでレンダリング
  → 失敗時: 検証・レンダリングのエラーをLLMに渡して修正（最大N回、デフォルト3）
  → mp4 + 使用スクリプトを出力
```

修復ループが品質の本体で、実行結果をフィードバックする execution-feedback 型の
リフレクションとして機能する。静的検証はサンドボックス起動（秒単位）の前に
ミリ秒で弾ける問題を検出してループを高速化する層であり、セキュリティ境界ではない
（境界はサンドボックス。禁止importチェックは多層防御）。
各試行の経過（生成中/検証失敗/レンダリング中/修復n回目）はイベントとして購読可能にし、
CLIの進捗表示とサーバーのSSEの両方から使う。

実行前のLLM自己批評（レビュー専用呼び出し）は採用しない。Manimで多いAPI誤用系の
エラーは実行しないと検出できず、毎試行のLLMコスト増に見合わないため。

### LLMプロバイダー

- `LlmClient` プロトコルによる薄い抽象で任意のLLMに対応（BYOKなので非依存は必須要件）
  - `anthropic`: Anthropic API（既定）
  - `openai-compatible`: OpenAI 本家に加え、`base_url` 指定で OpenAI 互換 API を話す
    ローカルLLMサーバー（Ollama / vLLM / LM Studio 等）をすべてカバーする
- モデル名・温度等は設定で上書き可能。デフォルトは品質/コストバランスの良いモデル

### サンドボックス

LLM生成コードの実行は任意コード実行そのものなので、隔離をデフォルトにする。

| モード | 内容 | 用途 |
|--------|------|------|
| docker（デフォルト） | manim公式イメージを `--network none` + CPU/メモリ/タイムアウト制限の使い捨てコンテナで実行 | 通常利用 |
| local（opt-in） | ホストで直接 `manim` 実行 | Docker不可の環境・開発 |

dockerモードはmanim環境（ffmpeg・LaTeX・pangocairo等）をイメージに閉じ込めるため、
セキュリティと同時に「ホストへのmanimセットアップ不要」という配布上の利点も持つ。

サンドボックスはインターフェースで抽象化し、将来の実装追加（gVisor等）を妨げない。

### サーバーモード

- FastAPI + SQLite + プロセス内ワーカー。**外部DB・キューを必須にしない**
- REST契約（demoリポジトリが消費する安定API）:
  - `POST /v1/generations` … ジョブ作成、`request_id` を返す
  - `GET  /v1/generations/{request_id}` … ステータス取得
  - `GET  /v1/generations/{request_id}/stream` … SSEで進捗ストリーム
  - `GET  /v1/health`
- ステータス: `pending / processing / completed / failed`（旧protoの語彙を継承）
- 認証: APIキー（環境変数でカンマ区切り指定）。レートリミットをアプリ内で持つ
- プロトコルは REST + SSE のみ。gRPC は内部サービス間境界（旧 Go↔Python）の消滅とともに
  役割を失い、GraphQL はリソース1種類の API には過剰。型付き契約は FastAPI が生成する
  OpenAPI スキーマで担い、demo 側はそこから TypeScript クライアントを型生成する

### ストレージ

- ローカルファイルシステムがデフォルト
- S3互換をオプション（GCS/Cloud Run前提の設計は外す）

## ディレクトリ構成（案）

```
src/text2manim/
  pipeline/     生成→レンダリング→修復ループの本体
  llm/          プロバイダー抽象と各実装
  sandbox/      docker / local レンダラー
  server/       FastAPI・ジョブ・SSE
  storage/      local / s3
  cli.py
docs/
```

Docker Compose は使わない。常駐するのは `text2manim serve` の1プロセスのみで、
DBはSQLite、レンダリングは都度使い捨てコンテナを起動するため、
オーケストレーションの対象が存在しない。サーバー自体のコンテナ化は
docker.sock のマウントを要求しサンドボックスの隔離を薄めるため推奨しない。

## マイルストーン

1. **M1: CLIで一発生成** — pipeline + llm + サンドボックス。`text2manim "..."` が動く ✅
2. **M2: 修復ループ + dockerサンドボックス** — 品質と安全性の本体 ✅
3. **M3: サーバーモード** — REST + SQLiteジョブ + SSE
4. **M4: 公開整備** — PyPI公開、README（デモGIF）、demoリポジトリの再接続

## 将来拡張（ロードマップ候補）

- **視覚的リフレクション**: レンダリング成功後にフレームを抽出し、vision対応LLMが
  「プロンプトの意図との一致・要素の重なり・レイアウト崩れ」を評価して再生成を促す。
  「動く」の先の「良い動画」を担保する品質パス。LLMコストが増えるためopt-inとする

## 旧資産の扱い

- 旧実装は `v0-archive` タグを打って main を全面書き換え
- `model/` のfine-tuning実験はタグに封じ込めて削除
- 旧protoのAPI概形（非同期ジョブ + ステータス + ストリーム）は思想としてRESTに継承
