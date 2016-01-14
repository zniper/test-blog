from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages import success, error
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models import ObjectDoesNotExist, Q
from django.conf import settings

import re

from logging import getLogger
from haystack.query import SearchQuerySet

from .models import Entry, Category
from .forms import EntryForm

User = get_user_model()

MODEL_MAPS = {
    'categories': Category,
    'editor': User
}

logger = getLogger(__name__)


class PostEntryView(LoginRequiredMixin, generic.CreateView):
    """
    View for authenticated users to post new entry.
    """
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
        return reverse('content:view_entry', kwargs={'pk': self.object.pk})


class EditEntryView(LoginRequiredMixin, UserPassesTestMixin,
                    generic.UpdateView):
    """
    View for editor or admin to edit existing entry.
    """
    model = Entry
    form_class = EntryForm

    def get_success_url(self):
        success(self.request,
                _('Congratulations! This has been successfully updated.'))
        return reverse('content:view_entry', kwargs={'pk': self.object.pk})

    def test_func(self):
        """Check the permission of current user on editing this entry."""
        user = self.request.user
        entry = self.get_object()
        if user.is_staff or user == entry.editor:
            return True
        error(self.request,
              _('Sorry, you don\'t have permission to edit that entry.'))


class SingleEntryView(generic.DetailView):
    # Displays full content of a given entry. Visible to everyone.
    model = Entry


class EntryListView(generic.ListView):
    """
    List multiple of entries with brief information. The view has pagination,
    and content can be filtered by editor or category.
    """
    template_name = "content/entries.html"
    model = Entry
    paginate_by = 3
    target = None

    def get_queryset(self):
        """Additionally filter the result by given field"""
        queryset = super(EntryListView, self).get_queryset()
        filter_by = self.request.GET.get('by')
        target_id = self.request.GET.get('id')
        if filter_by and target_id:
            queryset = queryset.filter(**{filter_by: target_id})
        # Get the target object
        try:
            self.target = MODEL_MAPS[filter_by].objects.get(pk=target_id)
        except ObjectDoesNotExist:
            logger.exception('Cannot filter by [{0}, {1}]'.format(
                filter_by, target_id))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        context['target_name'] = getattr(self.target, 'username', None) or \
            getattr(self.target, 'name', None) or ''
        return context


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    """Find the term in query string and reduce redundant spaces."""
    return [normspace(' ', (t[0] or t[1]).strip())
            for t in findterms(query_string)]


def get_query(query_string, search_fields):
    """Search for present of all terms in search fields."""
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field in search_fields:
            q = Q(**{field+'__icontains': term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


class SearchResultView(generic.ListView):
    # Displays list of entries matching with submitted query.
    template_name = 'content/search_results.html'
    paginate_by = 3

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        results = []
        if settings.USE_HAYSTACK:
            results = SearchQuerySet().filter(content=q) if q else []
        else:
            query = get_query(q, ['title', 'text', 'categories__name'])
            if query:
                results = Entry.objects.filter(query)
        return results

    def get_context_data(self, **kwargs):
        """
        Paginated items will be converted to real objects in order to be
        correctly displayed in result page.
        """
        context = super(SearchResultView, self).get_context_data(**kwargs)
        if settings.USE_HAYSTACK:
            pks = [item.pk for item in context['object_list']]
            context['object_list'] = Entry.objects.filter(pk__in=pks)
        context['query'] = self.request.GET.get('q')
        return context
