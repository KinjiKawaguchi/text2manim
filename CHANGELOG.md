# Changelog

## [0.5.1](https://github.com/KinjiKawaguchi/text2manim/compare/v0.5.0...v0.5.1) (2026-07-13)


### Bug Fixes

* **ci:** release-pleaseからpublishを直接呼び出す ([1b51c9b](https://github.com/KinjiKawaguchi/text2manim/commit/1b51c9bbacd14e8ad8279bf53b5506c315679ae8))

## [0.5.0](https://github.com/KinjiKawaguchi/text2manim/compare/v0.4.0...v0.5.0) (2026-07-13)


### ⚠ BREAKING CHANGES

* serveをステートレスな生成ワーカーに再設計
* 旧実装(Go API + Python worker)を廃止しv1リアーキテクトを開始

### Features

* serveのコンテナイメージを追加しGHCRへ公開する ([da648bd](https://github.com/KinjiKawaguchi/text2manim/commit/da648bd70801ee452d7b038e36d11f852e03a585))
* サーバーモードを実装 (REST + SQLiteジョブキュー + SSE) ([71ca4d8](https://github.com/KinjiKawaguchi/text2manim/commit/71ca4d858757e2875ce514f8450529a4ee72c868))
* レンダリングsubprocessへのシークレット継承を遮断 ([d6c65f9](https://github.com/KinjiKawaguchi/text2manim/commit/d6c65f9e0192497656809f125a7f3f6b53e54c03))
* 生成→検証→レンダリング→修復のコアパイプラインを実装 ([a04bb95](https://github.com/KinjiKawaguchi/text2manim/commit/a04bb950866424c6ef1a2d8a7568ebc4f6bac6d1))


### Bug Fixes

* **ci:** バージョンを__init__.py起点の動的取得にしてリリースPRのCI失敗を解消 ([3795ee6](https://github.com/KinjiKawaguchi/text2manim/commit/3795ee6675d6175884aad77f59b64691defacba8))
* temperatureを指定時のみリクエストに含める ([b9914cf](https://github.com/KinjiKawaguchi/text2manim/commit/b9914cf7a74453946d71ad5adabb4f4f76067ee3))


### Documentation

* サーバーモードのスケーリング境界を明文化 ([70f949c](https://github.com/KinjiKawaguchi/text2manim/commit/70f949c10242e694fa37d18425fb672ce6eda10d))
* 実測に基づくリソースモデルと最小スペックを明記 ([dd3892e](https://github.com/KinjiKawaguchi/text2manim/commit/dd3892ed036b870da3f92ad99f3c60d3c285c17d))
* 旧実装への参照をコードとドキュメントから削除 ([3e81f01](https://github.com/KinjiKawaguchi/text2manim/commit/3e81f01c959fcc45ff045089fa3c4daa28993c38))
* 著作権年を更新しイメージ配布時のライセンス義務を明記 ([256c8e7](https://github.com/KinjiKawaguchi/text2manim/commit/256c8e7e9ef15d94deaaa987215924adde3e5664))


### Miscellaneous Chores

* 旧実装(Go API + Python worker)を廃止しv1リアーキテクトを開始 ([699933d](https://github.com/KinjiKawaguchi/text2manim/commit/699933d9e3dc5e946a7597f8dbd6b21052e4bd90))


### Code Refactoring

* serveをステートレスな生成ワーカーに再設計 ([39a3663](https://github.com/KinjiKawaguchi/text2manim/commit/39a3663c5ab819795ee445b84f99093dc3bcd15c))
