# Usage: python file.py <input> <output>

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
    # Replace <cite class="ex"></cite> with <font style="color:green"></font>
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

def format(line):
    if '\t' not in line:
        return line.strip()
    parts = line.split('\t', 1)
    word = parts[0]
    meaning = parts[1].strip()

    meaning = match_remove(meaning)
    meaning = match_replace(meaning)
    meaning = match_convert(meaning)
    meaning = unescape(meaning)
    meaning = meaning.strip()

    result = f"{word}\t{meaning}"
    return result

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input> <output>")
        sys.exit(1)
    input = sys.argv[1]
    output = sys.argv[2]

    with open(input, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    results = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        result = format(stripped)
        results.append(result)

    with open(output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))

if __name__ == '__main__':
    main()
