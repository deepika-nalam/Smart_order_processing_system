from django.core.cache import cache
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        cache_key = "products:list"
        cached_data = cache.get(cache_key)

        if cached_data:
            print(" PRODUCTS LIST FROM CACHE")
            return Response(cached_data)

        print(" PRODUCTS LIST FROM DATABASE")
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)
        print("CACHE SET")
        return response

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs["pk"]
        cache_key = f"products:detail:{product_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            print(" PRODUCT DETAIL FROM CACHE")
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)
        return response
