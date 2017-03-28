from optparse import make_option
from django.core.management.base import BaseCommand

from common.utils import replace_media_urls

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--old-path', '-o',
                        dest='oldpath',
                        default='stories',
                        help='old path for replace'),
        make_option('--new-path', '-n',
                        dest='newpath',
                        default='news',
                        help='new path for replace'),
            )
    help = """Replace in news.full_text if url equal http://www.otdonhiomsk.ru/images/<old_path> to /media/<new_path>. Without arguments replace http://www.otdonhiomsk.ru/images/stories to /media/news"""

    def handle(self, *args, **options):
        total_count = replace_media_urls(old=options['oldpath'],
                                        new=options['newpath'])
        self.stdout.write('Replaced %d urls...\n' % total_count)
