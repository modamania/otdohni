# -*- coding: utf-8 -*-
from apps.newsletter.models import Subscription
import os
from django.db.models.query_utils import Q

from django.core.management import call_command

from django.db import connection, connections, IntegrityError
from django.db.utils import ConnectionDoesNotExist

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from django.utils.html import strip_tags

from pytils.translit import slugify

from tagging.models import Tag
from threadedcomments.models import ThreadedComment
from rating.models import Vote
from news.models import NewsItem
from photoreport.models import Photo, PhotoReport
from place.models import (Place, PlaceCategory, PlaceGallery, PlaceAddress,
                   PlaceAddressWorkTime, RateCategories)
from event.models import Event, EventCategory, Occurrence
from action.models import Action, Poll, WorkBidder
from tea.models import Interview

from query import *

import re
import datetime


WEEKDAYS = {
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6,
        'Sunday': 7,
    }


def _get_votes(votes, votesum):
    """
    _get_votes(3,11) = [4,4,3]
    """
    mid_vote = int(round(votesum / float(votes)))
    tail = int(votesum - (mid_vote*votes))
    if tail:
        all_vote = [mid_vote for i in xrange(votes-abs(tail))]
        tail_vote = [mid_vote+(tail/abs(tail)) for i in xrange(abs(tail))]
        all_vote.extend(tail_vote)
    else:
        all_vote = [mid_vote for i in xrange(votes)]
    return all_vote


def _IntToTime(value):
    """
    Convert integer value to datetime.time
    e.g IntToTime(1900) = datetime.time(19,0)
    """
    strtime = str(value)
    if len(strtime) == 4:
        hour = int(strtime[:2])
        if hour == 24: hour = 0
        minute = int(strtime[2:])
        return datetime.time(hour, minute)
    elif len(strtime) == 3:
        hour = int(strtime[:1])
        minute = int(strtime[2:])
        return datetime.time(hour, minute)
    else:
        return datetime.time(00,00)


def _insert_tags(conn, query):
    """
    Insert tags records for place, placecategory and photoreports
    """
    records_list = list(set(_get_records(conn, query['query_select'])))
    cursor = connection.cursor()
    cursor.executemany(query['query_insert'], records_list)


def _get_records(conn, query, head=None, args=None):
    """
    Get list of dict with records from conn
    """
    if not args: args = tuple()
    try:
        cursor = connections[conn].cursor()
    except ConnectionDoesNotExist:
        print 'The database alias "%s" not exist' % conn
        return None
    cursor.execute(query, args)
    records = cursor.fetchall()
    if head:
        records = [dict(el) for el in [zip(head,item) for item in records]]
    return records

def _get_cursor(conn):
    try:
        cursor = connections[conn].cursor()
    except ConnectionDoesNotExist:
        print 'The database alias "%s" not exist' % conn
        return None
    return cursor


def _get_photos(string):
    """
    Get photo list for place instance
    """
    pattern = re.compile(r'src=\'(?P<photo>\w+)\' title=\'(?P<title>.*?)\'')
    result = pattern.findall(string)
    return result


def _get_sites(site_name):
    #return Site.objects.filter(id=1)
    return Site.objects.filter(Q(id=1) | Q(id=3))


#loads news from old base to NewsItem
def load_news(site_name=['otdohniomsk.ru'], conn='otdohni_old', striptags=True):
    call_command('reset', 'news', interactive=False)
    records = _get_records(conn, **NEWS_QUERY)
    if not records:
        return
    sites = _get_sites(site_name)
    for rec in records:
        if NewsItem.objects.filter(pk=rec["id"]):
            continue
        if rec['image']:
            rec['image'] = os.path.join('news/old', rec['image'])
        if striptags:
            rec['short_text'] = strip_tags(rec['short_text'])[:500]
        else:
            rec['short_text'] = rec['short_text'][:500]
        rec['slug'] = slugify(rec['title'])[-50:]
        try:
            news, created = NewsItem.objects.get_or_create(**rec)
            news.sites.add(*sites)
        except IntegrityError:
            print 'news dublicate slug %s' % rec['slug']
            rec['slug'] = rec['slug'] + str(rec['id'])
            news, created = NewsItem.objects.get_or_create(**rec)
            news.sites.add(*sites)
            print 'generate new slug for news %s' % rec['slug']
    print ' Load %d/%d news...' % (len(NewsItem.objects.all()),
                                           len(records))
#loads subscribers from old base to Subscriber
def load_subscribers(site_name=['otdohniomsk.ru'], conn='otdohni_old', striptags=True):
    records = _get_records(conn, **SUBSCRIBER_QUERY)
    if not records:
        return
    sites = _get_sites(site_name)
    for rec in records:
        if Subscription.objects.filter(pk=rec["id"]):
            continue

        if not rec['user_id']:
            del rec['user_id']
        else:
            if not User.objects.filter(id=rec["user_id"]):
                continue

        try:
            subscriber, created = Subscription.objects.get_or_create(**rec)

        except IntegrityError:
            print 'subscriber dublicate email %s' % rec['email']
    print ' Load %d/%d subscribers...' % (len(Subscription.objects.all()),
                                   len(records))

#loads places from old base to Place, PlaceCategory, PlaceGallery,
#PlaceAddress, PlaceAddressWorkTime
def load_places(site_name=['otdohniomsk.ru'], conn='otdohni_old'):
    call_command('reset', 'place', interactive=False)
    call_command('reset', 'tagging', interactive=False)
    call_command('reset', 'rating', interactive=False)

    #import all places from jos_places_company
    places = _get_records(conn, **PLACE_QUERY)
    addresses = _get_records(conn, **ADDRESS_QUERY)
    work_times = _get_records(conn, **ADDRESS_WORK_TIME_QUERY)
    tags = _get_records(conn, **TAG_QUERY)
    categories = _get_records(conn, **CATEGORY_QUERY)
    rate_items = _get_records(conn, **RATE_CATEGORY_QUERY)
    place_photos = _get_records(conn, **PLACE_PHOTOS_QUERY)
    sites = _get_sites(site_name)

    if not (places and addresses and work_times and categories and
           tags and rate_items and place_photos):
        return

    for place in places:
        if Place.objects.filter(pk=place["id"]):
            continue
        status = place.pop('status')

        if place["logotype"]: place["logotype"] = 'place/logo/%s' % place["logotype"]
        if place["photo"]: place["photo"] = 'place/%s/promo_picture/big/%s' % (place["id"], place["photo"])

        if status == 1:
            place['is_new'] = True
        if status == 2:
            place['expert_choice'] = True
        try:
            obj, created = Place.objects.get_or_create(**place)
            obj.sites.add(*sites)
        except:
            print 'place not added id %d' % place['id']
    #fix photo path
    #places = Place.objects.all()
    #for place in places:
    #    if place.logotype:
    #        place.logotype = 'place/logo/%s' % place.logotype.name
    #    if place.photo:
    #        place.photo = 'place/%s/promo_picture/big/%s' % (
    #                                place.id, place.photo.name)
    #        place.save()

    #import all adressess from jos_places_address
    for address in addresses:
        try:
            obj, created = PlaceAddress.objects.get_or_create(**address)
        except:
            print 'address not added id %d' % address['id']

    #import all worktimes from jos_places_work_time
    for worktime in work_times:
        worktime.update({
            'from_time':_IntToTime(worktime['from_time']),
            'till_time':_IntToTime(worktime['till_time'])
        })
        try:
            obj, created = PlaceAddressWorkTime.objects.get_or_create(**worktime)
        except:
            print 'worktime not added id %d' % worktime['id']

    #import all tags from jos_tegs
    for tag in tags:
        try:
            obj, created = Tag.objects.get_or_create(**tag)
        except:
            print 'tag not added id %d' % tag['id']
    print ' Load %d/%d tags...' % (len(Tag.objects.all()),
                                           len(tags))

    #import all tags without parent from jos_places_tags
    for category in categories:
        try:
            if not category['order']:
                import random
                category['order'] = random.randint(300,1000)
            obj, created = PlaceCategory.objects.get_or_create(**category)
        except:
            print 'cat not added id %d' % category['id']

    #import all relations for place and category from jos_places_category
    for rate_item in rate_items:
        try:
            cat = PlaceCategory.objects.get(main_tag__id=rate_item['category_id'])
        except:
            print 'PlaceCategory %s does not exist' % rate_item['category_id']
        rate_item.update({'category_id': cat.id})
        try:
            obj, created = RateCategories.objects.get_or_create(**rate_item)
        except:
            print 'rate item not added id %d' % rate_item['id']

    #insert all photos for places
    for place in place_photos:
        photos = _get_photos(place['image'])
        for idx, photo in enumerate(photos):
            gallery, created = PlaceGallery.objects.get_or_create(
                place_id=place['id'],
                order=idx+1,
                image='place/%s/normal/%s.jpeg' % (place['id'], photo[0]),
                title='%s' % photo[1])

    #adds tags for each event and category
    _insert_tags(conn, TAGS_CATEGORY_QUERY)
    _insert_tags(conn, TAGS_PLACE_QUERY)

    print 'Loaded %d places, %s categories, %d addresses, %d worktimes' % (
        Place.objects.count(),
        PlaceCategory.objects.count(),
        PlaceAddress.objects.count(),
        PlaceAddressWorkTime.objects.count())


#loads photos and photoreports from old base to Photo, PhotoReports
def load_photoreports(site_name=['otdohniomsk.ru'], conn='otdohni_old'):
    photos = _get_records(conn, **PHOTO_QUERY)
    photoreports = _get_records(conn, **PHOTOREPORT_QUERY)
    sites = _get_sites(site_name)

    if not (photos and photoreports):
        return

    for ph in photoreports:
        try:
            report = PhotoReport.default_manager.get(id=ph['id'])
        except PhotoReport.DoesNotExist:
            ph['slug'] = ph['slug'][:50]
            if not ph['date_event']:
                ph['date_event'] = datetime.date(2008,10,15)
            place_name = ph['description']
            place_name = place_name.replace("&quot;", "").strip().lower().capitalize()
	    place_id = ''
            if place_name:
                try:
                    place = Place.objects.filter(name__contains=place_name, is_published = 1)[:1]
                    if place:
                        place_id = place[0].pk
                except Place.DoesNotExist:
                    place_id = ''
                    pass
            else:
                place_id = ''
            report_data = {'id': ph['id'],
                           'date_event': ph['date_event'],
                           'title': ph['title'],
                           'slug': ph['slug'],
                           'pub_date': ph['date_event'],
                           'place_id': place_id,
                           }
            report = PhotoReport.default_manager.create(**report_data)
            report.sites.add(*sites)

        """
        if not PhotoReport.objects.filter(pk=ph["id"]):
            continue
        ph['place_event_id'] = 1158
        ph['slug'] = ph['slug'][:50]
        if not ph['date_event']:
            ph['date_event'] = datetime.date(2008,10,10)
        ph['pub_date'] = ph['date_event']

        try:
            photoreport, created = PhotoReport.default_manager.get_or_create(**ph)
            photoreport.sites.add(*sites)
        except:
            print 'NOT ADDED %s photoreport' % ph['slug']
        """

    print ' Load %d/%d photoreports...' % (len(PhotoReport.default_manager.all()),
                                           len(photoreports))
    
    for ph in photos:
        if PhotoReport.objects.filter(pk=ph["id"]):
            continue
        ph['slug'] = slugify(ph['title']+str(ph['id']))[-50:]
        ph['image'] = os.path.join('photoreports/old/',
                                             ph['image'])

        try:
            report = PhotoReport.default_manager.get(id=ph['photoreport_id'])
        except PhotoReport.DoesNotExist:
            report_data = {'id': ph['photoreport_id'],
                      'date_event': datetime.date(2008,10,10),
                      'title': ph['title'],
                      'slug': ph['slug'],
                      'pub_date': datetime.date(2008,10,10),
                     }
            report = PhotoReport.default_manager.create(**report_data)
            report.sites.add(*sites)
        try:
            photo, created = Photo.objects.get_or_create(**ph)
        except IntegrityError:
            print 'photo dublicate slug %s' % ph['slug']
            ph['slug'] = slugify(ph['title']+str(ph['id']))[-50:]
            photo, created = NewsItem.objects.get_or_create(**rec)
            print 'generate new slug for news %s' % rec['slug']
        print 'Load report %s' % report

    print ' Load %d/%d photos...' % (len(Photo.objects.all()),
                                           len(photos))

    _insert_tags(conn, TAGS_PHOTOREPORT_QUERY)


def load_occurence(conn, event_id):
    records = _get_records(conn, args=(event_id,), **OCCURRENCE_QUERY)

    for record in records:

        # REPEAT_ON
        repeat_on = record['repeat_on']
        if repeat_on:
            if repeat_on in ('weekly', 'week'):
                repeat_on = 2
            elif repeat_on in ('daily', 'day'):
                repeat_on = 1
        else:
            if not record['end_date']:
                record['end_date'] = record['start_date']
            repeat_on = 0

        record['repeat_on'] = repeat_on
        def make_end(dc):
            keys = ('end_date', 'start_date', 'repeat_until', 'repeat_every',
                    'repeat_number', 'repeat_on')
            end, start, until, val, num, on = (dc[x] for x in keys)

            if not end and not on:
                end = start
            elif not on and not val:
                end = start
            elif on:
                if until and (end and until > end.date()):
                    end = until
                if until and (not end and until > start.date()):
                    end = until
                if until and not end and until <= start.date():
                    end = start
                if not until and ((not end) or (end <= start)):
                    if val == 1 and not num:
                        end = start
                    elif val == 1 and num:
                        end = start + datetime.timedelta(days=1) * num
                    elif on == 2 and not val:
                        end = None
            return dict(
                (x for x in zip(keys, (end, start, until, val, num, on))))


        # END_DATE
        record.update(make_end(record))
        record.pop('repeat_until')
        # PEREAT_NUMBER
        if record['repeat_number'] == 0:
            record['repeat_number'] = None
            
        # REPEAT_EVERY
        if not record['repeat_every']:
            record.pop('repeat_every')

        # REPEAT_WEEKDAY
        weekdays = []
        for i, weekday in enumerate(('monday', 'thuesday', 'wednesday',
                                    'thursday', 'friday', 'saturday', 'sunday')):
            day_value = record.pop(weekday)
            if day_value:
                weekdays.append(str(i))
        record['repeat_weekday'] = ','.join(weekdays)
        if record['repeat_weekday'] in ('0,0,0,0,0,0,0', ''):
            record['repeat_weekday'] = None

        if repeat_on == 2 and record['repeat_weekday'] == None:
            continue

        # START_TIMES
        if not record['start_times']:
            record['start_times'] = [record['start_date'].time()]
        else:
            record['start_times'] = record['start_times'].replace('24:00', '00:00')
            # supports the following delimiters:
            # '.', ' ', ';'
            times = re.split('(?:(?<=\d) (?=\d))|[;,]', record['start_times'])
            record['start_times'] = []
            if record['start_date'].time():
                record['start_times'].append(record['start_date'].time())
            for time_to_conv in times:
                match = re.match("(\d{1,2})[-:](\d{1,2})", time_to_conv.strip())
                if not match: continue
                hour, minute = match.groups()
                record['start_times'].append(datetime.time(int(hour), int(minute)))
        try:
            Occurrence.objects.create(**record)
        except:
            import pdb; pdb.set_trace()


def load_event(conn=None, site_name=['otdohniomsk.ru']):
    votes_sql = EVENT_QUERY.pop('votes_sql')
    star_sql = EVENT_QUERY.pop('star_sql')

    error_events = []
    error_occurrence = []

    cursor = _get_cursor(conn)
    records = _get_records(conn, **EVENT_QUERY) 
    sites = _get_sites(site_name)

    for record in records:
        rid = record['id']
        if Event.objects.filter(pk=rid):
            continue

        # IMAGE
        if record['image'] is None:
                record['image'] = record['add_picture']
        record['image'] = "afisha/old/main/%s" % record['image']
        record.pop('add_picture')

        cursor.execute(votes_sql, (rid,))
        record['num_votes'] = cursor.fetchone()[0]

        cursor.execute(star_sql, (rid,))
        record['rate'] = cursor.fetchone()[0] or 1

        record['is_published'] = bool(record['is_published'])\
                                    if record.pop('approved')\
                                    else False

        if u'от 6 до 12 минут' in record['description']:
            record['publish_on_main'] = False

        try:
            event = Event.objects.create(**record)
            event.sites.add(*sites)
        except Exception, e:
            error_events.append((record['id'], e))

        try:
            load_occurence(conn, record['id'])
        except Exception, e:
            error_occurrence.append((record['id'], e))
            
        if not Occurrence.objects.filter(event__id=rid).exists():
            Event.objects.filter(id=rid).delete()
        
        print "Loaded event %d" % record['id']
    if error_events:
        print ' Error when loading %d events' % len(error_events)
    if error_occurrence:
        print ' Error when loading %d repetitions' % len(error_occurrence)
    print ' Loaded %d/%d events...' % (Event.objects.count(),
                                           len(records))


def load_category(conn='otdohni_old'):
    records = _get_records(conn, **CATEGORU_QUERY)

    for record in records:
        record['slug'] = slugify(record['title'])
        record['order'] = record["id"]
        if EventCategory.objects.filter(pk=record["id"]):
            continue

        EventCategory.objects.create(**record)
    print ' Load %d/%d categories...' % (len(EventCategory.objects.all()),
                                           len(records))


def load_taxi(conn='otdohni_old'):
    records = _get_records(conn, **TAXI_QUERY)
    taxi_tag, created = Tag.objects.get_or_create(name=u'Такси', slug='taxi')
    #taxi_cat, created = PlaceCategory.objects.get_or_create(name=u'Такси', main_tag=taxi_tag)
    try:
        taxi_cat=PlaceCategory.objects.get(name=u'Такси', main_tag=taxi_tag)
    except PlaceCategory.DoesNotExist:
        taxi_cat=PlaceCategory(name=u'Такси',main_tag=taxi_tag)
        taxi_cat.save()
    ids = [rec.get('id') for rec in records]
    places = Place.objects.filter(id__in=ids)
    taxi_cat.places.add(*places)
    print ' Load %d/%d taxies...' % (len(places),
                                           len(records))


#loads actions from old base to action.model.Action
def load_action(site_name=['otdohniomsk.ru'], conn='otdohni_old', striptags=True):
    pattern = re.compile(r'http:\/\/(?:w{3}\.)?otdohniomsk\.ru\/(?:\w+\/){2}([-_./\w]+)')
    #call_command('reset', 'action', interactive=False)
    actions = _get_records(conn, **ACTION_QUERY)
    polls = _get_records(conn, **POLL_QUERY)
    workbidders = _get_records(conn, **WORKBIDDER_QUERY)
    if not actions:
        return
    sites = _get_sites(site_name)

    for rec in actions:
        if rec['image']:
            rec['image'] = os.path.join('news/old', rec['image'])
        if striptags:
            rec['short_text'] = strip_tags(rec['short_text'])[:500]
        else:
            rec['short_text'] = rec['short_text'][:500]
        rec['slug'] = slugify(rec['title'])[-50:]

        try:
            action, created = Action.objects.get_or_create(**rec)
            action.sites.add(*sites)
        except IntegrityError:
            print 'action dublicate slug %s' % rec['slug']
            rec['slug'] = rec['slug'] + str(rec['id'])
            action, created = Action.objects.get_or_create(**rec)
            action.sites.add(*sites)
            print 'generate new slug for action %s' % rec['slug']

    print ' Load %d/%d actions...' % (len(Action.objects.all()),
                                           len(actions))
    for poll in polls:
        poll['start_date'] = datetime.date(2011,01,01)
        if poll['status']:
            poll['end_date'] = datetime.date(2011,12,31)
            poll['status'] = 'ACTIVE'
        else:
            poll['end_date'] = datetime.date(2011,01,02)
            poll['status'] = 'COMPLETED'
        p, created = Poll.objects.get_or_create(**poll)

    print 'Load %d/%d polls...' % (len(Poll.objects.all()), len(polls))

    for work in workbidders:
        if work['text']:
            if not "img src=" in work['text']:
                work['text'] = work['text'].decode('utf-8')
            photos = pattern.findall(work['text'])
            if photos:
                work['photo'] = os.path.join('news/old',
                                             photos[0])
            if "img src=" in work['text']:
                work['text'] = ''
        work['author_name'] = work['title']
        w, created = WorkBidder.objects.get_or_create(**work)
    print ' Load %d/%d workbidders...' % (len(WorkBidder.objects.all()),
                                           len(workbidders))
    _insert_tags(conn, LIKE_QUERY)


#load ratings from old base to rating.models.Vote
def load_rating(conn='otdohni_old', app_label=None, model=None):
    if app_label == 'place':
        query = VOTE_PLACE_QUERY
    if app_label == 'photoreport':
        query = VOTE_PHOTOREPORT_QUERY
    if app_label == 'event':
        query = VOTE_EVENT_QUERY
    raw_records = _get_records(conn, **query)
    if app_label and model and raw_records:
        try:
            ct = ContentType.objects.get(app_label=app_label, model=model)
        except ContentType.DoesNotExist:
            return 'content type does not exist %s %s' % (app_label, model)
        user, created = User.objects.get_or_create(username='TestVoter')
        records = []
        for record in raw_records:
            record.update({'content_type_id': ct.pk})
            if 'user_id' not in record:
                record.update({'user_id': user.id})
            if 'votes' in record and 'votesum' in record:
                votes = record.pop('votes')
                votesum = record.pop('votesum')
                vote_list = _get_votes(votes, votesum)
                for i, vote in enumerate(vote_list):
                    r = record.copy()
                    r.update({'vote': vote})
                    records.append(r)
            else:
                records = raw_records
        #return raw_records

        ct.model_class()
        votes = 0
        for record in records:
            #import ipdb;ipdb.set_trace()
            Vote.objects.create(**record)
            votes += 1
        print 'Load %d votes for %s...' % (votes, model)


#loads comments from old base to ThreadedComment
def load_comment(conn='otdohni_old', app_label=None, model=None):
    if app_label == 'photoreport':
        query = PHOTO_COMMENT_QUERY
    else:
        query = COMMENT_QUERY
    records = _get_records(conn, **query)
    if app_label and model and records:
        try:
            ct = ContentType.objects.get(app_label=app_label, model=model)
        except ContentType.DoesNotExist:
            return 'content type does not exist %s %s' % (app_label, model)

        if app_label == 'event':
            records = [rec for rec in records if rec['object_pk']>5000000]
        elif app_label == 'place':
            records = [rec for rec in records \
                       if 1000000<rec['object_pk']<5000000]
        elif app_label == 'news' or app_label == 'action':
            records = [rec for rec in records if rec['object_pk']<1000000]

        for record in records:
            record.update(
                {'site_id':1,
                'content_type_id':ct.pk,
                'user_name': strip_tags(record['user_name'])
                }
            )
            pk = str(record['object_pk'])[-4:]
            record['object_pk'] = int(pk)

            user = User.objects.filter(first_name=record['user_name'])
            if not user:
                user = User.objects.filter(username=record['user_name'])
            if not user:
                try:
                    user = User.objects.filter(id=record['user_name'])
                except ValueError:
                    pass
            if user:
                record.update({'user_id': user[0].id})

            #set record['submit_date'] to datetime.datetime
            if not isinstance(record['submit_date'], datetime.datetime):
                record['submit_date'] = datetime.datetime.fromtimestamp(int(record['submit_date']))

        model_class = ct.model_class()
        comments = 0
        for record in records:
            record['comment'] = record['comment'].replace(r'\"', '"')
            if model_class.objects.filter(id=record['object_pk']).exists():
                ThreadedComment.objects.create(**record)
                comments += 1
        print 'Load %d comments for %s...' % (comments, model)


def load_tea(conn='otdohni_old', site_name=['otdohniomsk.ru']):
    call_command('reset', 'tea', interactive=False)
    sites = _get_sites(site_name)
    records = _get_records(conn, args=("%tea-with-star%",), **TEA_QUERY)
    pattern_image = re.compile("""<img.*src=["'](.*(?<!svaylogo).jpg)["'].*alt=['"](?!svaylogo).*/\s?>""")
    pattern_title = re.compile(r"<h[2]>[\r\n]*(?:<strong>)?(.*):")

    error_tea = []

    for record in records:
        title = pattern_title.findall(record['full_text'])
        # TODO: replaced join and endswith by re
        record['title'] = ' '.join(title[0].split()[:2])\
                                if title else record['title']
        if record['title'].endswith(':'):
            record['title'] = record['title'][:-1]
        if record['image']:
            image = record['image']
        else:
            images = pattern_image.findall(record['full_text'])
            for i in images:
                if not 'logo' in i:
                    image = i
                    break
            if image:
                record['image'] = image
            else:
                record.pop('image')
        record['is_published'] = bool(record['is_published'])
        try:
            tea = Interview.objects.create(**record)
        except Exception, e:
            error_tea.append((record['id'], e))
        else:
            tea.sites = sites
            tea.save()
            print "Loaded tea %d" % record['id']
    if error_tea:
        print " Error when loading %d tea" % len(error_tea)
    print "Loaded %d/%d tea" % (Interview.objects.count(), len(records))


def replace_media_urls(old='stories', new='news/old',
                       app_label='news', model='newsitem', field='full_text', new_path='/media/'):
    from django.db.models import get_model
    from django.db.models.query import  QuerySet
    from django.db.models.sql import  Query
    BASE_NEW_PATH = new_path
    BASE_OLD_RE = r'http:\/\/w{3}\.otdohniomsk\.ru\/images\/'
    BASE_OLD_PATH = 'http://www.otdohniomsk.ru/images/'

    old_path = BASE_OLD_PATH + old
    new_path = BASE_NEW_PATH + new
    p = re.compile(BASE_OLD_RE + old)

    total_count = 0
    m = get_model(app_label, model)
    q = Query(m)
    q.add_filter(('%s__contains' % field, old_path))
    qs = QuerySet(m, q)

    for item in qs:
        item.__dict__[field], count = p.subn(new_path, item.__dict__[field])
        total_count += count
        item.save()
    return total_count
