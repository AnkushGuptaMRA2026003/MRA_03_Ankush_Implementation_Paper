"""
scripts/check_env.py
Environment verification script. Run this first to confirm all dependencies are installed.
Author: Ankush Gupta (MRA2026003)

Usage:
    python scripts/check_env.py
"""

import sys

REQUIRED = [
    "transformers",
    "sentence_transformers",
    "torch",
    "faiss",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "yaml",
    "requests",
    "rouge_score",
    "bert_score",
    "tqdm",
    "dotenv",
]

print("=" * 50)
print("Environment Verification — AITR Lab02")
print(f"Python: {sys.version}")
print("=" * 50)

all_ok = True
for pkg in REQUIRED:
    try:
        mod = __import__(pkg)
        version = getattr(mod, "__version__", "unknown")
        print(f"  ✓  {pkg:<30} {version}")
    except ImportError:
        print(f"  ✗  {pkg:<30} NOT INSTALLED")
        all_ok = False

print("=" * 50)
if all_ok:
    print("All dependencies OK.")
else:
    print("Some dependencies missing. Run: pip install -r requirements.txt")

# Check CUDA
try:
    import torch
    cuda_ok = torch.cuda.is_available()
    print(f"CUDA available: {cuda_ok}")
    if cuda_ok:
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
except Exception as e:
    print(f"CUDA check failed: {e}")
