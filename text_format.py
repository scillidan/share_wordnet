# Usage: python file.py <input_file> <output_file>

import sys
import re
from html import unescape

def match_remove(text):
    # Remove <h1></h1>
    text = re.sub(r'<h1>.*?</h1>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove <span ...></span>
    text = re.sub(r'</?span[^>]*>', '', text, flags=re.IGNORECASE)
    return text

def match_replace(text):
    # Replace <i class="pos grammar"> with <i>
    text = re.sub(r'<i[^>]*>', '<i>', text, flags=re.IGNORECASE)
    # Replace <small class="co"> with <small>
    text = re.sub(r'<small[^>]*>', '<small>', text, flags=re.IGNORECASE)
    # Replace <cite class="ex"></cite> with <u></u>
    # Replace <cite class="ex"> with <u> and </cite> with </u>
    text = re.sub(r'<cite\s+class="ex"[^>]*>', '<font style="color:green">', text, flags=re.IGNORECASE)
    text = re.sub(r'</cite>', '</font>', text, flags=re.IGNORECASE)
    # Replace \\n with <br>
    text = text.replace('\\n', '\n')
    lines = text.splitlines()
    text = '<br>'.join(line.strip() for line in lines if line.strip() != '')
    # Replace all variations of <br> tags with <br>
    text = re.sub(r'<br\s*/?>', '<br>', text, flags=re.IGNORECASE)
    # Replace repeated <br> with <br>
    text = re.sub(r'(<br>\s*)+', '<br>', text)
    return text

def match_convert(text):
    # Convert <ol></ol> to numbering list
    def repl(match):
        ol_tag = match.group(1)
        li_tag = re.findall(r'<li>(.*?)</li>', ol_tag, flags=re.DOTALL | re.IGNORECASE)
        cleaned_li_tag = [f"{i + 1}. {item.strip()}" for i, item in enumerate(li_tag)]
        return '<br><br>'.join(cleaned_li_tag)
    return re.sub(r'<ol>(.*?)</ol>', repl, text, flags=re.DOTALL | re.IGNORECASE)
    return text.strip()

def format_line(line):
    if '\t' not in line:
        return line.strip()
    parts = line.split('\t', 1)
    word_part = parts[0]
    meaning_part = parts[1].strip()

    meaning_part = match_remove(meaning_part)
    meaning_part = match_replace(meaning_part)
    meaning_part = match_convert(meaning_part)
    meaning_part = unescape(meaning_part)
    meaning_part = meaning_part.strip()

    formatted_line = f"{word_part}\t{meaning_part}"
    return formatted_line

def main():
	if len(sys.argv) != 3:
		print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
		sys.exit(1)
	input_file = sys.argv[1]
	output_file = sys.argv[2]

	with open(input_file, 'r', encoding='utf-8') as f:
		lines = f.readlines()

	results = []
	for line in lines:
		stripped = line.strip()
		if not stripped:
			continue
		formatted_line = format_line(stripped)
		results.append(formatted_line)

	with open(output_file, 'w', encoding='utf-8') as file_out:
		file_out.write('\n'.join(results))

if __name__ == '__main__':
	main()
