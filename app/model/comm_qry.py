# -*- coding: utf-8 -*-

import sys
from datetime import date

def get_now_week():
    delta = date.today() - date(2016, 9, 5)
    return delta.days / 7 + 1

if __name__ == '__main__':
    print get_now_week()