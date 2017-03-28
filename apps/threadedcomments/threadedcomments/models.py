from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.comments.managers import CommentManager
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from annoying.fields import AutoOneToOneField


PATH_SEPARATOR = getattr(settings, 'COMMENT_PATH_SEPARATOR', '/')
PATH_DIGITS = getattr(settings, 'COMMENT_PATH_DIGITS', 10)
RELATE_CHOICE = (
    ('0', '0'),
    ('+', '+'),
    ('-', '-'),
)

class ThreadedComment(Comment):
    title = models.TextField(_('Title'), blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, default=None,
        related_name='children', verbose_name=_('Parent'))
    last_child = models.ForeignKey('self', null=True, blank=True,
        verbose_name=_('Last child'))
    tree_path = models.TextField(_('Tree path'), editable=False)
        #db_index=True)

    objects = CommentManager()

    __like = None
    __like_users = None
    __nolike = None
    __nolike_users = None

    def _get_depth(self):
        return len(self.tree_path.split(PATH_SEPARATOR))
    depth = property(_get_depth)

    def _root_id(self):
        return int(self.tree_path.split(PATH_SEPARATOR)[0])
    root_id = property(_root_id)

    def _root_path(self):
        return ThreadedComment.objects.filter(pk__in=self.tree_path.
                                              split(PATH_SEPARATOR)[:-1])
    root_path = property(_root_path)

    def save(self, *args, **kwargs):
        skip_tree_path = kwargs.pop('skip_tree_path', False)
        super(ThreadedComment, self).save(*args, **kwargs)
        if skip_tree_path:
            return None

        tree_path = unicode(self.pk).zfill(PATH_DIGITS)
        if self.parent:
            tree_path = PATH_SEPARATOR.join((self.parent.tree_path, tree_path))

            self.parent.last_child = self
            ThreadedComment.objects.filter(pk=self.parent_id).update(
                last_child=self)

        self.tree_path = tree_path
        ThreadedComment.objects.filter(pk=self.pk).update(
            tree_path=self.tree_path)

    def __get_relate(self):
        relate_list = self.relate.select_related().all()
        self.__like = []
        self.__nolike = []
        for r in relate_list:
            if r.relate == '+':
                self.__like.append(r)
            elif r.relate == '-':
                self.__nolike.append(r)

    def __get_like(self):
        if self.__like is None:
            self.__get_relate()
        return self.__like

    like = property(__get_like)

    def __get_like_users(self):
        if self.__like_users is None:
            self.__like_users = [l.user for l in self.like]
        return self.__like_users

    like_users = property(__get_like_users)

    def __get_nolike(self):
        if self.__nolike is None:
            self.__get_relate()
        return self.__nolike

    nolike = property(__get_nolike)

    def __get_nolike_users(self):
        if self.__nolike_users is None:
            self.__nolike_users = [l.user for l in self.nolike]
        return self.__nolike_users

    nolike_users = property(__get_nolike_users)

    class Meta(object):
        ordering = ('tree_path',)
        db_table = 'threadedcomments_comment'
        verbose_name = _('Threaded comment')
        verbose_name_plural = _('Threaded comments')

class RelatedComment(models.Model):
    comment = models.ForeignKey(ThreadedComment, related_name='relate')
    user = models.ForeignKey(User)
    relate = models.CharField(max_length=1, choices=RELATE_CHOICE, default=0)
