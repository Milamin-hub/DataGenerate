from django.urls import path
from generate.views import GenerateCSVView


urlpatterns = [
    path('generate-csv/', GenerateCSVView.as_view(), name='generate_csv'),
]