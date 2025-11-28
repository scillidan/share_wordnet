# Write by GPT-4o mini🧙‍♂️, scillidan🤡
# Usage: python text_format.py <input_file> <output_file>

import sys
import re
from html import unescape

def remove_h1(text):
	return re.sub(r'<h1>.*?</h1>', '', text, flags=re.DOTALL | re.IGNORECASE)

def remove_span_tags(text):
	return re.sub(r'</?span[^>]*>', '', text, flags=re.IGNORECASE)

def normalize_br_tags(text):
	return re.sub(r'<br\s*/?>', '<br />', text, flags=re.IGNORECASE)

def convert_newline_to_br(text):
	text = text.replace('\\n', '\n')
	lines = text.splitlines()
	text = '<br />'.join(line.strip() for line in lines if line.strip() != '')
	text = re.sub(r'(<br\s*/?>\s*)+', '<br />', text)
	return text

def flatten_ol_lists(text):
    def repl(match):
        ol_content = match.group(1)
        items = re.findall(r'<li>(.*?)</li>', ol_content, flags=re.DOTALL | re.IGNORECASE)
        cleaned_items = [f"{i + 1}. {item.strip()}" for i, item in enumerate(items)]  # Numbering items
        return '<br />'.join(cleaned_items)  # Join with <br />

    return re.sub(r'<ol>(.*?)</ol>', repl, text, flags=re.DOTALL | re.IGNORECASE)

def remove_h1_span_ol_and_fix_breaks(text):
    text = remove_h1(text)
    text = remove_span_tags(text)
    text = flatten_ol_lists(text)
    text = normalize_br_tags(text)
    text = convert_newline_to_br(text)
    return text.strip()

def add_extra_br_before_i(text):
    # Add an extra <br /> before <i class="pos grammar"> tags if not already present twice
    # Replace every <br /><i ...> with <br /><br /><i ...>
    text = re.sub(r'(<br />)(\s*<i class="pos grammar"[^>]*>)', r'\1<br />\2', text, flags=re.IGNORECASE)
    return text

def process_line(line):
    if '\t' not in line:
        return line.strip()
    dict_word, html_content = line.split('\t', 1)
    processed_html = remove_h1_span_ol_and_fix_breaks(html_content)
    processed_html = unescape(processed_html)
    processed_html = re.sub(r'\s+', ' ', processed_html)
    processed_html = processed_html.strip()
    processed_html = add_extra_br_before_i(processed_html)
    return f"{dict_word}\t{processed_html}"

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
		processed_line = process_line(stripped)
		results.append(processed_line)

	with open(output_file, 'w', encoding='utf-8') as f_out:
		f_out.write('\n'.join(results))

if __name__ == '__main__':
	main()
