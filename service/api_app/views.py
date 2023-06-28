from datetime import datetime

# import openpyxl
# from excel_response import ExcelResponse
from rest_framework import status, pagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_app.models import PreOrder
from api_app.serializers import PreOrderSerializer


class PreOrderPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PreOrderAPIView(ModelViewSet):
    queryset = PreOrder.objects.all()
    serializer_class = PreOrderSerializer
    pagination_class = PreOrderPagination

    def get_queryset(self) -> queryset:
        queryset = super().get_queryset()

        bought = self.request.query_params.get('bought')
        canceled = self.request.query_params.get('canceled')
        product = self.request.query_params.get('product')

        if bought is not None:
            bought = bought.lower() == 'true'
            queryset = queryset.filter(bought=bought)
        if canceled is not None:
            canceled = canceled.lower() == 'true'
            queryset = queryset.filter(canceled=canceled)
        if product is not None:
            queryset = queryset.filter(product=product)

        queryset = queryset.order_by('date_ordered')

        return queryset

    def update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        bought = request.data.get('bought', instance.bought)
        canceled = request.data.get('canceled', instance.canceled)

        if bought is True and instance.bought is False:
            instance.bought = True
            instance.day_of_bought = datetime.now()

        if canceled is True and instance.canceled is False:
            instance.canceled = True
            instance.day_of_canceled = datetime.now()

        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
