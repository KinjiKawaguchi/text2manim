from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import datetime
from manim import *

# Code Llama モデルのロード
model_name = "meta-llama/CodeLlama-7b-Python-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

# プロンプトの設定
prompt = """
# Manimを使用して三平方の定理を説明するアニメーションを作成してください。
# 作成したコードを実行しただけでアニメーションが作られる形式である必要があります。
# アニメーションには以下の要素を含めてください：
# 1. 直角三角形の描画
# 2. 各辺の長さの表示
# 3. 各辺の二乗を表す正方形の描画
# 4. a^2 + b^2 = c^2 の数式の表示

from manim import *

if __name__ == "__main__":

"""

# モデルによるコード生成
input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
output = model.generate(input_ids, max_length=10000, num_return_sequences=1)
generated_code = tokenizer.decode(output[0], skip_special_tokens=True)

# 生成されたコードをその日時で保存
now = datetime.datetime.now()
filename = f"manim_{now:%Y%m%d_%H%M%S}.py"
with open(f"src/model/experiment/code-llama/generated/{filename}" , "w") as f:
    f.write(generated_code)
