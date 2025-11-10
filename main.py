from data_loader import load_inputs, preview_page
from generator import generate_page_variants
from config import DEFAULT_MODEL
import argparse


def main():
    # -----------------------------
    # 🧠 Define CLI arguments
    # -----------------------------
    parser = argparse.ArgumentParser(
        description="Generate LLM-optimized webpage variants for a given brand."
    )

    parser.add_argument(
        "--input",
        type=str,
        default="sample_inputs/RIDGE_INPUTS.json",
        help="Path to the JSON input file (default: sample_inputs/RIDGE_INPUTS.json)",
    )

    parser.add_argument(
        "--n_variants",
        type=int,
        default=5,
        help="Number of page variants to generate (default: 5)",
    )

    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"OpenAI model to use (default: {DEFAULT_MODEL})",
    )

    parser.add_argument(
        "--preview_only",
        action="store_true",
        help="If set, only print preview info without generating variants.",
    )

    args = parser.parse_args()

    # -----------------------------
    # 📥 Load and preview data
    # -----------------------------
    config = load_inputs(args.input)
    preview_page(config)

    if args.preview_only:
        print("\n🟢 Preview only — no variants generated.")
        return

    # -----------------------------
    # ⚙️ Generate variants
    # -----------------------------
    variants = generate_page_variants(
        brand_name=config["brand_name"],
        original_page_text=config["page_text"],
        qa_pairs=config["qa_pairs"],
        n_variants=args.n_variants,
        model=args.model,
    )

    print(f"\n✅ Done! Generated {len(variants)} variants.")

if __name__ == "__main__":
    main()
