import json
from typing import Any, Dict, List
from editor_utils import apply_edit_plan_to_page
from llm_client import request_edit_plan_from_llm
import os
from config import OUTPUT_DIR

def generate_page_variants(brand_name: str, original_page_text: str, qa_pairs: List[Dict[str, str]], n_variants: int = 25, model: str = "gpt-4.1-mini") -> List[Dict[str, Any]]:
    used_hypotheses, variants = [], []

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i in range(1, n_variants + 1):
        print(f"\n=== Generating variant {i}/{n_variants} ===")
        plan = request_edit_plan_from_llm(brand_name, original_page_text, qa_pairs, used_hypotheses, model=model)
        hypothesis_name = plan.get("hypothesis_name", f"variant_{i}")
        hypothesis_rationale = plan.get("hypothesis_rationale", "")

        used_hypotheses.append({"hypothesis_name": hypothesis_name, "hypothesis_rationale": hypothesis_rationale})
        new_page_text = apply_edit_plan_to_page(original_page_text, plan)

        variants.append({
            "variant_id": i,
            "hypothesis_name": hypothesis_name,
            "hypothesis_rationale": hypothesis_rationale,
            "edit_plan": plan,
            "page_text": new_page_text
        })

    output_path = os.path.join(OUTPUT_DIR, f"{brand_name}_variants.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(variants, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Saved all {len(variants)} variants to {output_path}")
    return variants
