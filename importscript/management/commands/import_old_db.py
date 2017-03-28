# -*- coding: utf-8 -*-
import os
import pytils
import re
import progressbar
#import MySQLdb
from datetime import datetime, time

from django.core.management.base import BaseCommand
from django.core.management import  call_command
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from profile.models import OldAuth
from importscript.settings import *
from importscript.connect import *
from friendship.models import Friendship
from tagging.models import Tag
from place.models import PlaceCategory, Place, PlaceAddress,\
                            PlaceAddressWorkTime
from place.models import gen_file_name as place_gen_file_name
from threadedcomments.models import ThreadedComment
from private_messages2.models import Chain, Message
from django.db.models import Q


def check_username(uname):
    if User.objects.filter(username=uname).exists():
        return check_username(uname + '_')
    return uname


def import_profile():
    call_command('reset', 'auth', interactive=False)
    OLD_USERPIC_PATH = os.path.join('userpic', 'large')
    fields = ['jos_users.id', 'jos_users.username', 'jos_users.email', \
        'jos_users.registerDate','jos_users.lastvisitDate',
        'jos_users.name', 'jos_comprofiler.lastname', \
        'jos_comprofiler.avatar', 'jos_comprofiler.cb_sex', \
        'jos_comprofiler.cb_dr', 'jos_comprofiler.country', \
        'jos_comprofiler.city', 'jos_comprofiler.website',
        'jos_comprofiler.location', 'jos_comprofiler.occupation', \
        'jos_comprofiler.company', 'jos_comprofiler.address', \
        'jos_comprofiler.phone', 'jos_comprofiler.cb_interest', \
        'jos_comprofiler.interests', 'jos_users.password']

    sql = "SELECT %s FROM jos_users JOIN jos_comprofiler\
            ON jos_users.id=jos_comprofiler.user_id" % ', '.join(fields)

    cursor = db.cursor()

    cursor.execute(sql)
    all_users = cursor.fetchall()
    count = 0
    bar = progressbar.ProgressBar(maxval=len(all_users), widgets=[
        'import profile: ',
        progressbar.SimpleProgress(),
    ]).start()

    decode = lambda x: unicode(x, 'utf8')

    for row in all_users:
        username = decode(row[1])
        cyrillic = sum(1 for char in username if u'\u0400' <= char <= u'\u04FF')
        if cyrillic > 0:
            try:
                username = decode(pytils.translit.translify(username))
            except ValueError:
                username = str(datetime.now())

        username = re.sub(r'[^A-Za-z0-9_]', '_', username)

        username = check_username(username)
        if User.objects.filter(pk=row[0]):
            continue
    
        user = User(pk=row[0], username=username)

        try:
            user.last_login = datetime.strptime(str(row[4]), \
                '%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass

        try:
            user.date_joined = datetime.strptime(str(row[3]), \
                '%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass

        try:
            user.first_name = decode(row[5][:30])
        except:
            pass

        try:
            user.email = decode(row[2][:128])
        except:
            pass

        try:
            user.save()
        except:
            print user.id

        old_auth = OldAuth(user=user, password=row[20])
        old_auth.save()

        userpic = row[7]
        if userpic:
            path = os.path.join(OLD_USERPIC_PATH, userpic)
            user.profile.userpic = path

        if row[8] == 'женский':
            user.profile.sex = 'female'
        elif row[8] == 'мужской':
            user.profile.sex = 'male'
        user.profile.birthday = row[9]


        try:
            user.profile.country = decode(row[10][:50])
        except:
            pass
        try:
            user.profile.city = decode(row[11][:50])
        except:
            pass
        try:
            user.profile.web_site = row[12]
        except:
            pass
        try:
            user.profile.icq = decode(row[13][:15])
        except:
            pass
        try:
            user.profile.profession = decode(row[14])
        except:
            pass
        try:
            user.profile.company = decode(row[15])
        except:
            pass
        try:
            user.profile.address = decode(row[16])
        except:
            pass
        try:
            user.profile.phone_number = decode(row[17][:50])
        except:
            pass
        try:
            user.profile.interest = decode(str(row[18]))
        except:
            pass
        try:
            user.profile.about = decode(row[19])
        except:
            pass
        user.profile.save()

        count += 1
        bar.update(count)

    bar.finish()
    magog = User.objects.get(pk=1791)
    magog.is_staff, magog.is_superuser = True, True
    magog.save()


def import_friendship():

    def are_friends(user1, user2):
        FriendshipManager = Friendship.objects

        if user1.is_anonymous() or user2.is_anonymous():
            return FriendshipManager.none()

        if user1 == user2:
            return FriendshipManager.none()

        friendship = FriendshipManager.none()
        try:
            friendship = FriendshipManager.filter(
                    from_user=user1, to_user=user2
                ).select_related(depth=1).get()
        except Friendship.DoesNotExist:
            pass

        if not friendship:
            try:
                friendship = FriendshipManager.filter(
                    from_user=user2, to_user=user1
                ).select_related(depth=1).get()
            except Friendship.DoesNotExist:
                friendship = FriendshipManager.none()
        return friendship

    fields = ['referenceid', 'memberid', 'accepted']
    sql = "SELECT %s FROM jos_comprofiler_members ORDER BY pending DESC"% (', '.join(fields))

    cursor = db.cursor()
    insert_cursor = db.cursor()

    cursor.execute(sql)
    all_friendship = cursor.fetchall()
    count = 0
    bar = progressbar.ProgressBar(maxval=len(all_friendship), widgets=[
        'import friendship: ',
        progressbar.SimpleProgress(),
    ]).start()

    for row in all_friendship:
        sql = "select accepted from jos_comprofiler_members where referenceid=%s and memberid=%s" % (row[1], row[0])
        insert_cursor.execute(sql)
        confirm = bool(row[2])
        under_confirm = bool(insert_cursor.fetchall()[0][0])

        try:
            from_user = User.objects.get(pk=int(row[0]))
            to_user = User.objects.get(pk=int(row[1]))
        except:
            pass
        else:
            if not are_friends(from_user, to_user):
                if confirm:
                    if under_confirm is True:
                        Friendship(from_user=from_user,
                                    to_user=to_user, is_confirm=True).save()
                        #Friendship(from_user=to_user,
                        #            to_user=from_user, is_confirm=True).save()
                    elif not under_confirm is True:
                        Friendship(from_user=from_user, to_user=to_user,
                                    is_confirm=False).save()
        count += 1
        bar.update(count)
    bar.finish()


def import_message():
    fields = ['fromid', 'toid', 'toread', 'im_date', 'message']
    sql = "SELECT %s FROM jos_uddeim_in"% (', '.join(fields))

    cursor = db.cursor()

    cursor.execute(sql)
    all_messages = cursor.fetchall()
    count = 0
    bar = progressbar.ProgressBar(maxval=len(all_messages), widgets=[
            'import message: ', progressbar.SimpleProgress(),
        ]).start()

    for row in all_messages:
        sent_at = datetime.fromtimestamp(row[3])
        try:
            from_user = User.objects.get(pk=row[0])
            to_user = User.objects.get(pk=row[1])
        except:
            continue

        members = [from_user, to_user]
        chain = Chain.objects.create()
        chain.members.add(*members)
        chain.have_read.add(*members)
        chain.save()
        msg = Message(sender=from_user, sent_at=sent_at, body=row[4])
        msg.chain = chain
        msg.save()

        count += 1
        bar.update(count)
    bar.finish()

def import_tags():
    fields = ['id', 'name', 'alias']
    sql = "SELECT %s FROM jos_tegs"% (', '.join(fields))

    cursor = db.cursor()
    cursor.execute(sql)
    all_tags = cursor.fetchall()

    count = 0
    bar = progressbar.ProgressBar(maxval=len(all_tags), widgets=[
        'import tags: ',
        progressbar.SimpleProgress(),
    ]).start()

    for row in all_tags:
        Tag(pk=int(row[0]), name=str(row[1]), slug=str(row[2])).save()
        count+=1
        bar.update(count)
    bar.finish()

def import_placecat():
    fields = ['id', 'teg_id', 'ordering', 'second_name', 'published']
    sql = "SELECT %s FROM jos_places_tags WHERE parent_id=0" % (', '.join(fields));

    cursor = db.cursor()
    cursor.execute(sql)
    all_cats = cursor.fetchall()

    count = 0
    bar = progressbar.ProgressBar(maxval=len(all_cats), widgets=[
        'import place category: ',
        progressbar.SimpleProgress(),
    ]).start()
    for row in all_cats:

        tag = Tag.objects.get(pk=int(row[1]))
        place_category = PlaceCategory(pk=int(row[0]), main_tag=tag, name=str(row[3]),\
            category_mean=int(row[2]) if row[2]>0 else 1, is_published=bool(row[4]))

        place_category.save()

        sql = "SELECT teg_id FROM jos_places_tags WHERE parent_id=%s" % (place_category.pk);
        cursor = db.cursor()
        cursor.execute(sql)
        child_tags = cursor.fetchall()
        for r in child_tags:
            t=Tag.objects.get(pk=r[0])
            place_category.tagging.add(t)
        place_category.save()
        count+=1
        bar.update(count)
    bar.finish()

def import_places():
    OLD_LOGOTYPE_PATH = os.path.join(PATH_FOR_OLD_SITE, 'images/afisha/zaveds')
    OLD_PROMOPICTURE_PATH = os.path.join(PATH_FOR_OLD_SITE, 'images/places')
    content_type = ContentType.objects.get_for_model(Place)
    fields = [
        'id', #pk
        'title', #title
        'description', #description
        'url', #url
        'urlhits', #urlhits
        'email', #email
        'logotype', #logotype
        'logotype_alt', #logotype_alt
        'picture', #photo
        'picture_alt', #photo_alt
        'published', #is_published
        'promo_published', #promo_is_up
        'promo_from_date', #date_promo_up
        'promo_till_date', #date_promo_down
        'hits', #hits
    ]
    sql = "SELECT %s FROM jos_places_company" % (', '.join(fields));

    cursor = db.cursor()
    cursor.execute(sql)
    all_rows = cursor.fetchall()

    count = 0
    bar = progressbar.ProgressBar(maxval=len(all_rows), widgets=[
        'import places: ',
        progressbar.SimpleProgress(),
    ]).start()

    for row in all_rows:
        place = Place(
            pk=int(row[0]),
            name=str(row[1]),
            description=str(row[2]),
            url=str(row[3]),
            urlhits=int(row[4]),
            email=str(row[5]),
            logotype_alt=str(row[7]),
            photo_alt=str(row[9]),
            is_published=bool(row[10]),
            promo_is_up=bool(row[11]),
            hits=int(row[14])
        )
        try:
            place.date_promo_up = datetime.strptime(str(row[12]), \
                '%Y-%m-%d')
        except ValueError:
            pass
        try:
            place.date_promo_down = datetime.strptime(str(row[13]), \
                '%Y-%m-%d')
        except ValueError:
            pass

        path = os.path.join(OLD_LOGOTYPE_PATH, str(row[6]))
        if os.path.isfile(path):
             place.logotype = path
             place.logotype.save(place_gen_file_name(place, path), \
                 ContentFile(open(path, 'rb').read()))

        path = os.path.join(OLD_PROMOPICTURE_PATH, str(place.pk), 'promo_picture/big', str(row[8]))
        if os.path.isfile(path):
            place.photo = path
            place.photo.save(place_gen_file_name(place, path), \
                ContentFile(open(path, 'rb').read()))

        sql = "SELECT COUNT(*)  FROM jos_places_company_extensions  WHERE company_id=%s and extension_id=1" \
            % place.pk
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if bool(result[0][0]):
            place.is_new = True

        sql = "SELECT COUNT(*)  FROM jos_places_company_extensions  WHERE company_id=%s and extension_id=2" \
            % place.pk
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if bool(result[0][0]):
            place.expert_choice = True

        place.save()

        sql = "SELECT tag_id FROM jos_places_category WHERE company_id=%s" \
            % place.pk
        cursor = db.cursor()
        cursor.execute(sql)
        cat_list = cursor.fetchall()
        for row in cat_list:
            cat_pk = int(row[0])
            cat = PlaceCategory.objects.get(main_tag__pk=cat_pk)
            place.category.add(cat)

        sql = "SELECT teg_id FROM jos_tegs_zaveds WHERE zaved_id=%s" \
            % place.pk
        cursor = db.cursor()
        cursor.execute(sql)
        tag_list = cursor.fetchall()
        for row in tag_list:
            tag_pk = int(row[0])
            try:
                tag = Tag.objects.get(pk=tag_pk)
            except:
                pass
            else:
                place.tagging.add(tag)

        import_place_comment(content_type, place)

        place.save()

        import_address(place)

        count+=1
        bar.update(count)
    bar.finish()


def import_address(place):
    DISTRICT = {
        '0': 'none',
        '1': 'kirovskiy',
        '2': 'leninskiy',
        '3': 'oktybrakiy',
        '4': 'sovetskiy',
        '5': 'centralniy',
    }

    fields = ['id', 'mainoffice', 'address', 'geopoint',
        'district_id', 'phone', 'email']
    sql = "SELECT %s FROM jos_places_address WHERE company_id=%s" \
         % (', '.join(fields), place.pk)
    cursor = db.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        address = str(row[2]).replace('\\"', '"')
        address = PlaceAddress(
            pk=int(row[0]),
            place=place,
            is_main_office=bool(row[1]),
            address=address,
            geopoint=str(row[3]),
            district=DISTRICT[str(row[4])],
            phone=str(row[5]),
            email=str(row[6])
        )
        address.save()
        import_work_time(address)


def import_work_time(address):
    fields = [
        'id',
        'mon',
        'tue',
        'wed',
        'thu',
        'fri',
        'sat',
        'sun',
        'from_time',
        'till_time',
        'round_the_clock',
        'day_off',
    ]
    sql = "SELECT %s FROM jos_places_work_time WHERE address_id=%s" \
         % (', '.join(fields), address.pk)
    cursor = db.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        wt = PlaceAddressWorkTime(
            pk=int(row[0]),
            address=address,
            mon=bool(row[1]),
            tue=bool(row[2]),
            wed=bool(row[3]),
            thu=bool(row[4]),
            fri=bool(row[5]),
            sat=bool(row[6]),
            sun=bool(row[7]),
            from_time=time_string_parse(str(row[8])),
            till_time=time_string_parse(str(row[9])),
            all_day=bool(row[10]),
            day_off=bool(row[11])
        )
        wt.save()


def import_place_comment(content_type, place):
    comment = ThreadedComment()
    comment.content_type = content_type
    comment.site_id = settings.SITE_ID


def time_string_parse(s):
    try:
        if not s:
            t = time(0,0,0)
        elif len(s) == 3:
            h = int(s[0])
            if h == 24:
                h = 0
            t = time(h,int(s[1:]),0)
        elif len(s) == 4:
            h = int(s[0:2])
            if h == 24:
                h = 0
            t = time(h,int(s[2:]),0)
        else:
            t = None
    except:
        print
        print 's='+s
        raise
    return t


class Command(BaseCommand):
    def handle(self, *args, **options):
        if 'all' in args:
            run_all = True
        else:
            run_all = False

        if 'profile' in args or run_all:
            print 'start import profile:'
            import_profile()

        if 'friendship' in args or run_all:
            print 'start import friendship:'
            import_friendship()

        if 'message' in args or run_all:
            print 'start import message:'
            import_message()

        if 'tags' in args or run_all:
            print 'start import tags:'
            import_tags()

        if 'placecat' in args or run_all:
            print 'start import place category:'
            import_placecat()

        if 'places' in args or run_all:
            print 'start import places:'
            import_places()