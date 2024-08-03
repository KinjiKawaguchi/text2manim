# data/scripts/data_collection.py

from github import Github
import os
import base64
from dotenv import load_dotenv

load_dotenv()

# GitHub Personal Access Token (環境変数から読み込み)
github_token = os.getenv("GITHUB_TOKEN")

# GitHubクライアントの初期化
g = Github(github_token)


def search_manim_code():
    # Manimをインポートしているコードを検索
    query = "import manim language:Python"
    results = g.search_code(query)

    collected_data = []

    for file in results:
        try:
            repo = file.repository
            content = base64.b64decode(file.content).decode('utf-8')

            # Manimのインポートを含むファイルのみを保存
            if "import manim" in content or "from manim import" in content:
                collected_data.append({
                    "repo_name": repo.full_name,
                    "file_path": file.path,
                    "content": content,
                    "url": file.html_url
                })

                print(f"Collected: {repo.full_name}/{file.path}")
        except Exception as e:
            print(f"Error processing {file.html_url}: {str(e)}")

    return collected_data


def save_collected_data(data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, item in enumerate(data):
        filename = f"manim_sample_{idx}.py"
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write(f"# Source: {item['url']}\n")
            f.write(f"# Repo: {item['repo_name']}\n")
            f.write(f"# Path: {item['file_path']}\n\n")
            f.write(item['content'])


if __name__ == "__main__":
    collected_data = search_manim_code()
    save_collected_data(collected_data, "../raw")
    print(f"Collected {len(collected_data)} Manim code samples.")
