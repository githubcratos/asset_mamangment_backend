from django.contrib import admin
from django.urls import include, path

from asset.views import get_asset_name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('asset.urls')),
    path('qr-code/<int:id>/', get_asset_name, name='asset-qr-code'),
]
