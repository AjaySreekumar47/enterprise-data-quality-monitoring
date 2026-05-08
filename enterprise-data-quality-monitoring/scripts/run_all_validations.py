import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

validation_scripts = [
    ROOT_DIR / "scripts" / "validate_customer.py",
    ROOT_DIR / "scripts" / "validate_product.py",
    ROOT_DIR / "scripts" / "validate_sales.py",
]

for script in validation_scripts:
    print("\n" + "=" * 80)
    print(f"Running {script.name}")
    print("=" * 80)

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(ROOT_DIR),
    )

    if result.returncode != 0:
        raise RuntimeError(f"{script.name} failed with exit code {result.returncode}")

print("\n✅ All table validations completed successfully.")
print(f"📊 Open dashboard with: streamlit run streamlit_app/dashboard.py")