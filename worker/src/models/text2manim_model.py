import manim
import tempfile
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Text2ManimModel:
    def __init__(self, config):
        self.config = config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(config.model_name).to(self.device)

    def generate_script(self, prompt):
        # プロンプトの準備
        full_prompt = f"Generate a Manim script for the following prompt: {prompt}\n\nMakim script:"

        # トークナイズとモデル入力の準備
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.device)

        # スクリプト生成
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=1000,
                num_return_sequences=1,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )

        # 生成されたスクリプトのデコード
        generated_script = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # プロンプト部分を除去してスクリプトのみを抽出
        script = generated_script.split("Makim script:")[-1].strip()

        return script

    def generate_video(self, script):
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "scene.py")
            with open(script_path, "w") as f:
                f.write(script)

            output_file = os.path.join(tmpdir, "output.mp4")
            os.system(f"manim {script_path} MyScene -o {output_file}")

            if os.path.exists(output_file):
                return output_file
            else:
                raise Exception("Failed to generate video")