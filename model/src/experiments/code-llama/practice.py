from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import argparse

parser = argparse.ArgumentParser(description='Run CodeLlama model.')
parser.add_argument('--modelsize', type=int, required=True, help='Size of the model in billions (e.g., 13 for 13B).')
args = parser.parse_args()
model_size = args.modelsize

modelname = f"meta-llama/CodeLlama-{model_size}b-Python-hf"
model = AutoModelForCausalLM.from_pretrained("meta-llama/CodeLlama-13b-Python-hf")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/CodeLlama-13b-Python-hf")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# prompt = "Please write a Python function that takes a list of integers as input and returns the sum of the list."

# not Instructed なのでcodeの出だしを書いてあげる?
prompt = "import * from manim\n# Draw the graph of a quadratic function and indicate its vertex and axis."

inputs = tokenizer(prompt, return_tensors="pt").to(device)

with torch.no_grad():
    output = model.generate(**inputs, max_length=10000,do_sample=True,
                            top_k=50, top_p=0.95, temperature=0.5)

generated_code = tokenizer.decode(output[0], skip_special_tokens=True)

print(generated_code)
