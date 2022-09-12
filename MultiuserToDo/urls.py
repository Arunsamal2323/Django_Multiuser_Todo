
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from task.sitemaps import StaticViewSitemap
from task import views
router = routers.SimpleRouter()

sitemaps = {
    'static': StaticViewSitemap
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('task/', include('task.urls')),
    # path('', include(router.urls)),
    path('', views.index, name='index'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "MultiuserToDo Admin"
admin.site.site_title = "MultiuserToDo Admin Site"
admin.site.index_title = "Welcome to MultiuserToDo Portal"