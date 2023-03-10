from django.urls import path
from generate.views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('generate-csv/', GenerateCSVView.as_view(), name='home'),
    path('create-schema/', CreateSchemaView.as_view(), name='create_schema'),
    path('add-field/', AddFieldView.as_view(), name='add_field'),
    path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)