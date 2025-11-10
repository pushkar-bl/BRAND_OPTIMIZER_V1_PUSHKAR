import json
import textwrap
from openai import OpenAI
from typing import Any, Dict, List
from editor_utils import summarize_qa_pairs
from config import OPENAI_API_KEY, DEFAULT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def build_edit_prompt(brand_name: str, page_text: str, qa_pairs: List[Dict[str, str]], used_hypotheses: List[Dict[str, str]]) -> Dict[str, str]:
    qa_summary = summarize_qa_pairs(qa_pairs, max_chars=5000)
    previous_hypotheses_txt = json.dumps(used_hypotheses, indent=2, ensure_ascii=False) if used_hypotheses else "[]"

    system_msg = textwrap.dedent(f"""
    You are a senior content editor and marketer at {brand_name}.
    Your job is to propose extremely lightweight edits to our existing web page so that
    large language models (LLMs) rank {brand_name} higher and describe it more
    positively in their answers to customer questions.
    STRICT RULES: ... (same as your original code)
    """)

    user_msg = textwrap.dedent(f"""
    Here are example customer questions:
    {qa_summary}
    <PAGE_START>
    {page_text}
    <PAGE_END>
    Output valid JSON only.
    """)

    return {"system": system_msg, "user": user_msg}


def request_edit_plan_from_llm(brand_name: str, page_text: str, qa_pairs: List[Dict[str, str]], used_hypotheses: List[Dict[str, str]], model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    messages = build_edit_prompt(brand_name, page_text, qa_pairs, used_hypotheses)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": messages["system"]},
            {"role": "user", "content": messages["user"]}
        ],
    )
    raw_text = response.output_text.strip()
    try:
        plan = json.loads(raw_text)
    except json.JSONDecodeError:
        start, end = raw_text.find("{"), raw_text.rfind("}")
        if start != -1 and end != -1:
            plan = json.loads(raw_text[start:end+1])
        else:
            raise ValueError("Invalid JSON from model output")
    for key in ["adds", "deletes", "edits"]:
        plan.setdefault(key, [])
        plan[key] = plan[key][:3]
    return plan
