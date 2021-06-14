from django.conf.urls import url
from Workers import views

urlpatterns = [
    url(r'^worker/$',           views.workerApi),
    url(r'^worker/([0-9]+)$',   views.workerApi),
    url(r'^test-worker/$',      views.testWorkerApi),
    url(r'^parser/[-a-z0-9]+/$', views.parserSetGetApi),
    url(r'^parser/$',           views.parserEditApi)
]