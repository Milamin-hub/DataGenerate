from django.urls import path
from generate.views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('generate-csv/', GenerateCSVView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)