from apps.specprojects.models import SpecProject

def spec_menu(request):
    spec_menu = SpecProject.objects.top_menu()

    return {'spec_menu': spec_menu}
