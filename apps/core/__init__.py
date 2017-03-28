from django.db.models.sql.constants import LOOKUP_SEP
from django.db.models import sql
from django.db import connection

import itertools


class Indexable(object):

    def __init__(self,it):
        self.it=it

    def __iter__(self):
        for elt in self.it:
            yield elt

    def __getitem__(self,index):
        try:
            return next(itertools.islice(self.it,index,index+1))
        except TypeError:
            return list(itertools.islice(self.it,index.start,index.stop,index.step))


def load_related_m2m(object_list, field):

    select_fields = ['pk']
    #related_field = object_list.model._meta.get_field(field)
    if not object_list:
        return
    model = object_list[0].__class__
    related_field = model._meta.get_field(field)
    related_model = related_field.rel.to
    cache_name = 'all_%s' % field

    for f in related_model._meta.local_fields:
        select_fields.append('%s%s%s' % (field, LOOKUP_SEP, f.column))

    query = sql.Query(model)
    query.add_fields(select_fields)
    query.add_filter(('pk__in', [obj.pk for obj in object_list]))

    related_dict = {}
    cursor = connection.cursor()
    cursor.execute(query.__str__())
    for row in cursor.fetchall():
        if row[2]:
            related_dict.setdefault(row[0], []).append(related_model(*row[1:]))

    for obj in object_list:
        try:
            setattr(obj, cache_name, related_dict[obj.pk])
        except KeyError:
            setattr(obj, cache_name, [])

    return object_list
