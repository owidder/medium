from insert_in_file_module.textfsm_with_line_numbers import TextFSM_with_line_numbers
from io import StringIO

FSM_TEMPLATE = """
Start
  ^http.* -> HttpSection
  
HttpSection
  ^\s+server.* -> ServerSection
  
ServerSection
  ^\s+location.* -> Record
"""

NEW_LOCATION_LINES = """
        location ~ \.(gif|jpg|png)$ {
            root /data/images;
        }
"""

textfsm_with_line_numbers = TextFSM_with_line_numbers(StringIO(FSM_TEMPLATE))
with open("./nginx.conf") as nginx_read:
    content = nginx_read.read()
    fsm_result = textfsm_with_line_numbers.ParseText(content)
    line_number = int(fsm_result[0][0])
    content_lines = content.split("\n")
    content_lines.insert(line_number - 1, NEW_LOCATION_LINES)

with open("./nginx.conf", "w") as nginx_write:
    nginx_write.write("\n".join(content_lines))
