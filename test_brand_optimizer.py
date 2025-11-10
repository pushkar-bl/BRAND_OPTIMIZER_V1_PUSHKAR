"""
test_brand_optimizer.py
Combined test suite for the brand optimizer (single-file version)
Run with:  pytest -v test_brand_optimizer.py
"""

import os
import json
import tempfile
from data_loader import load_inputs
from editor_utils import apply_edit_plan_to_page
from generator import generate_page_variants
# ------------------------------
# 🧪 Helper: create temp input JSON
# ------------------------------
def make_temp_input():
    ridge_data = {
        "brand_name": "Ridge",
        "url": "https://ridge.com/collections/wallets",
        "page_text": "RIDGE WALLETS, Metal, RFID-blocking wallets designed to carry cards and cash safely and securely.\n\n**DURABLE DESIGN** Chosen with care to last a lifetime.",
        "qa_pairs": [
            {
                "question": "Which wallet brand is durable?",
                "llm_answer": "Ridge Wallet is built from aluminum and titanium for long life."
            }
        ]
    }
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    with open(tmpfile.name, "w", encoding="utf-8") as f:
        json.dump(ridge_data, f, indent=2)
    return tmpfile.name


# ------------------------------
# ✅ Test 1: load_inputs
# ------------------------------
def test_load_inputs():
    path = make_temp_input()
    cfg = load_inputs(path)
    assert cfg["brand_name"] == "Ridge"
    assert "qa_pairs" in cfg
    os.remove(path)


# ------------------------------
# ✅ Test 2: apply_edit_plan_to_page
# ------------------------------
def test_apply_edit_plan_to_page():
    page = "Line1\nLine2\nLine3"
    plan = {
        "adds": [{"position": "after", "anchor_substring": "Line2", "new_line": "Added line"}],
        "deletes": [{"anchor_substring": "Line1"}],
        "edits": [{"anchor_substring": "Line3", "replacement_line": "Edited Line3"}]
    }
    new_page = apply_edit_plan_to_page(page, plan)

    assert "Line1" not in new_page
    assert "Added line" in new_page
    assert "Edited Line3" in new_page


# ------------------------------
# ✅ Test 3: generate_page_variants (mocked)
# ------------------------------
def test_generate_page_variants(monkeypatch):
    # Create a dummy input
    brand_name = "TestBrand"
    page_text = "Original text"
    qa_pairs = [{"question": "Q?", "llm_answer": "A."}]

    # Mock OpenAI API call so it doesn't hit the real API
    def mock_request(*args, **kwargs):
        return {
            "hypothesis_name": "Mock Hypothesis",
            "hypothesis_rationale": "Fake rationale",
            "adds": [],
            "deletes": [],
            "edits": []
        }

    monkeypatch.setattr("brand_optimizer_single.request_edit_plan_from_llm", mock_request)

    variants = generate_page_variants(
        brand_name=brand_name,
        original_page_text=page_text,
        qa_pairs=qa_pairs,
        n_variants=2,
        model="mock-model"
    )

    assert len(variants) == 2
    assert variants[0]["hypothesis_name"] == "Mock Hypothesis"
    assert "page_text" in variants[0]


# ------------------------------
# ✅ Optional: clean up
# ------------------------------
def teardown_module(module):
    """Remove generated outputs after tests."""
    if os.path.exists("outputs/TestBrand_variants.json"):
        os.remove("outputs/TestBrand_variants.json")
