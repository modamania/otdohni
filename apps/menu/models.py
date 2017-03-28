class Menu(object):
    pass

class MenuItem(object):
    name = ''
    title = ''
    url = ''
    css_classes = ''
    is_active = False

    def __init__(self, *args, **kwargs):
        if not kwargs:
            for arg in args:
                if isinstance(arg, dict):
                    for prop in arg:
                        try:
                            setattr(self, prop, arg[prop])
                        except AttributeError:
                            raise TypeError("'%s' is an invalid keyword argument for this function" % arg)
        else:
            for prop in kwargs.keys():
                try:
                    setattr(self, prop, kwargs.pop(prop))
                except AttributeError:
                    raise TypeError("'%s' is an invalid keyword argument for this function" % prop)
