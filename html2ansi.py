# Usage: python file.py <input_file> <output_file>

import sys
import re

def html_to_ansi(text):
    replacements = {
        "<br>": r"\n",
        '<i>': "\033[3m",
        "</i>": "\033[0m",
        '<small>': "\033[2m",
        "</small>": "\033[0m",
        '<font style="color:green">': "\033[32m",
        "</font>": "\033[0m",
    }

    for html, ansi in replacements.items():
        text = text.replace(html, ansi)

    # Replace an HTML link tag with ANSI-escaped underlined blue text
    def html_to_ansi_link(match):
        a_tag = match.group(1)
        text_inner = match.group(2)
        return f"\033[4;34m{text_inner}\033[0m"

    # Replace all HTML anchor tags with ANSI-escaped text
    text = re.sub(r'<a\s+href="([^"]*)">([^<]*)</a>', html_to_ansi_link, text)

    return text

def main():
    if len(sys.argv) != 3:
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.read()

    formatted_lines = html_to_ansi(lines)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(formatted_lines)

if __name__ == "__main__":
    main()
