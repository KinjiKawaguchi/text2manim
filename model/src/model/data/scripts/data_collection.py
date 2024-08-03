from github import Github
import os
import base64
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
g = Github(github_token)

def search_manim_code(base_query, start_date, end_date, min_stars=0, max_stars=1000000):
    query = f"{base_query} created:{start_date}..{end_date} stars:{min_stars}..{max_stars}"
    results = g.search_code(query)
    return results

def collect_samples(base_query, start_date, end_date, min_stars, max_stars):
    collected_data = []
    results = search_manim_code(base_query, start_date, end_date, min_stars, max_stars)

    print(f"Found {results.totalCount} results for query: {base_query} "
          f"(date: {start_date} to {end_date}, stars: {min_stars} to {max_stars})")

    for file in results:
        try:
            repo = file.repository
            content = base64.b64decode(file.content).decode('utf-8')

            if "from manim import" in content or "import manim" in content:
                collected_data.append({
                    "repo_name": repo.full_name,
                    "file_path": file.path,
                    "content": content,
                    "url": file.html_url,
                })

                print(f"Collected: {repo.full_name}/{file.path}")

            time.sleep(0.1)  # Rate limiting
        except Exception as e:
            print(f"Error processing {file.html_url}: {str(e)}")

    return collected_data

def save_collected_data(data, base_output_dir):
    for item in data:
        # 時間ごとのディレクトリを作成
        time_dir = item['created_at'].strftime("%Y%m%d_%H")
        output_dir = os.path.join(base_output_dir, time_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # ファイル名を生成（リポジトリ名とファイルパスから）
        safe_filename = f"{item['repo_name'].replace('/', '_')}_{item['file_path'].replace('/', '_')}.py"
        file_path = os.path.join(output_dir, safe_filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# Source: {item['url']}\n")
            f.write(f"# Repo: {item['repo_name']}\n")
            f.write(f"# Path: {item['file_path']}\n")
            f.write(f"# Created at: {item['created_at']}\n\n")
            f.write(item['content'])

if __name__ == "__main__":
    base_query = "from manim import * language:Python"
    start_date = datetime(2015, 1, 1)
    end_date = datetime.now()
    date_range = 180  # days

    star_ranges = [(0, 10), (11, 50), (51, 100), (101, 1000), (1001, 1000000)]

    all_collected_data = []

    current_date = start_date
    while current_date < end_date:
        next_date = min(current_date + timedelta(days=date_range), end_date)

        for min_stars, max_stars in star_ranges:
            collected_data = collect_samples(
                base_query,
                current_date.strftime("%Y-%m-%d"),
                next_date.strftime("%Y-%m-%d"),
                min_stars,
                max_stars
            )
            all_collected_data.extend(collected_data)
            print(f"Collected {len(collected_data)} samples for this query")
            time.sleep(10)  # Wait between queries to avoid hitting rate limits

        current_date = next_date

    # Remove duplicates based on URL
    unique_data = {item['url']: item for item in all_collected_data}.values()

    base_output_dir = "./data/raw"
    save_collected_data(unique_data, base_output_dir)
    print(f"Collected a total of {len(unique_data)} unique Manim code samples.")