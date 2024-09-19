import requests
import base64
import time
import os

# GitHub APIの設定
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def search_code(keyword, language):
    query = f"{keyword} language:{language}"
    url = f"{GITHUB_API_URL}/search/code?q={query}&per_page=100"
    all_results = []
    page = 1

    while True:
        response = requests.get(url + f"&page={page}", headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        items = data.get("items", [])
        if not items:
            break

        all_results.extend(items)
        page += 1

        print(f"Retrieved {len(all_results)} results so far...")

        # レート制限への対応
        if "X-RateLimit-Remaining" in response.headers:
            remaining = int(response.headers["X-RateLimit-Remaining"])
            if remaining < 10:
                reset_time = int(response.headers["X-RateLimit-Reset"])
                sleep_time = reset_time - time.time() + 1
                print(f"Rate limit approaching. Sleeping for {sleep_time} seconds.")
                time.sleep(sleep_time)

        # GitHubの検索APIは最大1000件までしか返さない
        if len(all_results) >= 1000:
            print("Reached GitHub's search result limit of 1000 items.")
            break

    return all_results

def download_file(file_url, save_path):
    response = requests.get(file_url, headers=headers)
    if response.status_code == 200:
        content = base64.b64decode(response.json()["content"]).decode("utf-8")
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"File saved: {save_path}")
    else:
        print(f"Error downloading file: {response.status_code}")

def main():
    keyword = '"from manim import"'  # 検索したいキーワード
    language = "Python"  # 検索したい言語

    results = search_code(keyword, language)

    print(f"Total files found: {len(results)}")

    for item in results:
        file_url = item["url"]
        file_path = item["path"]
        repo_name = item["repository"]["full_name"]

        save_dir = os.path.join("downloaded_code", repo_name)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, os.path.basename(file_path))

        download_file(file_url, save_path)

if __name__ == "__main__":
    main()