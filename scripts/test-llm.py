import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import argparse

def generate_response(text, model, tokenizer, max_new_tokens=100, do_sample=True, top_p=0.95, temperature=0.7):
    text = text + "Ans. "
    tokenized_input = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            tokenized_input,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            top_p=top_p,
            temperature=temperature,
        )[0]

    print(tokenizer.decode(output))

def main():
    parser = argparse.ArgumentParser(description="Generate response using the language model")
    parser.add_argument("text", type=str, help="Input text for generating response")
    parser.add_argument("--model_path", type=str, default="../models/llm-jp/llm-jp-13b-instruct-full-jaster-dolly-oasst-v1.0", help="Path to the pretrained model")
    parser.add_argument("--tokenizer_path", type=str, default="../models/llm-jp/llm-jp-13b-instruct-full-jaster-dolly-oasst-v1.0", help="Path to the pretrained tokenizer")
    parser.add_argument("--max_new_tokens", type=int, default=100, help="Maximum number of tokens in the generated response")
    parser.add_argument("--do_sample", action="store_true", help="Whether to use sampling in generation")
    parser.add_argument("--top_p", type=float, default=0.95, help="Top-p nucleus sampling parameter")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature parameter for sampling")

    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_path)
    model = AutoModelForCausalLM.from_pretrained(args.model_path, torch_dtype=torch.float16)
    model = model.to("cuda:0")

    generate_response(args.text, model, tokenizer, args.max_new_tokens, args.do_sample, args.top_p, args.temperature)

if __name__ == "__main__":
    main()
