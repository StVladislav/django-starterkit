from rest_framework.decorators import api_view
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from celery.result import AsyncResult

from src._test.models import Product
from src._test.tasks import celery_task
from src._test.serializers import ProductSerializer


@api_view(['GET'])
def search_product(request):
    """
    It is an example for finding records by few fields with full-text search using gin index.

    curl -X get "http://localhost:8000/api/test/product_search/?q=name"
    """
    search_query = request.GET.get('q', '').strip()
    n_results = 10 # Number of returned records
    threshold = 0.2 # Minima threshold for trigram simmilarity
    
    if not search_query:
        return Response(
            {"error": "Search query parameter 'q' is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    products = Product.objects.annotate(
        similarity=TrigramSimilarity('name', search_query) + 
                   TrigramSimilarity('category__name', search_query)
    ).filter(
        Q(similarity__gt=threshold) |
        Q(name__icontains=search_query) |
        Q(category__name__icontains=search_query)
    ).order_by('-similarity')[:n_results]
    
    out = ProductSerializer(products, many=True, context={'request': request}).data
    
    return Response({"result": out}, status=status.HTTP_200_OK)


@api_view(['GET'])
def run_celery_task(request):
    """
    Simple view for run a specified celery task.

    curl -X GET http://localhost:8000/api/test/run_celery_task/
    """
    task = celery_task.delay()

    return Response({
        "status": "Task started successfully",
        "task_id": task.id
    })


@api_view(['GET'])
def check_celery_task(request, task_id):
    """
    Simple view for check running celery task by its id.

    curl -X GET http://localhost:8000/api/test/check_celery_task/<task_id>/
    """
    result = AsyncResult(task_id)
    empty_out = {
        "status": "pending",
        "result": None
    }

    return Response(result.result if result.ready() else empty_out)
