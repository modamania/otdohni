from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator

from models import Chain
from forms import MessageForm, MessageSimpleForm

from annoying.functions import  get_object_or_None


class MessageMixin(TemplateView):
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(MessageMixin, self).dispatch(request, *args, **kwargs)

    def to_inbox(self):
        return HttpResponseRedirect(reverse('messages_inbox'))

    def to_chain(self, pk):
        return HttpResponseRedirect(reverse('messages_view', args=[pk]))

    @property
    def session(self):
        return self.request.session

    @property
    def user(self):
        return self.request.user


class Inbox(MessageMixin):
    template_name = 'messages/inbox.html'

    def get_context_data(self, **kwargs):
        session = self.session
        chain_list = [
            [chain, self.user in chain.have_read.all()]
            for chain in Chain.objects.inbox(self.user)
        ]

        if not session.get('show_recently_deleted', False):
            deleted_messages = session.get('recently_deleted', [])
            chain_count = len(deleted_messages)
            session['show_recently_deleted'] = True
        else:
            chain_count = 0
            session['recently_deleted'] = []

        return {
            "chain_list": chain_list,
            "undo_count": chain_count,
        }


class View(MessageMixin):
    template_name = 'messages/view.html'

    def get(self, request, pk):
        chain = get_object_or_404(Chain, pk=int(pk))
        if self.user not in chain.members.all():
            return self.to_inbox()
        chain.have_read.add(self.user)
        form = MessageSimpleForm(
                initial={
                    'chain': chain,
                    'sender': self.user,
        })
        return self.render_to_response({
            'chain': chain,
            'other_users': chain.members.all().exclude(id=self.request.user.pk),
            'message_list': chain.messages.all().order_by('sent_at', 'id') \
                .prefetch_related('sender', 'sender__profile'),
            'form': form,
        })

    def post(self, request, pk):
        form = MessageSimpleForm(request.POST)
        if form.is_valid():
            message = form.save()
            message.chain.have_read = [self.user,]
        return self.to_chain(pk)


class Delete(MessageMixin):
    def remove_chain(self, chain):
        chain.make_as_delete(self.user)
        self.recently_deleted.append(chain.pk)

    def get(self, request, pk=None):
        self.recently_deleted = []

        m_id = request.GET.getlist('m_id')
        if not pk and m_id:
            for key in m_id:
                chain = get_object_or_None(Chain, pk=key)
                if chain:
                    self.remove_chain(chain)
            if not self.recently_deleted:
                raise Http404
        else:
            chain = get_object_or_404(Chain, pk=pk)
            self.remove_chain(chain)
        messages.add_message(request, messages.INFO, _(u"Message successfully deleted."))
        self.session['recently_deleted'] = self.recently_deleted
        self.session['show_recently_deleted'] = False
        return self.to_inbox()


class Undelete(MessageMixin):
    def get(self, request):
        recently_deleted = self.session.pop('recently_deleted')
        for pk in recently_deleted:
            chain = get_object_or_None(Chain, pk=pk)
            if chain:
                chain.removed.remove(self.user)
        return self.to_inbox()


class Compose(MessageMixin):
    template_name = 'messages/compose.html'

    def get(self, request, to=''):
        initial = {}
        if to:
            initial['recipient'] = get_object_or_404(User, pk=to)
        return self.render_to_response({
            'form': MessageForm(initial=initial),
        })

    def post(self, request, to=''):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            chain = Chain.objects.create()
            chain.members.add(*form.cleaned_data['recipient'])
            chain.members.add(self.user)
            chain.have_read.add(self.user)
            chain.save()

            message.chain = chain
            message.sender = self.user
            message.save()

            return self.to_inbox()
        return self.get(request)


class Unread(MessageMixin):
    def get(self, request):
        m_id = request.GET.getlist('m_id')
        if m_id:
            for key in m_id:
                chain = get_object_or_404(Chain, pk=key)
                chain.make_as_unread_by_user(self.user)
        return self.to_inbox()

class Read(MessageMixin):
    def get(self, request):
        m_id = request.GET.getlist('m_id')
        if m_id:
            for key in m_id:
                chain = get_object_or_404(Chain, pk=key)
                chain.make_as_read(self.user)
        return self.to_inbox()
