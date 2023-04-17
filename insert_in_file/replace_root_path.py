from insert_in_file_module.textfsm_with_line_numbers import TextFSM_with_line_numbers
from io import StringIO

TEMPLATE = """
Start
  ^\s+location ~ .*images.* -> LocationSection

LocationSection
  ^\s+root.* -> Record
"""

textfsm_with_line_numbers = TextFSM_with_line_numbers(StringIO(TEMPLATE))
with open("./nginx.conf") as nginx_read:
    content = nginx_read.read()
    fsm_result = textfsm_with_line_numbers.ParseText(content)
    line_number = int(fsm_result[0][0])
    content_lines = content.split("\n")
    content_lines[line_number-1] = "      root    /var/www/virtual/newimages.server.com/htdocs;"
    print("\n".join(content_lines))

with open("./nginx.conf", "w") as nginx_write:
    nginx_write.write("\n".join(content_lines))
