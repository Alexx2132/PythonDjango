from django.urls import path

from .views import *
from .classurl import FourDigitYearConverter
register_converter(FourDigitYearConverter, "yyyy")

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('students/<int:studid>/', students_id),
    path('students/', students_mainpage, name='mpage'),
    path('raise_err_400', e_400),
    path('raise_err_500', e_500),
    path('raise_err_403', e_403),
    path('years/<yyyy:year_id>/', year),
]