from django.urls import path
from .views import   *

urlpatterns = [
    path("admin-login/", AdminLoginView.as_view()),
    path("create-customer/", CustomerCreateView.as_view()),
    path('customer-detail/<int:id>', CustomerDetailView.as_view()),
    path('customers-under-me/', GetCustomersUnderMeView.as_view()),
    path('dashboard/', DashBoardView.as_view()),

]