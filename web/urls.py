from __future__ import absolute_import
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.views.static import serve

from tupa.views import raportti_500

admin.autodiscover()

urlpatterns = [
    path("kipa/", include("tupa.urls")),
    path("admin/", admin.site.urls),
]

if settings.SERVE_MEDIA:
    urlpatterns += [
        path(
            "kipamedia/<path>",
            serve,
            {"document_root": settings.STATIC_DOC_ROOT},
        )
    ]

handler500 = raportti_500
