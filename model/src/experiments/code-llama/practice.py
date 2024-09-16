from transformers import AutoTokenizer
import transformers
import torch
import argparse
import os
from datetime import datetime

parser = argparse.ArgumentParser(description='Run CodeLlama model.')
parser.add_argument('--modelsize', type=int, required=True, help='Size of the model in billions (e.g., 13 for 13B).')
parser.add_argument('--device_map', type=str, default="auto", help='Device map for model distribution. E.g., "auto", "cpu", 0, [0,1], or a dictionary.')
parser.add_argument('--output_dir', type=str, default="assets/experiments/code-llama", help='Directory to save the output.')
args = parser.parse_args()

model_size = args.modelsize
modelname = f"meta-llama/CodeLlama-{model_size}b-Python-hf"
print(f"Using model: {modelname}")

# デバイスマップの処理
if args.device_map.isdigit():
    device_map = int(args.device_map)
elif args.device_map.startswith('[') and args.device_map.endswith(']'):
    device_map = eval(args.device_map)
    print(f"Using device_map: {device_map}")
else:
    device_map = args.device_map

print(f"Using device_map: {device_map}")

tokenizer = AutoTokenizer.from_pretrained(modelname)
pipeline = transformers.pipeline(
    "text-generation",
    model=modelname,
    torch_dtype=torch.float16,
    device_map=device_map,
)

prompt = "import * from manim\n# Draw the graph of a quadratic function and indicate its vertex and axis."
sequences = pipeline(
    prompt,
    do_sample=True,
    top_k=10,
    temperature=0.1,
    top_p=0.95,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=4095,
)

# 出力ディレクトリの作成
os.makedirs(args.output_dir, exist_ok=True)

# 現在の時刻を取得してファイル名に使用
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(args.output_dir, f"output_{model_size}B-{current_time}.txt")

# 結果を表示し、ファイルに保存
with open(output_file, 'w') as f:
    for seq in sequences:
        result = seq['generated_text']
        print(f"Result: {result}")
        f.write(f"Result: {result}\n")

print(f"Output saved to: {output_file}")