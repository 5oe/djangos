def format_variable(field_name):
    # 格式化 变量名
    # CharField -->  create_char_field
    if field_name == 'ForeignKey':
        return 'create_foreign_key'
    i = field_name.find('Field')
    s = field_name[:i]  # Integer Char
    s = s.lower()
    return '_'.join(['create', s, 'field'])


if __name__ == '__main__':
    print(format_variable('DateTimeField'))
