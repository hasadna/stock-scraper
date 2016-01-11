import numbers


def cast_to_num(str):
    if isinstance(str, numbers.Number):
        return str

    if ',' in str:
        str = ''.join([s for s in list(str) if s.isdigit()])

    try:
        return float(str) if '.' in str else int(str)
    except Exception as e:
        return None