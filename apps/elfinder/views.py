# Create your views here.
from django.shortcuts import render_to_response
from django.conf import settings
from elFinder import connector as api
from django.utils import simplejson as json
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import  csrf_exempt

@staff_member_required
def elfinder(request):
  return render_to_response('elfinder.html', {"STATIC_URL":settings.STATIC_URL})

@staff_member_required
@csrf_exempt
def connector(request):
  try:
    finder = api(settings.ELFINDER)
  except:
    response = {}
    response['error'] = 'Invalid backend configuration'
    return HttpResponse(json.dumps(response),mimetype='application/json')

  if request.POST:
    if "cmd" in request.POST and request.POST["cmd"] == "upload":
      request.POST['upload[]'] = request.FILES.getlist('upload[]')

    finder.run(request.POST)
    return HttpResponse(json.dumps(finder.httpResponse))

  finder.run(request.GET)

  ret = HttpResponse(mimetype=finder.httpHeader["Content-type"])

  if finder.httpHeader["Content-type"] == "application/json":
    ret.content = json.dumps(finder.httpResponse)
  else:
    ret.content = finder.httpResponse

  for head in finder.httpHeader:
    if head != "Content-type":
      ret[head] =  finder.httpHeader[head]
  ret.status_code = finder.httpStatusCode
  return ret
