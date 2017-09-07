# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, url, include
from domanayuge.views import Blog, Article, \
    send_email, RemontPage, RemontList, RemontPrice,\
    RemontCaseList, RemontCase, robots, RemontPriceList
from django.contrib.sitemaps.views import sitemap
import settings
from domanayuge.models import ContentEntry
from domanayuge.sitemaps import get_sitemap_dict


admin.autodiscover()

urlpatterns = patterns('',   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^content_edit/', include('content_edit.urls')),
    url(r'^$', RemontPage.as_view() ,name='remontpage'),
    url(r'^projects/(?P<key>[-\w]+)/$', RemontList.as_view(), name='projects'),
    url(r'^prices/(?P<key>[-\w]+)/$', RemontPriceList.as_view(), name='prices'),
    url(r'^price/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', RemontPrice.as_view(), name='price'),        
    url(r'^blog/$', Blog.as_view(), name='blog'),
    url(r'^blog/(?P<slug>[-\w]+)/$', Article.as_view(), name='page'),
    url(r'^cases/(?P<key>[-\w]+)/$', RemontCaseList.as_view(), name='cases'),
    url(r'^cases/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', RemontCase.as_view(), name='case'),
    url(r'^sendemail/$', send_email, name='send_email'),
)

blog_dict = {
    'queryset': ContentEntry.objects.filter(categories__slug="blog", tags__contained_by=[u'ремонт']),
    'date_field': 'publication_date',
}

urlpatterns += patterns('',
        url(r'^sitemap\.xml$', sitemap,
        {'sitemaps':get_sitemap_dict([u'ремонт'], 'portfolioremont', None, 'remontprices')},
        name='django.contrib.sitemaps.views.sitemap'),        
        url(r'^robots\.txt$', robots),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))