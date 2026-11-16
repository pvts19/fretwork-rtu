import sys
from pathlib import Path

# Корень проекта в sys.path, чтобы тесты видели модули places, visits и т. д.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
