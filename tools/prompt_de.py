"""Print the prompt (first code block) under a '## <ID>' heading of a prompts markdown file.

Usage:
  python tools/prompt_de.py "Criativo NN/prompts_imagens.md" H1
"""
import pathlib
import re
import sys

md = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
sec = re.search(r"^## " + re.escape(sys.argv[2]) + r"\b.*?```\n(.*?)```", md, re.S | re.M)
if not sec:
    sys.exit(f"section '## {sys.argv[2]}' with a code block not found")
print(sec.group(1).strip())
