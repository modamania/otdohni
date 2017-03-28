from optparse import make_option
from apps.common.utils import load_subscribers
from django.core.management.base import BaseCommand

from django.core.management import call_command

from common.utils import (load_news, load_places, load_photoreports,
                          load_comment, load_category, load_event,
                          load_action, load_rating, load_taxi,
                          load_tea, replace_media_urls)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--conn', '-c',
                        dest='conn',
                        default='otdohni_old',
                        help='Set connection for chose database.'),
            )
    help = "Load data from database with `connection` alias to news, photoreport, place, threadcomment apps"

    def handle(self, *args, **options):
        if 'all' in args:
            load_places(conn=options['conn'])
            load_taxi(conn=options['conn'])
            load_news(conn=options['conn'])
            load_category(options['conn'])
            load_event(options['conn'])
            load_action(options['conn'])
            load_tea(options['conn'])

            call_command('reset', 'photoreport', interactive=False)
            load_photoreports(conn=options['conn'])

            call_command('reset', 'threadedcomments', interactive=False)
            load_comment(options['conn'], 'news', 'newsitem')
            load_comment(options['conn'], 'action', 'action')
            load_comment(options['conn'], 'event', 'event')
            load_comment(options['conn'], 'place', 'place')
            load_comment(options['conn'], 'photoreport', 'photo')

            call_command('reset', 'rating', interactive=False)
            load_rating(options['conn'], 'place', 'place')
            load_rating(options['conn'], 'photoreport', 'photo')
            load_rating(options['conn'], 'event', 'event')

        if 'category' in args:
            load_category(options['conn'])

        if 'places' in args:
            load_places(conn=options['conn'])

        if 'taxi' in args:
            load_taxi(conn=options['conn'])

        if 'news' in args:
            load_news(conn=options['conn'])

        if 'photoreport' in args:
            call_command('reset', 'photoreport', interactive=False)
            load_photoreports(conn=options['conn'])

        if 'event' in args:
	    call_command('reset', 'event', interactive=False)
	    load_category(options['conn'])
            load_event(options['conn'])

        if 'action' in args:
	    call_command('reset', 'action', interactive=False)
            load_action(options['conn'])

        if 'tea' in args:
	    call_command('reset', 'tea', interactive=False)
            load_tea(options['conn'])

        if 'comments' in args:
            call_command('reset', 'threadedcomments', interactive=False)
            load_comment(options['conn'], 'news', 'newsitem')
            load_comment(options['conn'], 'action', 'action')
            load_comment(options['conn'], 'event', 'event')
            load_comment(options['conn'], 'place', 'place')
            load_comment(options['conn'], 'photoreport', 'photo')

        if 'rating' in args:
            call_command('reset', 'rating', interactive=False)
            load_rating(options['conn'], 'place', 'place')
            load_rating(options['conn'], 'photoreport', 'photo')
            load_rating(options['conn'], 'event', 'event')

        if 'replace_media_urls' in args:
            replace_media_urls(new='tea/old', app_label='tea', model='interview', field='image', new_path='')
            replace_media_urls(new='tea/old', app_label='tea', model='interview')
            replace_media_urls('stories', 'news/old', 'action', 'action', 'full_text')
            replace_media_urls('stories', 'news/old', 'action', 'workbidder', 'text')
            replace_media_urls('stories', 'news/old', 'news', 'newsitem', 'full_text')
            replace_media_urls('stories', 'news/old', 'place', 'place', 'description')

        if 'subscribers' in args:
            load_subscribers(options['conn'])
        
        replace_media_urls(new='tea/old', app_label='tea', model='interview', field='image', new_path='')
        replace_media_urls(new='tea/old', app_label='tea', model='interview')
        replace_media_urls('stories', 'news/old', 'action', 'action', 'full_text')
        replace_media_urls('stories', 'news/old', 'action', 'workbidder', 'text')
        replace_media_urls('stories', 'news/old', 'news', 'newsitem', 'full_text')
