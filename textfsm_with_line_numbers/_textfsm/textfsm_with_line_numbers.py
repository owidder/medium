from textfsm import TextFSM
from io import StringIO
import re


def add_line_numbers_to_text(text: str):
    lines = text.split("\n")
    modified = [f"_{idx+1}_{line}\n" for idx, line in enumerate(lines)]
    modified.append(f"_{len(lines)+1}_\n")
    return "".join(list(modified))


def add_line_number_rules_to_template(template: str):
    modified = [
        line.replace("^", "^_${Linenum}_", 1)
        if re.match(r"^\s*\^.*$", line)
        else line
        for line in template.split("\n")
    ]
    modified.insert(0, "Value Required Linenum (\\d+)\n")
    return "\n".join(modified)


class TextFSM_with_line_numbers(TextFSM):
    def __init__(self, template: StringIO):
        template_str = template.getvalue()
        TextFSM.__init__(self, StringIO(add_line_number_rules_to_template(template_str)))

    def ParseText(self, text, eof=True):
        text_with_line_numbers = add_line_numbers_to_text(text)
        return TextFSM.ParseText(self, text=text_with_line_numbers, eof=eof)

