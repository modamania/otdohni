# -*- coding: utf-8 -*-
from django import template
from django.template.loader import render_to_string

from action.models import WorkBidder


register = template.Library()

VOTE_BUTTON_TEMPLATE = template.Template('''
<span class="btn_wrapper like-button"><ins class="l"></ins><ins class="r"></ins>
<a href="{% url liked_work poll.id work.id %}" class="btn">Голосовать</a>
</span>
''')

# Нужно перенести логику из этого шаблона в шаблонный тег vote_button
STUPID_TEMPLATE = template.Template('''
{% if work in user_votes %}
    {% for work_voted in user_votes %}
        {% if work == work_voted %}
            {% with work.work_votes.all|first as vote %}
                {% if poll.vote_frequency == 'ONCE' or poll.vote_frequency == 'DAY' and now == vote.vote_date or  poll.vote_frequency == 'WEEK' and now >= vote.vote_date and now <= vote.in_a_week %}
                    <div class="current-votes">Спасибо за Ваш голос!
                        {% if poll.vote_frequency == 'DAY' %}Завтра Вы сможете проголосовать еще раз.{% endif %}
                        {% if poll.vote_frequency == 'WEEK' %}Через неделю Вы сможете проголосовать еще раз.{% endif %}
                    </div>
                {% else %}
                    {% if poll.status != 'NONE' %}
                        {% if user.date_joined.date < poll.start_date and poll.can_vote == 'OLD' or poll.can_vote == 'ALL' %}

                        {% else %}
                            <div class="current-votes">Вы не можете голосовать за эту работу.</div>
                        {% endif %}
                    {% endif %}
                {% endif %}
            {% endwith %}
        {% endif %}
    {% endfor %}
{% else %}
    {% if poll.status != 'NONE' %}
        {% if user.date_joined.date < poll.start_date and poll.can_vote == 'OLD' or poll.can_vote == 'ALL' %}

        {% else %}
            <div class="current-votes">Вы не можете голосовать за эту работу.</div>
        {% endif %}
    {% endif %}
{% endif %}
''')

@register.simple_tag(takes_context=True)
def poll_detail(context):
	#action = get_object_or_404(Action, slug=action_slug)
	user_votes = []
	if not context['user'].is_anonymous():
	    user_votes = WorkBidder.objects.filter(work_votes__user=context['user'], poll=context['poll']).distinct()
	context.update({
		'user_votes': user_votes
		})
	template = 'action/poll_detail_as_%s.html' % context['poll'].display_type
	return render_to_string(template, context)

@register.simple_tag(takes_context=True)
def vote_button(context, poll, work, user):
	try:
		if poll.can_add_like(user, work):
			return VOTE_BUTTON_TEMPLATE.render(context)
		else:
			return STUPID_TEMPLATE.render(context)
	except:
		pass
	return ''