# Write by GPT-4o mini🧙‍♂️, scillidan🤡
# Usage: python html2ansi.py <input_file> <output_file>

import sys
import re

def process_text(text):
    replacements = {
        '<i class="pos grammar">': "\033[3m",
        "</i>": "\033[0m",
        '<small class="co">': "\033[2m",
        "</small>": "\033[0m",
        '<cite class="ex">': "\033[3m",
        "</cite>": "\033[0m",
        "<br />": r"\n",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    def replace_link(match):
        href = match.group(1)
        inner_text = match.group(2)
        return f"\033[4;34m{inner_text}\033[0m"

    text = re.sub(r'<a\s+href="([^"]*)">([^<]*)</a>', replace_link, text)

    return text

def main():
	if len(sys.argv) != 3:
		print("Usage: python cli.py input output")
		sys.exit(1)
	input_file = sys.argv[1]
	output_file = sys.argv[2]

	with open(input_file, "r", encoding="utf-8") as f:
		content = f.read()

	processed = process_text(content)

	with open(output_file, "w", encoding="utf-8") as f:
		f.write(processed)

if __name__ == "__main__":
	main()
