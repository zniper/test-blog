from django.views import generic

from content.models import Entry


class HomePage(generic.ListView):
    template_name = "home.html"
    model = Entry
    paginate_by = 3


class AboutPage(generic.TemplateView):
    template_name = "about.html"
