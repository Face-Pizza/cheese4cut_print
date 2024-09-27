from django.urls import path
from .views import print_file  # views.py에서 print_file 함수 가져오기

urlpatterns = [
    path('print/', print_file, name='print_file'),  # /api/print로 요청 시 print_file 함수 호출
]