def get_splitter(filename: str):
    for char in filename:
        if char in ('-', '–', '—', '/'):
            return char
    return '  '

    # return '-' if '-' in filename else '–' if '–' in filename else '—' if '—' in filename else '/' if '/' in filename else '  '