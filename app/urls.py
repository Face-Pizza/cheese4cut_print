from django.urls import path
from .views import print_file, get_print_status  # get_print_status 추가

urlpatterns = [
    path('print/', print_file, name='print_file'),  # 프린트 요청
    path('print-status/', get_print_status, name='get_print_status'),  # 프린터 상태 확인 요청
]
