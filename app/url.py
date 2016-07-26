# -*- coding: utf-8 -*-

from ctrl.grade import GradeCtrl
from ctrl.table import TableCtrl
from ctrl.library import LibraryCtrl
from ctrl.card import CardCtrl
from ctrl.net import NetCtrl
from ctrl.news import NewsCtrl

url = [
    (r'/grade', GradeCtrl),
    (r'/table', TableCtrl),
    (r'/library', LibraryCtrl),
    (r'/card', CardCtrl),
    (r'/net', NetCtrl),
    (r'/news', NewsCtrl),
]