#core/urls.py
from django.urls import path, include
from .views import (
    login_view,
    logout_view,
    scan_view,
    admin_panel,
    program_select,  # ✅ 추가
)

urlpatterns = [
    path('', login_view, name='login'),  # ⬅ 이 줄을 수정
    path('scan/', scan_view, name='scan_view'),
    path('program-select/', program_select, name='program_select'),
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('logout/', logout_view, name='logout'),
    path('programs/', include('product_program.urls')),
    path('product-info/', include('product_info.urls')),
    path('product-check/', include('product_check.urls')),
]
