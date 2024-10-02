# ベースイメージとして Python 3.12 を使用
FROM python:3.12-slim AS builder

# 作業ディレクトリを設定
WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    ffmpeg \
    texlive-base \
    texlive-latex-extra \
    pkg-config \
    libcairo2-dev \
    build-essential \
    libpango1.0-dev \
    && rm -rf /var/lib/apt/lists/*

# 環境変数を設定
ENV PKG_CONFIG_PATH="/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/share/pkgconfig:$PKG_CONFIG_PATH"
ENV PYTHONPATH=/app:/app/src:$PYTHONPATH

RUN echo ${PYTHONPATH}

# Python パッケージをインストール
RUN pip install --no-cache-dir pycairo uv

# プロジェクトファイルをコピー
COPY pyproject.toml requirements.lock* README.md /app/

# 依存関係をインストール
RUN uv pip install --no-cache --system -r requirements.lock

# アプリケーションのソースコードをコピー
COPY . /app/

# ポート50052を開放
EXPOSE 50052

# アプリケーションを実行
CMD ["python", "-m", "src.main"]
