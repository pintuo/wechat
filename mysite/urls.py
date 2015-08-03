from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^polls', include('polls.urls',namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^weixin', 'weixin.views.index'),
    url(r'^index', 'netbar.views.index'),
    url(r'^netbar_reservePC','netbar.views.reservePC'),
    url(r'^product','netbar.views.product'),
    url(r'^single','netbar.views.single'),
    url(r'^eleme','netbar.views.eleme'),
    url(r'^lottery','netbar.views.lottery'),
    url(r'^login','netbar.views.login'),
)
