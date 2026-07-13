# text2manim

テキストからManim動画を生成するエンジン。CLI・Pythonライブラリ・サーバーモード（REST API）を提供する。

> **開発中**: 設計は [docs/DESIGN.md](docs/DESIGN.md) を参照してください。

## 目指す姿

```bash
export ANTHROPIC_API_KEY=...
uvx text2manim "比例と反比例について説明する動画を作成してください"
# → out.mp4
```

- **CLI**: 1コマンドで生成。サーバーもDBも不要
- **ライブラリ**: Pythonプロジェクトに組み込み可能
- **サーバーモード**: `text2manim serve` でステートレスな生成worker（REST + SSE進捗ストリーム）

## 動作要件

- Python 3.14（uvが解決）と Docker
- サーバーモードの既定構成（同時レンダリング1）は **2vCPU / 4GB** のインスタンスで動作する。
  レンダリングはサンドボックスの上限（2GB / 2CPU / タイムアウト）で常に有界

## ライセンス

MIT
