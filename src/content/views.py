from django.views.generic import CreateView, DetailView
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success
from django.utils.translation import ugettext_lazy as _

from .models import Entry
from .forms import EntryForm


class PostEntryView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm

    def form_valid(self, form):
        # Inject the current user into entry object
        self.object = form.save(commit=False)
        self.object.editor = self.request.user
        return super(PostEntryView, self).form_valid(form)

    def get_success_url(self):
        success(self.request,
                _('Congratulations! New entry has been published.'))
        return reverse('content:view-entry', kwargs={'pk': self.object.pk})


class SingleEntryView(DetailView):
    model = Entry
