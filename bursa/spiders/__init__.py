#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

def get_boolean_value(str):
    value = None
    if str == u'כן':
        value = True
    elif str == u'לא':
        value = False

    return value

def remove_dash(str):
    return None if str.strip() == '-' else str