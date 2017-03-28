# -*- coding: utf-8 -*-
import logging
import datetime
import sys, traceback
import re
import pickle
import pytils
import os
from urlparse import urlparse

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.sites.models import Site

from grab.spider import Spider, Task

from place.models import Place, PlaceCategory, PlaceAddress,\
                            PlaceAddressWorkTime
from graber.models import MultiplePlace, PlaceUpdate, HeroCategory,\
                            HeroTagging
from graber.utils import update_place
from payments.models import PaymentSystem
from city.models import City


# logging.basicConfig(
#     level=logging.DEBUG,
#     format = "\n%(levelname) -10s %(module)s:%(lineno)s %(message)s",
# )
logger = logging.getLogger(__name__)

DAY_TRANSLATE = {
    u'пн': 'mon',
    u'вт': 'tue',
    u'ср': 'wed',
    u'чт': 'thu',
    u'пт': 'fri',
    u'сб': 'sat',
    u'вс': 'sun',
}


def update_wt_by_record(wt, record):
    if len(record) == 2:
        wt = update_wt_day(wt, record)
    else:
        wt = update_wt_time(wt, record)
    return wt

def update_wt_day(wt, record):
    record = record.lower()
    attr = DAY_TRANSLATE[record]
    setattr(wt, attr, True)
    return wt

def update_wt_time(wt, record):
    logger.log(logging.DEBUG, record)

    record = record.split(' - ')
    from_time = record[0]
    till_time = record[-1]

    logger.log(logging.DEBUG, 'from_time - till_time: %s - %s' % (from_time, till_time))

    if till_time == '24:00':
        till_time = '00:00'

    if from_time == till_time:
        wt.all_day = True
    else:
        from_time = from_time.split(':')
        till_time = till_time.split(':')

        from_time = datetime.time(int(from_time[0]), int(from_time[1]))
        till_time = datetime.time(int(till_time[0]), int(till_time[1]))

        wt.from_time = from_time
        wt.till_time = till_time

    return wt

def indent_work_time(wt1, wt2):
    if wt1.all_day and wt2.all_day:
        return True
    return wt1.from_time == wt2.from_time and wt1.till_time == wt2.till_time

def copy_work_day(to_wt, from_wt):
    for attr in DAY_TRANSLATE.values():
        if getattr(from_wt, attr):
            setattr(to_wt, attr, True)
    return to_wt

def update_wt_list(wt_list, wt):
    wt_len = len(wt_list)
    for i in xrange(wt_len):
        control_wt = wt_list.pop(i)
        if indent_work_time(control_wt, wt):
            control_wt = copy_work_day(control_wt, wt)
            wt_list.insert(i, control_wt)
            return wt_list
        else:
            wt_list.insert(i, control_wt)

    wt_list.append(wt)
    return wt_list

def get_work_time(html):
    logger.log(logging.DEBUG, html)
    wt_list = []
    for h in html:
        for t in h.html().split('<td>'):
            logger.log(logging.DEBUG, t)
            if not t:
                continue
            wt = PlaceAddressWorkTime()
            for f in t.split('</div>'):
                logger.log(logging.DEBUG, f)
                if u'<br>' in f:
                    logger.log(logging.DEBUG, 'Pattern in string')
                    f = f.replace(r'<br>', ' ')
                logger.log(logging.DEBUG, f)
                if f.startswith('<div'):
                    record = f.split('>')[1]
                    logger.log(logging.DEBUG, record)
                    wt = update_wt_by_record(wt, record)
            if not len(wt_list):
                wt_list.append(wt)
            else:
                wt_list = update_wt_list(wt_list, wt)

    #Append day off if not week day is used
    days = DAY_TRANSLATE.values()
    days_off = DAY_TRANSLATE.values()
    for wt in wt_list:
        for d in days:
            if getattr(wt, d):
                days_off.remove(d)
        if not days_off:
            break

    if days_off:
        wt = PlaceAddressWorkTime()
        wt.day_off = True
        for d in days_off:
            setattr(wt, d, True)
        wt_list.append(wt)

    return wt_list


def get_category(grab):
    rubrics = grab.doc.select('//div[@class="p_rubrics"]')
    if rubrics.exists():
        rubrics = rubrics.text().strip()
    else:
        return None

    cats = []
    for r in rubrics.split(';'):
        if r:
            cats.append(r.strip())

    otd_cats = []
    for cat in cats:
        if not cat:
            continue
        try:
            otd_cat = HeroCategory.objects.get(hero_name=cat.lower()).category
        except HeroCategory.DoesNotExist:
            pass
        except Exception as e:
            print u'\t\t%s -- %s' % (cat, e)
        else:
            otd_cats.append({'id': otd_cat.id, 'name':otd_cat.name,})
    return otd_cats

def get_tagging(grab):
    rubrics = grab.doc.select('//div[@class="p_rubrics"]')
    if rubrics.exists():
        rubrics = rubrics.text().strip()
    else:
        return None

    tags = []
    for r in rubrics.split(';'):
        if r:
            tags.append(r.strip())

    otd_tags = []
    for tag in tags:
        if not tag:
            continue
        try:
            otd_cat = HeroTagging.objects.get(hero_name=tag.lower()).tag
        except HeroTagging.DoesNotExist:
            pass
        except Exception as e:
            print u'\t\t%s -- %s' % (tag, e)
        else:
            otd_tags.append({'id': otd_cat.id, 'name':otd_cat.name,})
    return otd_tags

# def get_tagging(grab):
#     tagging = grab.doc.select('//div[@class="p_rubrics"]')
#     if tagging.exists():
#         return [p.strip() for p in tagging.text().split(';')]
#     return None


def get_payments(grab):
    payments = grab.doc.select('//span[@class="p_payoptions"]')
    if payments.exists():
        return [p.strip() for p in payments.text().split(';')]
    return None

def is_identical_list(html_list, db_list):
    if html_list:
        html_list = list(set(html_list))
        html_list = filter(lambda i: i != '', html_list)
        html_list.sort()
    else:
        html_list = []

    db_list = list(set(db_list))
    db_list = filter(lambda i: i != '', db_list)
    db_list.sort()

    if not html_list == db_list:
        return False
    return True

def to_moderation(place_object, place):
    is_identical = True
    for f in ['name', 'url', 'email']:
        now_v = getattr(place, f, None)
        new_v = place_object.get(f, None)
        if not now_v and not new_v:
            continue
        if not now_v == new_v:
            is_identical = False
            print '1'
            break

    if is_identical:
        is_identical = is_identical_list(
            [t['name'] for t in place_object.get('tagging')],
            [t.__unicode__() for t in place.tagging.all()]
        )

    if is_identical:
        is_identical = is_identical_list(
            [t['name'] for t in place_object.get('category')],
            [t.__unicode__() for t in place.category.all()]
        )

    if is_identical:
        is_identical = is_identical_list(place_object.get('payments'), [p.display for p in place.payments.all()])

    for adr_object in place_object['adr']:
        if is_identical:
            try:
                adr = place.address.get(address=adr_object['address'])
            except PlaceAddress.DoesNotExist:
                is_identical = False
                print '3'
            else:
                if not adr.phone == adr_object.get('phone', None):
                    is_identical = False
                    print '4'
        if is_identical and adr and 'wt_list' in adr_object:
            adr_wt_list = [wt.dump() for wt in adr.work_time.all()]
            if not adr_object['wt_list'] == adr_wt_list:
                is_identical = False
                print '5'

    if not is_identical:
        create_moderaion(place_object, place)


def create_moderaion(place_object, place):
    response_url = place_object['response_url']
    print ''
    print 'Create moderation'
    print place_object['response_url']
    print ''
    # return
    # exit(1)
    # print place_object
    PlaceUpdate.objects.filter(response_url=response_url).delete()
    kwargs = {
        'place': place,
        'response_url': response_url,
        'place_object': pickle.dumps(place_object),
    }
    PlaceUpdate.objects.create(**kwargs)
    # exit(0)


class AntiherosSpider(Spider):
    # initial_urls = ['http://www.antiheroes.ru/rubrics/4503719886454786']
    # initial_urls = ['http://www.antiheroes.ru/firm/704215723355781?hash=A99863GA073502641A39776Bguh62384H62J1HJ7cuvdx4385AJ0I0JA2296hddd7235A22512B148192']
    initial_urls = ['http://www.antiheroes.ru/']
    base_url = 'http://www.antiheroes.ru/'
    site_id = None
    city = u''

    def rebuild_url_to_city(self, url):
        url = url.replace(u'Москва', self.city)
        url = url.replace('&sir' , '')
        url = url.replace(' ' , '%20')
        return url

    def task_initial(self, grab, task):
        for cat in grab.css_list(u'.index_rubrics a'):
            yield Task('category', url=cat.get('href'))
        
    def task_category(self, grab, task):
        for cat in grab.css_list(u'ul.list_rubrics li a'):
            if HeroCategory.objects.filter(hero_name=cat.text.lower()).count():
                url = self.rebuild_url_to_city(cat.get('href'))
                yield Task('subcategory', url=url)

    def task_subcategory(self, grab, task):
        cat_description = grab.css_list(u'td.txt b')
        page_list = grab.doc.select('//div[@class="list_pages"]//a')

        cur_page = re.search(r'page=\d+', grab.response.url)
        if cur_page:
            cur_page = int(cur_page.group().replace('page=', ''))
        else:
            cur_page = 1
        if page_list.exists():
            for a in page_list:
                a_text = a.text()
                if a_text == u'Далее':
                    break
                if int(a_text) == (cur_page+1):
                    url = self.rebuild_url_to_city(a.attr('href'))
                    yield Task('subcategory', url=url)


        if cat_description[1].text:
            for place in grab.css_list('div.orgl.lc a'):
                yield Task('place', url=place.get('href'))
            for place in grab.css_list('div.orgl div.lc a'):
                yield Task('place', url=place.get('href'))

    def get_place(self, **kwargs):
        try:
            place = Place.default_manager.get(sites__id=self.site_id, **kwargs)
        except Place.DoesNotExist:
            return None, True
        except Place.MultipleObjectsReturned:
            mp = MultiplePlace.objects.create()
            for p in Place.default_manager.filter(sites__id=self.site_id, **kwargs):
                mp.place.add(p)
            raise Place.MultipleObjectsReturned
        else:
            return place, False

    def task_place(self, grab, task):
    # def task_initial(self, grab, task):
        try:
            place_name = unicode(grab.css_one('h1').text)
            if ',' in place_name:
                place_name = place_name.split(',')[0].strip()
            # print place_name
            
            try:
                place, need_create = self.get_place(identity=grab.response.url)
            except Place.MultipleObjectsReturned:
                return
            if not place:
                try:
                    place, need_create = self.get_place(name=place_name, identity='')
                except Place.MultipleObjectsReturned:
                    return


            place_object = dict()
            place_object['site_id'] = self.site_id
            place_object['name'] = place_name
            place_object['category'] = get_category(grab)
            place_object['tagging'] = get_tagging(grab)
            place_object['payments'] = get_payments(grab)

            res = urlparse(grab.response.url)
            place_object['response_url'] = '%s://%s%s' % (res.scheme, res.netloc, res.path)

            if not place_object['category']:
                return

            url = grab.doc.select('//table[@class="p_contacts"]//a')
            if url.exists():
                place_object['url'] = url.attr('href').split('http://')[2]

            email = grab.doc.select('//span[@itemprop="email"]')
            if email.exists():
                place_object['email'] = email.text()

            place_object['adr'] = list()
            address_text = grab.css_one('div.adr').text.strip()

            if not address_text.startswith(self.city):
                if not place:
                    # Нет заведения, нет проблем :)
                    return
                print ''
                print "--> BAD ADDRESS: %s" % address_text
                print "    place_name = %s" % place_name
                print "    place.id = %s" % place.id
                print "    place.identity = %s" % place.identity
                if place:
                    print "    manual_changed = %s" % place.manual_changed
                    if not place.manual_changed:
                        place.delete()
                        print "    place deleted"

                return

            # sys.stdout.write('*')

            adr = dict()
            address_text = address_text.replace(u'%s, ' % self.city, '').strip()
            adr['address'] = address_text
            tel = grab.doc.select('//span[@itemprop="tel"]')
            if tel.exists():
                adr['phone'] = u', '.join(t.text().strip() for t in tel)

            wt_html = grab.doc.select('//table[@class="p_wtime"]/tr/td')
            if wt_html.exists():
                wt_list = get_work_time(wt_html)
                adr['wt_list'] = [w.dump() for w in wt_list]

            place_object['adr'].append(adr)

            if need_create:
                create_moderaion(place_object, place)
            else:
                # from graber.utils import update_place
                # update_place(place_object, place)
                to_moderation(place_object, place)

        except Exception as e:
            print ''
            print '-'*40
            print e
            print '-'*40
            print grab.response.url
            print '-'*40
            print ''
            traceback.print_exc(file=sys.stdout)
            print ''
            # exit(1)



class Command(BaseCommand):

    help = "Parse http://www.antiheroes.ru/"
    def handle(self, *args, **kwargs):
        if settings.DEBUG:
            qs = City.objects.filter(name=u'Кемерово')
        else:
            qs = City.objects.all().exclude(name=u'Омск')
        for city in qs:
            try:
                print ''
                print '*'*40
                print city.site_id
                print city
                print ''
                bot = AntiherosSpider()
                bot.city = city.name
                bot.site_id = city.site_id
                BDSettings = settings.DATABASES['default']
                if settings.DEBUG:
                    bot.setup_cache(
                        backend = BDSettings['ENGINE'].split('.')[-1],
                        database = BDSettings['NAME'],
                        user = BDSettings['USER'],
                        passwd = BDSettings['PASSWORD'],
                    )
                bot.run()
                print ''
            except Exception as e:
                print ''
                print '-'*40
                print e
                print '-'*40
                print ''
                traceback.print_exc(file=sys.stdout)
                print ''
        print ''
        print 'COUNT: %s' % Place.default_manager.all().count()
        print ''


