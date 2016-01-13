from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import FieldError

from .models import Entry
from .forms import EntryForm


class PostEntryView(LoginRequiredMixin, generic.CreateView):
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


class SingleEntryView(generic.DetailView):
    model = Entry


class EntryListView(generic.ListView):
    template_name = "content/entries.html"
    model = Entry
    paginate_by = 3

    def get_queryset(self):
        """Additionally filter the result by given field"""
        queryset = super(EntryListView, self).get_queryset()
        filter_by = self.request.GET.get('by')
        target_id = self.request.GET.get('id')
        if filter_by and target_id:
            queryset = queryset.filter(**{filter_by: target_id})
        return queryset
