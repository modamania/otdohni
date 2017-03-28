# encoding: utf-8
from django.conf import settings

from models import Menu, MenuItem


menu = Menu()
menu.mainmenu = list()
for item in settings.MAINMENU:
    menu.mainmenu.append(MenuItem(item))

