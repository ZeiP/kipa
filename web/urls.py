from __future__ import absolute_import
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from tupa.views import raportti_500

admin.autodiscover()

urlpatterns = [
    url(r"^kipa/", include("tupa.urls")),
    url(r"^admin/", admin.site.urls),
]

if settings.SERVE_MEDIA:
    urlpatterns += [
        url(
            r"^kipamedia/(?P<path>.*)$",
            serve,
            {"document_root": settings.STATIC_DOC_ROOT},
        )
    ]

handler500 = raportti_500
