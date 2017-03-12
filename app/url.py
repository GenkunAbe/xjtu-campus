# -*- coding: utf-8 -*-

from ctrl.auth import AuthCtrl

from ctrl.grade import GradeCtrl
from ctrl.table import TableCtrl
from ctrl.library import BookSearchCtrl
from ctrl.library import BookDetailCrtl

from ctrl.card import CardInfoCtrl
from ctrl.card import CardPayTestCtrl
from ctrl.card import CardPayCtrl

from ctrl.net import NetCtrl
from ctrl.news import NewsCtrl

from ctrl.common_query import CommonQuery

url = [
    (r'/auth', AuthCtrl),

    (r'/grade', GradeCtrl),
    (r'/table', TableCtrl),

    (r'/cardinfo', CardInfoCtrl),
    (r'/cardpay', CardPayCtrl),
    (r'/cardpaytest', CardPayTestCtrl), 

    (r'/booksearch', BookSearchCtrl),
    (r'/bookdetail', BookDetailCrtl),

    (r'/net', NetCtrl),
    (r'/news', NewsCtrl),

    (r'/commqry', CommonQuery),
    
]