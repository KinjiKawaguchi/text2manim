from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model = AutoModelForCausalLM.from_pretrained("meta-llama/CodeLlama-7b-Python-hf")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/CodeLlama-7b-Python-hf")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

prompt = "Please write a Python function that takes a list of integers as input and returns the sum of the list."

inputs = tokenizer(prompt, return_tensors="pt").to(device)

with torch.no_grad():
    output = model.generate(**inputs, max_length=1000,do_sample=True,
                            top_k=50, top_p=0.95, temperature=0.5)

generated_code = tokenizer.decode(output[0], skip_special_tokens=True)

print(generated_code)
