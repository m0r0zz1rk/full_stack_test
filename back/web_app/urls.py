from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.common.utils.django.settings import get_settings_parameter
from web_app.yasg import urlpatterns as yasg_urls


urlpatterns = [
    path('backend/admin/', admin.site.urls),
    path('backend/api/v1/product/', include('apps.product.urls'))
]


# Подключение статики для корректной работы с CSS в админке и свагере
urlpatterns += static(
    get_settings_parameter('STATIC_URL'),
    document_root=get_settings_parameter('STATIC_ROOT')
)
urlpatterns += static(
    get_settings_parameter('MEDIA_URL'),
    document_root=get_settings_parameter('MEDIA_ROOT')
)
# Присоединение URL для swagger
urlpatterns += yasg_urls
