from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new-entry/$', views.PostEntryView.as_view(), name='post_entry'),
    url(r'^entries/$', views.EntryListView.as_view(), name='entry_list'),
    url(r'^entry-(?P<pk>\d+)/$', views.SingleEntryView.as_view(),
        name='view_entry'),
    url(r'^entry-(?P<pk>\d+)/edit$', views.EditEntryView.as_view(),
        name='edit_entry'),
    url(r'^search/', views.SearchResultView.as_view(), name='blog_search'),
]
