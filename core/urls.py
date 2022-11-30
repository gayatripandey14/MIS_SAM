"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls


schema_view = get_schema_view(
    openapi.Info(
        title="Celetel",
        default_version='v0.1.0',
        description="Celetel",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('mis-sam/admin/', admin.site.urls),
    path("mis-sam/test/", include("testapp.urls")),
    path("mis-sam/users/", include("users.urls")),
    path("mis-sam/smpp/", include("smpp.urls")),
    path("mis-sam/services/", include("smsroutes.urls")),
    path("mis-sam/wallet/", include("wallet.urls")),
    path("mis-sam/campaigns/", include("campaignmanager.urls")),
    path("mis-sam/analytics/", include("analytics.urls")),
    path('mis-sam/docs/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
]
