import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class AgentBase:
    def __init__(self, agent_config):
        self.agent_config = agent_config
        self.name = self.__class__.__name__.replace("Agent", "")  # e.g. "FactualityAgent" -> "Factuality"
        model_path = os.path.join(agent_config["model_path"], agent_config["model_name"])
        dtype = getattr(torch, agent_config.get("dtype", "float16"))
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map=agent_config.get("device_map", "auto"),
            torch_dtype=dtype,
        )
        self.generation_config = agent_config.get("generation", {})

    def chat_completion(self, messages, temperature=None, top_p=None, max_new_tokens=None):
        # Use agent defaults unless overridden by function call
        temperature = temperature if temperature is not None else self.generation_config.get("temperature", 0.0)
        top_p = top_p if top_p is not None else self.generation_config.get("top_p", None)
        max_new_tokens = max_new_tokens if max_new_tokens is not None else self.generation_config.get("max_new_tokens", 256)

        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        do_sample = temperature > 0.0
        gen_kwargs = dict(
            max_new_tokens=max_new_tokens,
            pad_token_id=self.tokenizer.eos_token_id,
            do_sample=do_sample,
        )
        if do_sample:
            gen_kwargs["temperature"] = temperature
            if top_p is not None:
                gen_kwargs["top_p"] = top_p
        else:
            gen_kwargs["temperature"] = None
            gen_kwargs["top_p"] = None
        output_ids = self.model.generate(**inputs, **gen_kwargs)
        answer_ids = output_ids[0, inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(answer_ids, skip_special_tokens=True).strip()
