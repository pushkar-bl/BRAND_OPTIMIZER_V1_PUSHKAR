# BRAND_OPTIMIZER_V1_PUSHKAR

This repository contains a Python-based pipeline for generating optimized brand-related text variants using OpenAI’s GPT models.  
The system processes structured JSON inputs, generates multiple textual variants, and stores all outputs in a designated folder for further analysis.

---

## 🧩 Overview

The code accepts a JSON file as input, processes each entry through a chosen model (e.g., GPT-4.1), and produces a set of textual variants.  
This is particularly useful for marketing optimization, product description testing, and generative text benchmarking.

---

## ⚙️ Installation

To install all required dependencies, please use the `requirements.txt` file provided in this repository.

Run the following command:

```bash
pip install -r requirements.txt
```
The project also requires an OpenAI-api key
## Input
A sample input file is provided in:
```
sample_inputs/RIDGE_INPUTS.json
```
## Running the script
Use the following command to run the script 
``` bash
python -m main.py --input sample_inputs/RIDGE_INPUTS.json --n_variants 10 --model gpt-4.1
```

## Output 
All generated files are automatically stored in the outputs/ directory.
Each run produces a timestamped JSON file that contains the generated text variants, along with metadata such as the model used, the number of variants, and the original input.
