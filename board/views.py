import os
import traceback
from datetime import datetime
from django.db.models import Max, Prefetch
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

import config.settings

from .models import Product, ProductList, Unit, Location
from .serializer import ProductPureSerializer, ProductListSerializer, ProductSerialzer, ProductAddSerializer
from .serializer import LocationSerializer, UnitSerializer, ProductUpdateSerializer

class ProductAddView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = ProductList.objects.all()
    serializer_class = ProductAddSerializer

    def create(self, request, *args, **kwargs):
        try:
            request.data['location'] = Location.objects.get(
                name=request.data['location']
            ).id
        except:
            pass

        return super().create(request, *args, **kwargs)

class ProductListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = ProductList.objects.all()
    serializer_class = ProductSerialzer

    def list(self, request, *args, **kwargs):
        pre_qs = ProductList.objects.select_related('product_name', 'location').filter(location=kwargs['location'])
        # queryset = Reagent.objects.prefetch_related(Prefetch('reagent_list', queryset=pre_qs)).filter(
        #     reagent_list__location=kwargs['location']).exclude(reagent_list__isnull=True).order_by('name')
        queryset = Product.objects.prefetch_related(Prefetch('product_list', queryset=pre_qs)).exclude(
            product_list__isnull=True).order_by('name')
        serializer = self.get_serializer(queryset, many=True)

        # 새로운 배열을 생성해서 담아줘야하는 이유는 serializer.data에는
        # 해당 장소에 없는 시약이 있을때도 검색되는 현상 때문에 그런것 제거
        result = []
        now = datetime.now()

        for i in serializer.data:
            new_list = []
            total = 0
            waste = 0
            for j in i['product_list']:
                total += j['amount']

                if j['date']:
                    j['date'] = j['date'][:10]
                    diff = datetime.strptime(j['date'], '%Y-%m-%d')
                    if (diff - now).days < 0:
                        waste += j['amount']
                new_list.append(j)

            if new_list:
                i['unit'] = Unit.objects.get(id=i['unit']).name
                i['total'] = total
                i['waste'] = waste
                result.append(i)
        return Response(result)

class ProductUpdateView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = ProductList.objects.all()
    serializer_class = ProductUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = ProductListSerializer(instance)
            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        temp = []
        for i in request.data:
            if not request.data[i]:
                temp.append(i)
            elif i == 'location':
                #아랫부분과 slug를 잘 조합해서 깔끔하게 짜보자.
                request.data[i] = Location.objects.get(name=request.data[i]).id
        for i in temp:
            del request.data[i]
        return super().update(request, *args, **kwargs)

class ProductSearchView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = ProductList.objects.all()
    serializer_class = ProductSerialzer

    def list(self, request, *args, **kwargs):
        pre_qs = ProductList.objects.select_related('product_name', 'location').exclude(location=1).exclude(location=2)
        # queryset = Reagent.objects.prefetch_related(Prefetch('reagent_list', queryset=pre_qs)).filter(
        #     reagent_list__location=kwargs['location']).exclude(reagent_list__isnull=True).order_by('name')
        queryset = Product.objects.prefetch_related(Prefetch('product_list', queryset=pre_qs)).filter(
            name__icontains=kwargs['name']).exclude(product_list__isnull=True).order_by('name')
        serializer = self.get_serializer(queryset, many=True)

        # 새로운 배열을 생성해서 담아줘야하는 이유는 serializer.data에는
        # 해당 장소에 없는 시약이 있을때도 검색되는 현상 때문에 그런것 제거
        result = []
        now = datetime.now()

        for i in serializer.data:
            new_list = []
            total = 0
            waste = 0
            for j in i['product_list']:
                total += j['amount']

                if j['date']:
                    j['date'] = j['date'][:10]
                    diff = datetime.strptime(j['date'], '%Y-%m-%d')
                    if (diff - now).days < 0:
                        waste += j['amount']
                new_list.append(j)

            if new_list:
                i['unit'] = Unit.objects.get(id=i['unit']).name
                i['total'] = total
                i['waste'] = waste
                result.append(i)
        return Response(result)

class RevenueView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = ProductList.objects.all()
    serializer_class = ProductSerialzer

    def post(self, request, *args, **kwargs):
        pre_qs = ProductList.objects.select_related('product_name', 'location').filter(
            sold_date__range=[timezone.make_aware(datetime.strptime(request.data['start'], '%Y-%m-%d')),
                         timezone.make_aware(datetime.strptime(request.data['end'], '%Y-%m-%d'))]).filter(location=2)

        queryset = Product.objects.prefetch_related(Prefetch('product_list', queryset=pre_qs)).exclude(product_list__isnull=True).order_by('name')
        serializer = self.get_serializer(queryset, many=True)

        # 새로운 배열을 생성해서 담아줘야하는 이유는 serializer.data에는
        # 해당 장소에 없는 시약이 있을때도 검색되는 현상 때문에 그런것 제거
        result = []
        now = datetime.now()

        for i in serializer.data:
            new_list = []
            total = 0
            for j in i['product_list']:
                total += j['amount']
                new_list.append(j)

            if new_list:
                i['unit'] = Unit.objects.get(id=i['unit']).name
                i['total'] = total
                result.append(i)
        return Response(result)

from board.file_handler import excel_file_maker
from openpyxl.writer.excel import save_virtual_workbook
class ExcelMakerView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = ProductList.objects.all()
    serializer_class = ProductSerialzer

    def retrieve(self, request, *args, **kwargs):
        pre_qs = ProductList.objects.select_related('product_name', 'location').filter(
            location=kwargs['location']
        )
        queryset = Product.objects.prefetch_related(Prefetch('product_list', queryset=pre_qs)).exclude(product_list__isnull=True).order_by('name')
        serializer = self.get_serializer(queryset, many=True)

        result = []
        for i in serializer.data:
            if i['product_list']:
                result.append(i)

        get_name = Location.objects.get(id=kwargs['location']).name
        file = excel_file_maker(result, get_name)

        response = HttpResponse(save_virtual_workbook(file), content_type='ms-excel')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        return response

class ProductView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductPureSerializer

    def create(self, request, *args, **kwargs):

        try:
            request.data['unit'] = Unit.objects.get(
                name=request.data['unit']
            ).id
        except:
            pass

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        data = Product.objects.aggregate(id=Max('id'))
        if data['id']:
            integer = data['id'] + 1
        else:
            integer = 1
        serializer.save(id=integer)

class LocationView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class UnitView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer