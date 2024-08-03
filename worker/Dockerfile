# ベースイメージとしてPython 3.9を使用
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    ffmpeg \
    texlive-full \
    && rm -rf /var/lib/apt/lists/*

# Poetryをインストール
RUN pip install --no-cache-dir poetry

# プロジェクトファイルをコピー
COPY pyproject.toml poetry.lock* /app/

# 依存関係をインストール
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# アプリケーションのソースコードをコピー
COPY src /app/src
COPY .env /app/.env

# 環境変数を設定
ENV PYTHONPATH=/app

# ポート50052を開放
EXPOSE 50052

# アプリケーションを実行
CMD ["python", "-m", "src.main"]