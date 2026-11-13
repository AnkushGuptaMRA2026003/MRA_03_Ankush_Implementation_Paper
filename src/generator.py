"""
src/generator.py
Generates literature reviews using a frozen LLM baseline.
Author: Ankush Gupta (MRA2026003)
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import Optional


BASELINE_PROMPT = (
    'Write a 200-word academic literature review on the topic: "{topic}".\n'
    "Include exactly 5 citations in [Author et al., Year] format.\n"
    "Focus on key papers from 2020 onwards."
)

RAG_PROMPT = (
    "Using the following recent papers as context:\n{retrieved_papers}\n\n"
    'Write a 200-word academic literature review on the topic: "{topic}".\n'
    "Include exactly 5 citations in [Author et al., Year] format, preferring the provided papers."
)


def load_model(model_name: str = "meta-llama/Llama-3.1-8B-Instruct", quantize: bool = True):
    """Load model and tokenizer. Uses 4-bit quantization by default."""
    kwargs = {}
    if quantize:
        from transformers import BitsAndBytesConfig
        bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
        kwargs["quantization_config"] = bnb_config

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        **kwargs,
    )
    model.eval()
    return model, tokenizer


def generate_literature_review(
    topic: str,
    model,
    tokenizer,
    retrieved_papers: Optional[str] = None,
    temperature: float = 0.3,
    max_new_tokens: int = 400,
    seed: int = 42,
) -> str:
    """
    Generate a literature review for the given topic.

    Args:
        topic: Research topic string.
        model: HuggingFace CausalLM model.
        tokenizer: Corresponding tokenizer.
        retrieved_papers: If provided, uses RAG prompt with these papers as context.
        temperature: Sampling temperature.
        max_new_tokens: Maximum tokens to generate.
        seed: Random seed for reproducibility.

    Returns:
        Generated literature review string.
    """
    torch.manual_seed(seed)

    if retrieved_papers:
        prompt = RAG_PROMPT.format(topic=topic, retrieved_papers=retrieved_papers)
    else:
        prompt = BASELINE_PROMPT.format(topic=topic)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decode only newly generated tokens (not the prompt)
    generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(generated_ids, skip_special_tokens=True)
