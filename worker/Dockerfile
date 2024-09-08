# ベースイメージとして Python 3.12 を使用
FROM python:3.12-slim AS builder

# 作業ディレクトリを設定
WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    ffmpeg \
    texlive-base \
    texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*

# Rye と uv をインストール
RUN pip install --no-cache-dir uv

# プロジェクトファイルをコピー
COPY pyproject.toml requirements.lock* /app/

# 依存関係をインストール
RUN uv pip install --no-cache --system -r requirements.lock

# アプリケーションのソースコードをコピー
COPY src /app/src
COPY .env /app/.env

# 環境変数を設定
ENV PYTHONPATH=/app

# ポート50052を開放
EXPOSE 50052

# アプリケーションを実行
CMD ["python", "-m", "src.main"]