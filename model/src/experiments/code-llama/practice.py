from transformers import AutoTokenizer
import transformers
import torch
import argparse

parser = argparse.ArgumentParser(description='Run CodeLlama model.')
parser.add_argument('--modelsize', type=int, required=True, help='Size of the model in billions (e.g., 13 for 13B).')
args = parser.parse_args()
model_size = args.modelsize

modelname = f"meta-llama/CodeLlama-{model_size}b-Python-hf"
print(f"Using model: {modelname}")

tokenizer = AutoTokenizer.from_pretrained(modelname)
pipeline = transformers.pipeline(
    "text-generation",
    model=modelname,
    torch_dtype=torch.float16,
    device_map="auto",
)

# not Instructed なのでcodeの出だしを書いてあげる?
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

for seq in sequences:
    print(f"Result: {seq['generated_text']}")