import os
import sys
import json
from datetime import datetime
import argparse

# OpenAI API
import openai

# HuggingFace Transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def load_prompts(prompt_file):
    if not os.path.exists(prompt_file):
        print(f'エラー: {prompt_file} が存在しません。')
        sys.exit(1)
    with open(prompt_file, 'r') as f:
        data = json.load(f)
    if not isinstance(data, list):
        print('エラー: プロンプトファイルはプロンプトのリストを含む必要があります。')
        sys.exit(1)
    return data

def load_models(model_file):
    if not os.path.exists(model_file):
        print(f'エラー: {model_file} が存在しません。')
        sys.exit(1)
    with open(model_file, 'r') as f:
        models = json.load(f)
    if not isinstance(models, list):
        print('エラー: モデルファイルはモデル情報のリストを含む必要があります。')
        sys.exit(1)
    return models

def create_output_dir(base_dir, execution_time, model_name):
    output_dir = os.path.join(base_dir, execution_time, model_name)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def process_with_openai(model_name, prompts, output_dir):
    # OpenAI API設定
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if openai.api_key is None:
        print('エラー: 環境変数 OPENAI_API_KEY が設定されていません。')
        sys.exit(1)

    for i, prompt in enumerate(prompts):
        print(f'[{model_name}] プロンプト {i+1}/{len(prompts)} を処理中...')
        try:
            response = openai.Completion.create(
                engine=model_name,
                prompt=prompt,
                max_tokens=1024
            )
            text = response['choices'][0]['text']
        except Exception as e:
            print(f'エラー: プロンプト {i+1} の処理中にエラーが発生しました: {e}')
            text = ''
        save_output(output_dir, i, text)

def process_with_hf(model_name, prompts, output_dir):
    # デバイスの設定
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # モデルとトークナイザーのロード
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        model.to(device)
        model.eval()
    except Exception as e:
        print(f'エラー: モデル {model_name} のロード中にエラーが発生しました: {e}')
        return

    for i, prompt in enumerate(prompts):
        print(f'[{model_name}] プロンプト {i+1}/{len(prompts)} を処理中...')
        inputs = tokenizer.encode(prompt, return_tensors='pt').to(device)
        try:
            outputs = model.generate(inputs, max_length=1024)
            text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            print(f'エラー: プロンプト {i+1} の処理中にエラーが発生しました: {e}')
            text = ''
        save_output(output_dir, i, text)

def save_output(output_dir, index, text):
    output_file = os.path.join(output_dir, f'prompt_{index+1}.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    parser = argparse.ArgumentParser(description='複数のLLMモデルでプロンプトを実行し、出力を保存します。')
    parser.add_argument('--prompt_file', type=str, default='data/sample_prompts.json', help='プロンプトが含まれるJSONファイル')
    parser.add_argument('--model_file', type=str, default='models.json', help='モデル情報が含まれるJSONファイル')
    parser.add_argument('--output_dir', type=str, default='outputs', help='出力を保存するディレクトリ')

    args = parser.parse_args()

    prompts = load_prompts(args.prompt_file)
    models = load_models(args.model_file)
    execution_time = datetime.now().strftime('%Y%m%d_%H%M%S')

    for model_info in models:
        provider = model_info.get('provider')
        model_name = model_info.get('model_name')
        if not provider or not model_name:
            print('エラー: モデル情報に provider または model_name がありません。')
            continue

        output_dir = create_output_dir(args.output_dir, execution_time, model_name)

        if provider == 'openai':
            process_with_openai(model_name, prompts, output_dir)
        elif provider == 'hf':
            process_with_hf(model_name, prompts, output_dir)
        else:
            print(f'エラー: 不明なプロバイダ {provider} が指定されました。')

if __name__ == '__main__':
    main()
