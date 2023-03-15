import aiohttp
import asyncio
import json
import openpyxl

from asgiref.sync import async_to_sync
from django.core.files import File
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from test_for_product_lab.settings import URL
from .serializers import ProductSerializer
from .schemas import ProductInput, DataFromFile


def check_results(result):
    if data := result.get('data'):
        if data.get('products'):
            if not isinstance(result, Exception):
                return result


async def get_by_url(session: aiohttp.ClientSession, url: str):
    response = await session.get(url)
    body = await response.text()
    data = json.loads(body)
    return data


async def make_requests(list_sku_numbers: list[str]):
    async with aiohttp.ClientSession() as session:
        requests = [get_by_url(session, URL + sku) for sku in list_sku_numbers]
        results = await asyncio.gather(*requests, return_exceptions=True)
        successful_result = list(filter(check_results, results))
        return successful_result


class ProductUploadView(GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ProductSerializer

    def post(self, request):
        file: File = request.FILES.get('file')
        sku: str = request.data.get('sku')
        if file and sku:
            return Response({'error': 'Choose one from file or sku'}, status=400)
        if not file and not sku:
            return Response({'error': 'One option is required'}, status=400)
        sku_num = []
        if sku:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                sku_num = [serializer.validated_data.get('sku')]
        if file:
            serializer = self.serializer_class(data=request.FILES)
            if serializer.is_valid(raise_exception=True):
                ds = openpyxl.load_workbook(file)
                sheet = ds.active
                sku_num = []
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    product = DataFromFile(sku=row[0]).sku
                    sku_num.append(product)
        result = async_to_sync(make_requests)(sku_num)
        if not result:
            return Response({'error': 'Invalid data or server API is down'}, status=404)
        # Получение Pydantic объекта/ов
        return_data = list(map(lambda x: (ProductInput.parse_obj(x)).products().dict(), result))
        if sku:
            return_data = return_data[0]
        return Response(return_data)

    def get_queryset(self):
        return None


def index(request):
    return render(request, 'index.html')
