"""
URL configuration for FutManagerBE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from .admin import admin_site

urlpatterns = [
    path("", include("field.urls")),
    path("", include("payment.urls")),
    path("", include("help.urls")),
    path("", include("service.urls")),
    path("", include("review.urls")),
    path("", include("user.urls")),
    path("", include("notifications.urls")),
    path("admin/", admin_site.urls),
]
