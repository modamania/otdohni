# encoding: utf-8
from settings import *

SITE_ID = 13
KEY_PREFIX = 'ekb_'

MAINMENU = [
    {'title': u'Афиша', 'url': reverse_lazy('event_list')},
    {'title': u'Места отдыха', 'url': reverse_lazy('place_list')},
    {'title': u'Фото', 'url': reverse_lazy('photoreport_list')},
    {'title': u'Конкурсы', 'url': reverse_lazy('action_list')},
    {'title': u'Новости', 'url': reverse_lazy('news_list')},
    {'title': u'Чай со звездой', 'url': reverse_lazy('overview_tea'), 'css_classes': 'menu_main__link_tea'},
    {'title': u'Хобби', 'url': '/hobbi/'},
    {'title': u'Доставка еды', 'url': '/dostavka_edy/'},
    {'title': u'Такси', 'url': '/taxi/'},
    {'title': u'Всё для праздника', 'url': '/holiday/'},
    #{'title': u'Бизнес-ланч', 'url': reverse_lazy('lunch_list')},
    #{'title': u'Авто', 'url': '/avto/'},
    #{'title': u'Скидки', 'url': '/sales/', 'css_classes': 'menu_main__link_sales'},
    #{'title': u'Академия', 'url': reverse_lazy('overview_tea'),
    #    'css_classes': 'm_academia'},
]
