from insert_in_file_module.textfsm_with_line_numbers import TextFSM_with_line_numbers
from io import StringIO

TEMPLATE = """
Start
  ^\s+location ~ .*images.* -> LocationSection

LocationSection
  ^\s+root.* -> Record
  ^\s*}\s*$$ -> EOF
"""

textfsm_with_line_numbers = TextFSM_with_line_numbers(StringIO(TEMPLATE))
with open("./nginx.conf") as nginx:
    print(textfsm_with_line_numbers.ParseText(nginx.read()))
