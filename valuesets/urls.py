from django.urls import path
from . import views

urlpatterns = [
    path('', views.value_set_list, name='value_set_list'),
    path('<int:value_set_id>/', views.value_set_detail, name='value_set_detail'),
    path('comparison/', views.value_set_comparison, name='value_set_comparison'),
]
