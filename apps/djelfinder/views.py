# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from django.utils import simplejson as json
from django.contrib.admin.views.decorators import staff_member_required

#@staff_member_required
def index(request):
	tmp = loader.get_template('index.html')
	con = Context(RequestContext(request))
	out = tmp.render(con)
	return HttpResponse(out)

def upload_form_tag(request):
	from django.template import loader, RequestContext
	tmp = loader.get_template('upload_form.html')
	out = tmp.render(RequestContext(request))
	return HttpResponse(out)

#@staff_member_required
def connector(request):
    from djelfinder.operations import *
    init = request.GET.get('init', False)
    cmd = request.GET.get('cmd', None)
    if cmd == 'upload_form':
            return upload_form_tag(request)
    target = request.GET.get('target',None)
    cur = request.GET.get('current', None)
    if request.POST.has_key('cmd'):
            cmd = request.POST.get('cmd', cmd)
            cur = request.POST.get('current', cur)
            target = request.POST.get('target', target)
    target_path = find_path(target)
    cur_path = find_path(cur)
    out = run(request, init=init, target=target_path, cmd=cmd, current=cur_path)
    out = json.dumps(out)
    return HttpResponse(out, mimetype='application/javascript')
