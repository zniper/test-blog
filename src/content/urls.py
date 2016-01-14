from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new-entry/$', views.PostEntryView.as_view(), name='post-entry'),
    url(r'^entries/$', views.EntryListView.as_view(), name='entry-list'),
    url(r'^entry-(?P<pk>\d+)/$', views.SingleEntryView.as_view(),
        name='view-entry'),
    url(r'^search/', views.SearchResultView.as_view(), name='blog-search'),
]
