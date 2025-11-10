import json
from typing import List, Dict, Any
import os

def load_inputs(input_path: str) -> Dict[str, Any]:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

def preview_page(config: Dict[str, Any]):
    print("Brand:", config["brand_name"])
    print("Num QA pairs:", len(config["qa_pairs"]))
    print("Page preview (first 20 lines):")
    for i, line in enumerate(config["page_text"].splitlines()[:20]):
        print(f"{i:>3}: {line}")