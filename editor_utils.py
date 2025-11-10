import copy
import json
from typing import List, Dict, Any

def apply_edit_plan_to_page(page_text: str, plan: Dict[str, Any]) -> str:
    lines = page_text.splitlines()
    lines_mod = copy.deepcopy(lines)

    # --- Deletions ---
    for delete in plan.get("deletes", []):
        anchor = delete.get("anchor_substring", "").strip()
        if not anchor:
            continue
        for idx, line in enumerate(lines_mod):
            if anchor in line:
                lines_mod.pop(idx)
                break

    # --- Edits ---
    for edit in plan.get("edits", []):
        anchor = edit.get("anchor_substring", "").strip()
        replacement_line = edit.get("replacement_line", "").rstrip("\n")
        if not anchor or not replacement_line:
            continue
        for idx, line in enumerate(lines_mod):
            if anchor in line:
                lines_mod[idx] = replacement_line
                break

    # --- Additions ---
    for add in plan.get("adds", []):
        position = add.get("position", "end").lower().strip()
        anchor = add.get("anchor_substring", "").strip()
        new_line = add.get("new_line", "").rstrip("\n")
        if not new_line:
            continue

        if position == "end" or not anchor:
            lines_mod.append(new_line)
            continue

        for idx, line in enumerate(lines_mod):
            if anchor in line:
                if position == "before":
                    lines_mod.insert(idx, new_line)
                elif position == "after":
                    lines_mod.insert(idx + 1, new_line)
                break
        else:
            lines_mod.append(new_line)

    return "\n".join(lines_mod)


def summarize_qa_pairs(qa_pairs: List[Dict[str, str]], max_chars: int = 6000) -> str:
    chunks, running_len = [], 0
    for i, qa in enumerate(qa_pairs, start=1):
        block = f"Q{i}: {qa['question']}\nA{i}: {qa['llm_answer']}\n\n"
        if running_len + len(block) > max_chars:
            break
        chunks.append(block)
        running_len += len(block)
    return "".join(chunks)
import copy
import json
from typing import List, Dict, Any

def apply_edit_plan_to_page(page_text: str, plan: Dict[str, Any]) -> str:
    lines = page_text.splitlines()
    lines_mod = copy.deepcopy(lines)

    # --- Deletions ---
    for delete in plan.get("deletes", []):
        anchor = delete.get("anchor_substring", "").strip()
        if not anchor:
            continue
        for idx, line in enumerate(lines_mod):
            if anchor in line:
                lines_mod.pop(idx)
                break

    # --- Edits ---
    for edit in plan.get("edits", []):
        anchor = edit.get("anchor_substring", "").strip()
        replacement_line = edit.get("replacement_line", "").rstrip("\n")
        if not anchor or not replacement_line:
            continue
        for idx, line in enumerate(lines_mod):
            if anchor in line:
                lines_mod[idx] = replacement_line
                break

    # --- Additions ---
    for add in plan.get("adds", []):
        position = add.get("position", "end").lower().strip()
        anchor = add.get("anchor_substring", "").strip()
        new_line = add.get("new_line", "").rstrip("\n")
        if not new_line:
            continue

        if position == "end" or not anchor:
            lines_mod.append(new_line)
            continue

        for idx, line in enumerate(lines_mod):
            if anchor in line:
                if position == "before":
                    lines_mod.insert(idx, new_line)
                elif position == "after":
                    lines_mod.insert(idx + 1, new_line)
                break
        else:
            lines_mod.append(new_line)

    return "\n".join(lines_mod)


def summarize_qa_pairs(qa_pairs: List[Dict[str, str]], max_chars: int = 6000) -> str:
    chunks, running_len = [], 0
    for i, qa in enumerate(qa_pairs, start=1):
        block = f"Q{i}: {qa['question']}\nA{i}: {qa['llm_answer']}\n\n"
        if running_len + len(block) > max_chars:
            break
        chunks.append(block)
        running_len += len(block)
    return "".join(chunks)
