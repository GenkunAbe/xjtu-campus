# -*- coding: utf-8 -*-

from ctrl.grade import GradeCtrl
from ctrl.table import TableCtrl
from ctrl.library import BookSearchCtrl
from ctrl.library import BookDetailCrtl

from ctrl.card import CardInfoCtrl
from ctrl.card import CardPreCtrl
from ctrl.card import CardPostCtrl

from ctrl.net import NetCtrl
from ctrl.news import NewsCtrl

url = [
    (r'/grade', GradeCtrl),
    (r'/table', TableCtrl),

    (r'/cardinfo', CardInfoCtrl),
    (r'/cardpre', CardPreCtrl),
    (r'/cardpost', CardPostCtrl),

    (r'/booksearch', BookSearchCtrl),
    (r'/bookdetail', BookDetailCrtl),

    (r'/net', NetCtrl),
    (r'/news', NewsCtrl),
]