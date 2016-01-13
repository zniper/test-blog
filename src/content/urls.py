from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new-entry/$', views.PostEntryView.as_view(), name='post-entry'),
    url(r'^entry-(?P<pk>\d+)/$', views.SingleEntryView.as_view(),
        name='view-entry'),
]