from django.contrib.comments.views.comments import post_comment as contrib_post_comment

def post_comment(request):
    redirect = contrib_post_comment(request)
    if 'Location' in redirect:
        redirect['Location'] = redirect['Location'].replace('?c=', '#comments-')
    return redirect
