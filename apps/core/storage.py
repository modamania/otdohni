import os
from django.core.files.storage import FileSystemStorage

from django.conf import settings

STORAGE_ROOT = os.path.join(settings.PROJECT_DIR,
                            settings.FILES_MEDIA_PREFIX)

fs = FileSystemStorage(location=STORAGE_ROOT, base_url='/')


class CustomStorage(FileSystemStorage):

    def __init__(self, location=STORAGE_ROOT, base_url='/', *args, **kwargs):
        super(CustomStorage, self).__init__(*args,
                        location=STORAGE_ROOT, base_url='/media/', **kwargs)
