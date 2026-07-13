# serve モードの配布イメージ (Cloud Run など Docker デーモンのない実行環境向け)。
#
# manim 公式イメージ (manim / ffmpeg / TeX / pangocairo 同梱) をベースに、
# text2manim 本体は uv が取得する独立した Python 3.14 環境で動かす。
# レンダリングは sandbox=local (コンテナ自体が隔離境界)。
FROM manimcommunity/manim:stable

LABEL org.opencontainers.image.source="https://github.com/KinjiKawaguchi/text2manim" \
      org.opencontainers.image.description="テキストからManim動画を生成するステートレスworker" \
      org.opencontainers.image.licenses="MIT"

USER root
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
RUN uv sync --frozen --no-dev --python 3.14 && mkdir -p /videos

ENV PATH="/app/.venv/bin:${PATH}"
EXPOSE 8000

ENTRYPOINT ["text2manim", "serve", "--host", "0.0.0.0", "--sandbox", "local", "--output-dir", "/videos"]
