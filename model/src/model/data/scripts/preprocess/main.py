import os
import json
from openai import OpenAI

# OpenAI APIキーを環境変数から取得
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# プロンプトファイルを読み込む
def load_prompt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# LLMを使用してコードを処理する
def process_code(prompt, code):
    response = client.chat.completions.create(
        model="gpt-4o",  # または適切なモデルを指定
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": code}
        ]
    )
    return response.choices[0].message.content

# 結果を保存する
def save_result(file_path, result):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

# メイン処理
def main():
    prompt = load_prompt('src/model/data/scripts/preprocess/prompt.txt')
    input_directory = 'data/raw/'
    output_directory = 'data/processed_codes'

    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith('.py'):  # Pythonファイルのみを処理
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, f'processed_{filename}.json')

            with open(input_path, 'r', encoding='utf-8') as file:
                code = file.read()

            result = process_code(prompt, code)
            save_result(output_path, {"original": code, "processed": result})

            print(f"Processed {filename}")

if __name__ == "__main__":
    main()