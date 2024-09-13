from github import Github
import os
import base64
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import threading
import json

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
g = Github(github_token)

class AtomicCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    def value(self):
        with self._lock:
            return self._value

def check_rate_limit():
    rate_limit = g.get_rate_limit()
    core_rate = rate_limit.core
    search_rate = rate_limit.search
    print(f"Core API Rate Limit: {core_rate.remaining}/{core_rate.limit}")
    print(f"Search API Rate Limit: {search_rate.remaining}/{search_rate.limit}")
    if search_rate.remaining < 5 or core_rate.remaining < 100:
        reset_time = max(search_rate.reset, core_rate.reset).replace(tzinfo=None)
        wait_time = (reset_time - datetime.now()).total_seconds()
        print(f"API rate limit almost exceeded. Waiting for {wait_time:.2f} seconds.")
        time.sleep(wait_time + 1)

def search_manim_repos(query, start_date, end_date):
    full_query = f"{query} created:<{start_date} created:>={end_date}"
    print(full_query)
    repos = g.search_repositories(query=full_query, sort="stars", order="desc")
    return list(repos)

def process_repo(repo):
    collected_data = []
    try:
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            elif file_content.name.endswith(".py"):
                try:
                    content = file_content.decoded_content.decode('utf-8')
                    if "from manim import" in content.lower():
                        collected_data.append({
                            "repo_name": repo.full_name,
                            "file_path": file_content.path,
                            "content": content,
                            "url": file_content.html_url,
                            "last_modified": file_content.last_modified
                        })
                except Exception as e:
                    print(f"Error processing file {file_content.html_url}: {str(e)}")
    except Exception as e:
        print(f"Error processing repo {repo.full_name}: {str(e)}")

    return collected_data

def collect_manim_code(start_date, end_date):
    query = "from manim import language:python"
    repos = search_manim_repos(query, start_date, end_date)
    print(f"Found {len(repos)} repositories for period {start_date} to {end_date}")

    all_data = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_repo = {executor.submit(process_repo, repo): repo for repo in repos}
        for future in tqdm(as_completed(future_to_repo), total=len(repos), desc="Processing repositories"):
            repo = future_to_repo[future]
            try:
                data = future.result()
                all_data.extend(data)
            except Exception as e:
                print(f"Error processing repo {repo.full_name}: {str(e)}")

            check_rate_limit()  # Check and wait if necessary after each repo

    return all_data

def save_collected_data(data, base_output_dir):
    for item in data:
        time_dir = datetime.strptime(item['last_modified'], "%a, %d %b %Y %H:%M:%S GMT").strftime("%Y%m%d_%H")
        output_dir = os.path.join(base_output_dir, time_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        safe_filename = f"{item['repo_name'].replace('/', '_')}_{item['file_path'].replace('/', '_')}.py"
        file_path = os.path.join(output_dir, safe_filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# Source: {item['url']}\n")
            f.write(f"# Repo: {item['repo_name']}\n")
            f.write(f"# Path: {item['file_path']}\n")
            f.write(f"# Last modified: {item['last_modified']}\n\n")
            f.write(item['content'])

def generate_date_ranges(start_date, end_date, interval_days):
    current_date = start_date
    while current_date < end_date:
        next_date = min(current_date + timedelta(days=interval_days), end_date)
        yield current_date.strftime("%Y-%m-%d"), next_date.strftime("%Y-%m-%d")
        current_date = next_date + timedelta(days=1)

if __name__ == "__main__":
    check_rate_limit()

    start_date = datetime(2015, 1, 1)
    end_date = datetime.now()
    interval_days = 180  # 半年ごとに分割

    all_collected_data = []

    for period_start, period_end in generate_date_ranges(start_date, end_date, interval_days):
        print(f"Collecting data for period: {period_start} to {period_end}")
        period_data = collect_manim_code(period_start, period_end)
        all_collected_data.extend(period_data)

        # 中間結果の保存
        interim_filename = f"interim_data_{period_start}_{period_end}.json"
        with open(interim_filename, 'w') as f:
            json.dump(period_data, f)

        print(f"Collected {len(period_data)} samples for this period. Interim results saved to {interim_filename}")
        time.sleep(0.1)  # 各期間の間に1分待機

    # Remove duplicates based on URL
    unique_data = list({item['url']: item for item in all_collected_data}.values())

    base_output_dir = "./assets/raw"
    save_collected_data(unique_data, base_output_dir)
    print(f"Collected a total of {len(unique_data)} unique Manim code samples.")