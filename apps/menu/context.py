from menu import menu
from menu.submenu import Submenu


def generate_menu(request):
    submenu = Submenu()
    menu.submenu = None
    for item in menu.mainmenu:
        url = unicode(item.url) #Convert reverse_lazy() to unicode string
        if request.path == url or request.path.startswith(url) and url != '/':
            item.is_active = True
            try:
                menu.submenu = getattr(submenu, item.name)
            except AttributeError:
                pass
            else:
                menu.submenu = menu.submenu()
        else:
            item.is_active = False
    if menu.submenu:
        for item in menu.submenu:
            if request.path == url:
                item.is_active = True
            else:
                item.is_active = False
    return {'menu': menu}
