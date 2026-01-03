# Usage: python file.py <input> <output>

import sys
import re

def convert(text):
    replacements = {
        "<br>": r"\n",
        '<font style="color:green">': "\033[32m",
        "</font>": "\033[0m",
        '<i>': "\033[3m",
        "</i>": "\033[0m",
        '<small>': "\033[2m",
        "</small>": "\033[0m",
    }

    for html, ansi in replacements.items():
        text = text.replace(html, ansi)

    # Replace an HTML link tag with ANSI-escaped underlined blue text
    def convert_link(match):
        a_tag = match.group(1)
        text_inner = match.group(2)
        return f"\033[4;34m{text_inner}\033[0m"

    # Replace all HTML anchor tags with ANSI-escaped text
    text = re.sub(r'<a\s+href="([^"]*)">([^<]*)</a>', convert_link, text)

    return text

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input> <output>")
        sys.exit(1)
    input = sys.argv[1]
    output = sys.argv[2]

    convert(input, output)
    print(f"Conversion completed: {input} to {output}")

if __name__ == '__main__':
    main()
