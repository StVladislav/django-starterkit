from django.urls import path, include
from src._test import views


urlpatterns = [
    path('product_search/', views.search_product, name='product-search'),
    path('run_celery_task/', views.run_celery_task, name='run_celery-task-task'),
    path('check_celery_task/<str:task_id>/', views.check_celery_task, name='check-celery-task'),
]
