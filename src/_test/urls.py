from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src._test import views


router = DefaultRouter()
router.register("products", views.ProductView, basename="product")

urlpatterns = [
    path('product_search/', views.search_product, name='product-search'),
    path('run_celery_task/', views.run_celery_task, name='run_celery-task-task'),
    path('check_celery_task/<str:task_id>/', views.check_celery_task, name='check-celery-task'),
]
urlpatterns += router.urls
