from rest_framework.decorators import api_view
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db.models import Q
from celery.result import AsyncResult

from src.examples.models import Product
from src.examples.tasks import celery_task
from src.examples.serializers import ProductSerializer

from utils.permissions import IsAdminOrReadOnly


@api_view(['GET'])
def search_product(request):
    """
    It is an example for finding records by few fields with full-text search using gin index.

    curl -X get "http://localhost:8000/api/examples/product_search/?q=name"
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

    curl -X GET http://localhost:8000/api/examples/run_celery_task/

    DONT FORGET SET UP PERMISSIONS IN PRODUCTION
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

    curl -X GET http://localhost:8000/api/examples/check_celery_task/<task_id>/

    DONT FORGET SET UP PERMISSIONS IN PRODUCTION
    """
    result = AsyncResult(task_id)
    empty_out = {
        "status": "pending",
        "result": None
    }

    return Response(result.result if result.ready() else empty_out)


class ProductView(viewsets.ModelViewSet):
    """
    Simple example how to create ModelViewSet with
    permissions.

    Example:
    [GET]
    >>> curl -X GET http://localhost:8000/api/examples/products/
    [POST]
    1. Getting auth token
    >>> curl -X POST http://localhost:8000/api/auth/token/login/ -H "Content-Type: application/json" \
        -d '{"email": "admin@datalizecrm.com", "password": "123"}'
    2. Adding new product with 1 category. Its should be created. Add received token to the request
    >>> curl -X POST http://localhost:8000/api/examples/products/ \
        -H "Content-Type: application/json" \
        -H "Authorization: Token token_from_previous_step" \
        -d '{"name": "New Product", "category": 1}'
    3. You should retrive JSON with new prdoct fields. Open admin panel and check this.

    P.S. If you want to create new products using category name not its ID - you will need to 
    re-write create and update methods in the ProductSerializer.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly,]
    queryset = Product.objects.all()

