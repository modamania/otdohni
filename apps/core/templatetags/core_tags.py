# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site

from django.utils.safestring import mark_safe
from django import template
from django.conf import settings
from django.template import Node, NodeList, VariableDoesNotExist
from django.core.urlresolvers import NoReverseMatch
from django.templatetags.future import url
from django.template.defaulttags import TemplateIfParser

from datetime import datetime, date
import re
import urlparse
import os


register = template.Library()

months = settings.MONTHS.values()


@register.filter
def exclude_user(qs, user):
    return qs.exclude(id=user.id)


@register.filter
def format_date(dt, option=""):
    """
    Дата в формате '6 февр.'
    если год = текущему (иначе - в формате dd.mm.yyyy)
    Если есть время, выводится также и
    оно (а если дата - сегодня, выводится только время)
    """
    dt_str = ''
    today = tomorrow = False
    dt_now = datetime.now().date()
    if isinstance(dt, (date, datetime)):
        if isinstance(dt, datetime):
            dt_date = dt.date()
        else:
            dt_date = dt

        if dt_date == dt_now:
            today = True
        if (dt_date - dt_now).days == 1:
            tomorrow = True

        if dt.year == datetime.now().year:
            dt_str = '%s&nbsp;%s' % (dt.day, months[dt.month-1])
        else:
            dt_str = dt.strftime('%d.%m.%Y')

        if isinstance(dt, datetime):
            if today:
                dt_str = dt.strftime('%H:%M')
            elif option != 'short':
                dt_str += ' ' + dt.strftime('%H:%M')
        else:
            if today:
                dt_str = 'сегодня'
            if tomorrow:
                dt_str = 'завтра'
    else:
        dt_str = "&nbsp;"
    return mark_safe(dt_str)

"""
    Выделяет имя файла из пути
"""
@register.filter
def attach(path):
    return os.path.basename(path)

"""
    Размер файла в килобайтах
"""
@register.filter
def size_kb(attached_file):
    try:
        size = attached_file.size
        import math
        return "%s Кб" % (int(math.ceil(float(size)/1024)))
    except:
        return u'размер неизвестен'

"""
    Проверяет существование файла
"""
@register.filter
def is_file(path):
    return os.path.isfile(path)


@register.filter
def username(user):
    try:
        return "%s" % user.username
    except:
        return ""

"""
    Обрезает длинные строки
"""
@register.filter
def crop(text, count):
    out = text[:int(count)]
    if len(text) > len(out):
        out += '&hellip;'
    return mark_safe(out)

"""
    Замена '<' и '>' на '&lt;' и '&gt;' в html-тегах за исключением разрешенных;
    расстановка <br /> в конце строк за исключением текста внутри <pre>;
    форматирование списков: "- " в начале строки заменяется на тире.

    Разрешено: <a href="">, <b>, <i>, <pre> (для вставки кода)
"""
def sanitize_html(value):
    out = ''
    linebreaks = True
    lt = '&lt;'
    gt = '&gt;'

    value = re.sub('<', lt, value)
    value = re.sub('>', gt, value)

    # Сформировать теги по найденным совпадениям
    def href_subber(match):
        if re.search('javascript', match.group(2)):
            return '<a href="#">%s</a>' % (match.group(4))
        return '<a href="%s">%s</a>' % (match.group(2), match.group(4))
    def tag_subber(match):
        return '<%s>%s</%s>' % (match.group(1), match.group(2), match.group(1))

    # Ссылки
    href_re = re.compile(lt + '(a +href=")([^"]+)(" ?' + gt + ')' + '(.+?)' + lt + '/a' + gt, re.I)
    value = href_re.sub(href_subber, value)

    # Другие разрешенные теги.
    # Регистр игнорируется, а в тег pre может быть заключено несколько строк.
    for tag in ('b', 'i', 'pre'):
        opt = re.I
        if tag == 'pre':
            opt =  re.I | re.S
        tag_re = re.compile(lt + '(' + tag + ')' + gt + '(.*?)' + lt + '/' + tag + gt, opt)
        value = tag_re.sub(tag_subber, value)

    for line in value.split("\n"):
        if '<pre>' in line: linebreaks = False
        if '</pre>' in line: linebreaks = True

        if linebreaks:
            # В списках заменяем минус на тире
            line = re.sub('^- ', '&#151;&nbsp;', line)

            # Выделяем цветом цитаты (если есть '>' в начале строки)
            match = re.search('(^' + gt + '.*)', line)
            if match:
                line = '<span class="comment-quote">' + match.group(0) + '</span>'
            out += line + "<br />"
        else:
            # внутри тега pre заменяем угловые скобки на коды
            # это было сделано вначале, но затем была вставка разрешенных тегов, а они тут не нужны
            line = re.sub('<', lt, line)
            line = re.sub('>', gt, line)
            line = re.sub(lt + 'pre' + gt, '<pre>', line)
            out += line

    return mark_safe(out)
register.filter('sanitize', sanitize_html)

@register.filter
def in_list(value,arg):
    return value in arg

@register.filter
def render_paginator(page, seo=''):
    try:
        if not page.has_other_pages():
            return ''
        PAGINATOR_MAX_VISIBLE_PAGE = getattr(settings, 'PAGINATOR_MAX_VISIBLE_PAGE', 5)
        arrow = []
        context = []

        if seo.paginator.value:
            label = seo.paginator.value
        elif seo.heading.value:
            label = seo.heading.value
        else:
            label = ''
        label = label.encode('utf-8')

#        <div class="pager__prev-next">
#        {% if places.has_previous %}
#            <a href="?page={{ places.previous_page_number }}" class="pager__prev"><span class="arrow">←</span> сюда</a>
#        {% else %}
#            <span class="pager__prev disabled"><span class="arrow">←</span> сюда</span>
#        {% endif %}
#        {% if places.has_next %}
#            <a href="?page={{ places.next_page_number }}" class="pager__next">туда <span class="arrow">→</span></a>
#        {% else %}
#            <span class="pager__next disabled">туда <span class="arrow">→</span></span>
#        {% endif %}
#        </div>

        if page.has_previous():
            arrow.append('<a href="?page=%(number)d" class="pager__prev" title="%(label)s - страница %(number)d"><span class="arrow">←</span> сюда</a>' % {'label': label,'number': page.number - 1})
        else:
            arrow.append('<span class="pager__prev disabled"><span class="arrow">←</span> сюда</span>')

        if page.has_next():
            arrow.append('<a href="?page=%(number)d" class="pager__next" title="%(label)s - страница %(number)d">туда <span class="arrow">→</span></a>' % {'label': label,'number': page.number + 1})
        else:
            arrow.append('<span class="pager__next disabled">туда <span class="arrow">→</span></span>')

        #context.append('<h4 class="pagenav-title">%s %s:</h4>' % (category, site.city.name))
        #context.append('<h4 class="pagenav-title">%s:</h4>' % paginator_label)

        if page.number > PAGINATOR_MAX_VISIBLE_PAGE + 1:
            context.append('<a href="?page=1" class="pager__page" title="Первая страница">←</a>')

        start = page.number - PAGINATOR_MAX_VISIBLE_PAGE
        if start < 1:
            start = 1
        fin = page.number
        range_page = range(start, fin)
        for p in range_page:
            context.append('<a href="?page=%(number)d" class="pager__page" title="%(label)s - страница %(number)d">%(number)d</a>' % {'label': label, 'number': p})

        context.append('<span class="current">%d</span>' % page.number)

        start = page.number + 1
        fin = start + PAGINATOR_MAX_VISIBLE_PAGE
        if fin > page.paginator.num_pages + 1:
            fin = page.paginator.num_pages + 1
        range_page = range(start, fin)
        for p in range_page:
            context.append('<a href="?page=%(number)d" class="pager__page" title="%(label)s - страница %(number)d">%(number)d</a>' % {'label': label, 'number': p})

        if fin < page.paginator.num_pages + 1:
            context.append('<a href="?page=%d" class="pager__page" title="Последняя страница">→</a>' % page.paginator.num_pages)

        tpl = '<div class="pager"><div class="pager__prev-next">%s</div><div class="pager__pages"><h4 class="pagenav-title">%s:</h4>%s</div></div>' % (''.join(arrow), label, ''.join(context))
        return mark_safe(tpl)
    except:
        return ''

@register.filter
def urljoin(base, url):
    return urlparse.urljoin(base, url)


@register.inclusion_tag('pagination/pagination.html', takes_context=True)
def new_paginate(context, hashtag=''):

    try:
        paginator = context['paginator']
        seo = context['seo']
        page_obj = context['page_obj']
        records = {'first': 1 + (page_obj.number - 1) * paginator.per_page}
        records['last'] = records['first'] + paginator.per_page - 1
        if records['last'] + paginator.orphans >= paginator.count:
            records['last'] = paginator.count

        PAGINATOR_MAX_VISIBLE_PAGE = getattr(settings, 'PAGINATOR_MAX_VISIBLE_PAGE', 5)

        show_first = page_obj.number > PAGINATOR_MAX_VISIBLE_PAGE + 1

        start = page_obj.number - PAGINATOR_MAX_VISIBLE_PAGE

        start = 1 if start < 1 else start

        finish = page_obj.number
        s_range = range(start, finish)

        start = page_obj.number + 1
        finish = start + PAGINATOR_MAX_VISIBLE_PAGE
        if finish > paginator.num_pages +1:
            finish = paginator.num_pages +1

        e_range = range(start, finish)

        show_last = finish < paginator.num_pages +1

        pages = s_range + [None,] + e_range

        if seo.paginator.value:
            label = seo.paginator.value
        elif seo.heading.value:
            label = seo.heading.value
        else:
            label = ''
        #label = label.encode('utf-8')

        to_return = {
            'MEDIA_URL': settings.MEDIA_URL,
            'pages': pages,
            'records': records,
            'page_obj': page_obj,
            'paginator': paginator,
            'hashtag': hashtag,
            'show_first' : show_first,
            'show_last' : show_last,
            'is_paginated': paginator.count > paginator.per_page,
            'paginator_label' : label,
        }

        if 'request' in context:
            getvars = context['request'].GET.copy()
            if 'page' in getvars:
                del getvars['page']
            if len(getvars.keys()) > 0:
                to_return['getvars'] = "&%s" % getvars.urlencode()
            else:
                to_return['getvars'] = ''
        return to_return
    except (KeyError, AttributeError):
        return {}


class ActiveLinkNodeBase(Node):

    def __init__(self, urlnode, var_list, nodelist_true, nodelist_false):
        self.urlnode = urlnode
        self.var_list = var_list
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        try:
            var_list = self.urlnode.render(context)
        except NoReverseMatch:
            var_list = []
            for i in self.var_list:
                try:
                    var_list.append(i.eval(context))
                except VariableDoesNotExist:
                    var_list.append(None)

        request = context.get('request')

        # Gracefully fail if request is not in the context
        if not request:
            import warnings
            warnings.warn("The activelink templatetags require that a "
                          "'request' variable is available in the template's "
                          "context. Check you are using a RequestContext to "
                          "render your template, and that "
                          "'django.core.context_processors.request' is in "
                          "your TEMPLATE_CONTEXT_PROCESSORS setting"
            )
            return self.nodelist_false.render(context)

        try:
            equal = self.is_active(request, *var_list)
        except Exception:
            pass

        if equal:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


class ActiveLinkEqualNode(ActiveLinkNodeBase):

    def is_active(self, request, path_to_check):
        return path_to_check == request.path


class ActiveLinkStartsWithNode(ActiveLinkNodeBase):

    def is_active(self, request, path_to_check):
        return request.path.startswith(path_to_check)


class ActiveLinkEndsWithNode(ActiveLinkNodeBase):

    def is_active(self, request, path_to_check):
        if re.search(path_to_check, request.path):
            return True
        return False


class ActiveLinkNotEndsWithNode(ActiveLinkNodeBase):

    def is_active(self, request, *args):
        bool_list = [re.search(path_to_check, request.path)
                    for path_to_check in args]
        return not any(bool_list)


def parse(parser, token, end_tag):
    bits = token.split_contents()[1:]
    var_list = []
    for item in bits:
        var_list.append(TemplateIfParser(parser, [item]).parse())

    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return var_list, nodelist_true, nodelist_false

@register.tag
def ifactive(parser, token):
    urlnode = url(parser, token)
    var_list, nodelist_true, nodelist_false = parse(parser, token, 'endifactive')
    return ActiveLinkEqualNode(urlnode, var_list, nodelist_true, nodelist_false)


@register.tag
def ifstartswith(parser, token):
    urlnode = url(parser, token)
    var_list, nodelist_true, nodelist_false = parse(parser, token, 'endifstartswith')
    return ActiveLinkStartsWithNode(urlnode, var_list, nodelist_true, nodelist_false)


@register.tag
def ifendswith(parser, token):
    urlnode = url(parser, token)
    var_list, nodelist_true, nodelist_false = parse(parser, token, 'endifendswith')
    return ActiveLinkEndsWithNode(urlnode, var_list, nodelist_true, nodelist_false)

@register.tag
def ifnotendswith(parser, token):
    urlnode = url(parser, token)
    var_list, nodelist_true, nodelist_false = parse(parser, token, 'endifnotendswith')
    return ActiveLinkNotEndsWithNode(urlnode, var_list, nodelist_true, nodelist_false)
