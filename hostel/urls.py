from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # root path
    path('student/signup/', views.student_signup, name='student_signup'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('complaint/', views.submit_complaint, name='submit_complaint'),
    path('student/request-room/', views.request_room, name='request_room'),
    path('rooms/', views.view_rooms, name='view_rooms'),
    path('student/pay-fee/', views.pay_fee, name='pay_fee'),
    path('admin/approve-fee/<int:fee_id>/', views.approve_fee, name='approve_fee'),
    path('student/payment-status/', views.payment_status, name='payment_status'),
    path('student/receipt/<int:fee_id>/', views.view_receipt, name='view_receipt'),
    path('student/room-change-request/', views.room_change_request, name='room_change_request'),
    path('profile/', views.student_profile, name='student_profile'),
]
