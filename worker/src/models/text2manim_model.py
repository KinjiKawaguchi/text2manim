import shutil
import tempfile
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from openai import OpenAI
from openai.types.chat import ChatCompletion
from typing import Optional
from src.config import Config


def extract_code_from_markdown(content: str) -> str:
    if content.strip().startswith("```") and content.strip().endswith("```"):
        lines = content.strip().split("\n")
        return "\n".join(lines[1:-1])  # Remove the first and last lines (```)
    return content


class Text2ManimModel:
    def __init__(self, config):
        self.config: Config = config
        if self.config.use_openai:
            self.client = OpenAI(api_key=self.config.openai_api_key)
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(config.model_name).to(
                self.device
            )

    def _generate_script_openai(self, prompt: str) -> Optional[str]:
        try:
            response: ChatCompletion = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that generates Manim scripts.All output must be in a form that can be executed, so if you are outputting natural language, please comment it out or take other measures.Markdown is also not allowed.(BAD example: ```python code ```)",
                    },
                    {
                        "role": "user",
                        "content": f"Generate a Manim script for the following prompt: {prompt}.Markdown is not allowed.(BAD example: ```python code ```)",
                    },
                ],
                max_tokens=self.config.openai_max_tokens,
                temperature=self.config.openai_temperature,
                top_p=self.config.openai_top_p,
            )

            content = response.choices[0].message.content
            if content is None:
                print("Warning: Received empty content from OpenAI API")
                return None

            return extract_code_from_markdown(content)
        except Exception as e:
            print(f"Error occurred while generating script: {str(e)}")
            return None

    def _generate_script_local(self, prompt: str) -> str:
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
                do_sample=True,
            )

        # 生成されたスクリプトのデコード
        generated_script = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # プロンプト部分を除去してスクリプトのみを抽出
        script = generated_script.split("Makim script:")[-1].strip()

        return script

    def generate_script(self, prompt):
        if self.config.use_openai:
            return self._generate_script_openai(prompt)
        else:
            return self._generate_script_local(prompt)

    def generate_video(self, script):
        tmpdir = tempfile.mkdtemp()
        try:
            script_path = os.path.join(tmpdir, "scene.py")
            with open(script_path, "w") as f:
                f.write(script)

            output_file = os.path.join(tmpdir, "output.mp4")
            os.system(f"manim {script_path} MyScene -o {output_file}")

            if os.path.exists(output_file):
                return output_file
            else:
                raise Exception("Failed to generate video")
        except Exception as e:
            shutil.rmtree(tmpdir)
            raise e
