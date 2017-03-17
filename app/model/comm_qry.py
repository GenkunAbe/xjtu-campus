# -*- coding: utf-8 -*-

import sys
from datetime import date

def get_now_week():
    delta = date.today() - date(2017, 2, 20)
    return int(delta.days / 7 + 1)

if __name__ == '__main__':
    print(get_now_week())