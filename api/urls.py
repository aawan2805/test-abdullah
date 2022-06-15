from django.urls import path
from api.views import CompanyView

urlpatterns = [
    path('inpsections?company=<str:company>', CompanyView.as_view()),
]
