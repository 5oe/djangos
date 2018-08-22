def is_isbn_or_key(word):
    if '-' not in word:
        ret = 'isbn' if len(word) == 13 and word.isdigit() else 'key'
    else:
        short_word = word.replace('-', '')
        ret = 'isbn' if len(short_word) == 10 and short_word.isdigit() else 'key'
    return ret
