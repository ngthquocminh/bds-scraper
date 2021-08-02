from django.conf.urls import url
from Workers import views

urlpatterns = [
    url(r'^test/$',                 views.test),
    url(r'^worker/$',               views.workerApi),
    url(r'^worker/([0-9]+)$',       views.workerApi),
    url(r'^test-worker/$',          views.testWorkerApi),
    url(r'^parser/[-a-z0-9]+/$',    views.parserSetGetApi),
    url(r'^parser/$',               views.parserEditApi),
    url(r'^test-parser/$',          views.testParserApi),
    url(r'^load-post-html/$',       views.loadPostHtml),
    url(r'^do-crawl/$',             views.doCrawlApi),
    url(r'^do-parse/$',             views.doParseApi),
    url(r'^worker-info/$',          views.getWorkerInfoApi),
    url(r'^pause-worker/$',         views.pauseWorkerApi),
    url(r'^stop-worker/$',          views.stopWorkerApi),
    url(r'^stop-all-worker/$',      views.stopAllWorkerApi),
    url(r'^toggle-shield/$',        views.toggleShieldApi)
]