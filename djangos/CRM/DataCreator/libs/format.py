def format_variable(field_name):
    # 格式化 变量名
    # CharField -->  create_char_field
    i = field_name.find('Field')
    s = field_name[:i]  # Integer Char
    s = s.lower()
    return '_'.join(['create', s, 'field'])
