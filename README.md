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
- **サーバーモード**: `text2manim serve` でREST API + ジョブキュー + SSE進捗ストリーム

## ライセンス

MIT
