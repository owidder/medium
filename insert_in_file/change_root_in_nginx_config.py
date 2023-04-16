from .insert_in_file import insert_into_file_with_template_and_key


TEMPLATE = """
Start
  ^\s+location ~ \^/(images.*: -> LocationSection

LocationSection
  ^\s+root.* -> Record
  ^\s*}\s*$$ -> EOF
"""


insert_into_file_with_template_and_key(
    file_path="./nginx.conf",
    template=TEMPLATE,
    key_to_insert="root",
    text_to_insert="      root    /var/www/virtual/newbig.server.com/htdocs;"
)
