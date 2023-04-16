import textfsm
import re, io


def read_file_with_line_numbers(filename: str):
    with open(filename) as inputfile:
        lines = inputfile.readlines()
        modified = [f"_{idx+1}_{line}" for idx, line in enumerate(lines)]
        modified.append(f"_{len(lines)+1}_\n")
        return "".join(list(modified))


def add_line_number_rules_to_template(template: str):
    modified = [
        line.replace("^", "^_${Linenum}_", 1)
        if re.match(r"^\s*\^.*$", line)
        else line
        for line in template
    ]
    modified.insert(0, "Value Required Linenum (\\d+)\n")
    return "".join(modified)


class Can_not_insert_line_exception(Exception):
    pass


def find_line_to_insert(fsm_results: list, key_to_insert: str) -> (int, bool, bool):
    for _index, element in enumerate(fsm_results):
        if len(element) == 1 or element[1].lower().strip().startswith(key_to_insert.lower()):
            return (int(element[0]), False, True)
        elif element[1].lower() > key_to_insert.lower():
            return (int(element[0]), False, False)
        elif len(element[1]) == 0:
            return (int(element[0]), True, False)

    raise Can_not_insert_line_exception()


def insert_into_file_with_template_and_key(
    file_path: str,
    template: str,
    key_to_insert: str,
    text_to_insert: str,
    offset = 1,
):
    file_content = read_file_with_line_numbers(file_path)
    template_with_line_number_rules = add_line_number_rules_to_template(template)
    fsm = textfsm.TextFSM(io.StringIO(template_with_line_number_rules))
    fsm_result = fsm.ParseText("".join(file_content))
    line_to_insert, end_marker_found, same_line = find_line_to_insert(fsm_result, key_to_insert)
    text_to_insert_with_cr = text_to_insert if text_to_insert.endswith("\n") else text_to_insert + "\n"
    with open(file_path, "r") as read_file:
        lines = read_file.readlines()
        if line_to_insert is not None:
            if same_line:
                number_of_lines_to_insert = len(text_to_insert.split("\n"))
                lines[line_to_insert-1:line_to_insert+number_of_lines_to_insert-1] = text_to_insert_with_cr
            else:
                lines.insert(line_to_insert - (1 if end_marker_found else offset), text_to_insert_with_cr)

    with open(file_path, "w") as write_file:
        write_file.write("".join(lines))
