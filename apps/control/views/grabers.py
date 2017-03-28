# -*- coding: utf-8 -*-
import pickle
import difflib
import re

from django.shortcuts import get_object_or_404, redirect

from control.utils import can_access
from annoying.decorators import render_to

from apps.graber.models import MultiplePlace, PlaceUpdate
from place.models import PlaceAddressWorkTime


def render_place_object(place_object):
    out = list()
    out.append(place_object['name'])
    for f in ('url', 'email'):
        v = place_object.get(f, None)
        if v:
            out.append('%s' % v )
        else:
            out.append(u'%s - нет данных' % f )

    out.append('')
    out.append(u'Категории:')
    category = place_object.get('category')
    if category:
        category = list(set([t['name'] for t in category]))
        category = filter(lambda i: i != '', category)
        out.append('%s' % u'; '.join(category))
    else:
        out.append('')

    out.append('')
    out.append(u'Теги:')
    tagging = place_object.get('tagging')
    if tagging:
        tagging = list(set([t['name'] for t in tagging]))
        tagging = filter(lambda i: i != '', tagging)
        out.append('%s' % u'; '.join(tagging))
    else:
        out.append('')

    out.append('')
    out.append(u'Платёжные системы:')
    payments = place_object.get('payments')
    if payments:
        payments = list(set(payments))
        payments = filter(lambda i: i != '', payments)
        out.append('%s' % u'; '.join(payments))
    else:
        out.append('')

    for adr in place_object['adr']:
        out.append('')
        out.append('%s' % adr.get('address', ''))
        out.append('%s' % adr.get('phone', ''))
        if 'wt_list' in adr:
            for wt_dump in adr['wt_list']:
                wt = PlaceAddressWorkTime(**wt_dump)
                out.append('%s' % wt.work_time())
    return '\n'.join(out)

@can_access()
@render_to('control/graber/dashboard.html')
def graber_dashboard(request):
    return {
        'multiple_place_count': MultiplePlace.objects.count(),
        'place_update_count': PlaceUpdate.objects.filter(status='new').count()
    }


@can_access()
@render_to('control/graber/clone_list.html')
def graber_clone_list(request):
    return {
        'multiple_place': MultiplePlace.objects.all(),
    }


@can_access()
@render_to('control/graber/clone_list_item.html')
def graber_clone_item(request, id):
    clone = get_object_or_404(MultiplePlace, id=id)
    if request.method == "POST":
        clone.delete()
        return redirect('control_graber_clone_list')
    return {
        'clone': clone
    }


@can_access()
@render_to('control/graber/place_update_list.html')
def graber_place_update_list(request):
    return {
        'palce_update': PlaceUpdate.objects.filter(status='new')
    }

@can_access()
@render_to('control/graber/place_update_form.html')
def graber_place_update_form(request, id):

    import pickle
    from graber.utils import update_place, create_place

    update = get_object_or_404(PlaceUpdate, id=id)
    approve_complete = False
    now_approve = False

    if request.method == 'POST':
        if 'approve' in request.POST and not 'reject' in request.POST:
            now_approve = True
            place_object = pickle.loads(update.place_object)
            approve_complete = update.approve()
            update.delete()
            if approve_complete:
                return redirect('control_graber_place_update_list')
        elif 'reject' in request.POST and not 'approve' in request.POST:
            update.delete()
            return redirect('control_graber_place_update_list')
        else:
            return redirect('control_graber_place_update_form')



    if update.place:
        place_txt = render_place_object(update.place.dump())
    else:
        place_txt = ''
    # place_txt = place_txt.replace('\n', '<br/>')

    place_obj_txt = render_place_object(pickle.loads(update.place_object),)
    # place_obj_txt = place_obj_txt.replace('\n', '<br/>')

    diff_operations = get_diff_operations(place_txt, place_obj_txt)

    return {
        'update': update,
        'diff_operations': diff_operations,
        'approve_complete': approve_complete,
    }


def split_txt(txt):
    words = []
    match = '([ ]+)'
    for s in txt.splitlines(True):
        for w in re.split(match, s):
            words.append(w)
    return words

def get_diff_operations(a, b):
    operations = []
    a_words = split_txt(a)
    b_words = split_txt(b)
    sequence_matcher = difflib.SequenceMatcher(None, a_words, b_words)
    for opcode in sequence_matcher.get_opcodes():
        operation, start_a, end_a, start_b, end_b = opcode

        deleted = ''.join(a_words[start_a:end_a])
        inserted = ''.join(b_words[start_b:end_b])

        operations.append({'operation': operation,
                           'deleted': deleted,
                           'inserted': inserted})
    return operations

