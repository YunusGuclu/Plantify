from django.urls import path
from .views import home, start_workflow, task_status,products,all_products,product_detail

urlpatterns = [
  # API uçlarınızı bir “api/” prefix’iyle gruplayın
  path('api/start/', start_workflow, name='start_workflow'),
  path('api/status/', task_status, name='task_status'),
  path('api/products/', products, name='products'),
  # Vue geliştirme esnasında Django sadece API sunacak:
  path('api/all-products/', all_products, name='all_products'),
  path('api/products/<str:name>/', product_detail, name='product_detail'),
  path('', home, name='home'),
]
