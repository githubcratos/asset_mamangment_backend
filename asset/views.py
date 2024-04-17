from collections import defaultdict

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Asset
from .serializers import AssetSerializer
import requests


@api_view(['GET'])
def get_asset_name(request, id):
    try:
        asset = Asset.objects.get(pk=id)
        context = {'asset': asset}
        return render(request, 'asset_detail.html', context)
    except Asset.DoesNotExist:
        context = {'error': 'Asset not found'}
        return render(request, 'asset_detail.html', context, status=404)

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['Department']
    ordering = ['Department']
#     /api/assets/?ordering=Department $$ /api/assets/?ordering=-Department

    @action(detail=False, methods=['get'], url_path='by-department')
    def assets_by_department(self, request):
        # Fetch all assets
        all_assets = self.get_queryset()

        # Group assets by department
        department_assets = defaultdict(list)
        for asset in all_assets:
            department_assets[asset.Department].append(asset)

        # Serialize the assets for each department
        serialized_data = {}
        for department, assets in department_assets.items():
            serializer = AssetSerializer(assets, many=True)
            serialized_data[department] = serializer.data

        return Response(serialized_data)

    @action(detail=False, methods=['get'])  # detail=False means this is not for a single object
    def special_message(self, request):
        # Your custom function logic here
        message = "Hello world"
        return Response({"message": message})
