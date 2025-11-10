"""
URL configuration for my_app project.

The `urlpatterns` list routes URLs to api. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function api
    1. Add an import:  from my_app import api
    2. Add a URL to urlpatterns:  path('', api.home, name='home')
Class-based api
    1. Add an import:  from other_app.api import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import get_resolver
from django.urls import path

from .api import api
from .views import health_view


def debug_urls(request):
    resolver = get_resolver()
    url_patterns = []

    def list_urls(patterns, prefix=""):
        for pattern in patterns:
            if hasattr(pattern, "url_patterns"):
                list_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            else:
                url_patterns.append(
                    {
                        "pattern": prefix + str(pattern.pattern),
                        "name": getattr(pattern, "name", "No name"),
                        "callback": str(pattern.callback),
                    }
                )

    list_urls(resolver.url_patterns)
    return JsonResponse({"urls": url_patterns})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("health/", health_view),
    path("debug-urls/", debug_urls),
]
