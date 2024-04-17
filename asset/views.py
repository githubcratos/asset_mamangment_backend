from collections import defaultdict

from django.http import JsonResponse
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
        return JsonResponse({'Asset name': asset.AssetName, "Category": asset.Category, "Department": asset.Department})
    except Asset.DoesNotExist:
        return JsonResponse({'error': 'Asset not found'}, status=404)

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
        print(generate_qr_code())
        message = "Hello world"
        return Response({"message": message})



def generate_qr_code():
    url = "https://qrcode-monkey.p.rapidapi.com/qr/custom"

    payload = {
        "data": "https://www.qrcode-monkey.com",
        "config": {
            "body": "square",
            "eye": "frame3",
            "eyeBall": "ball10",
            "erf1": ["fv"],
            "erf2": ["fv", "fh"],
            "erf3": ["fh", "fh"],
            "brf1": ["fh"],
            "brf2": ["fv"],
            "brf3": ["fh"],
            "bodyColor": "#5C8B29",
            "bgColor": "#FFFFFF",
            "eye1Color": "#3F6B2B",
            "eye2Color": "#3F6B2B",
            "eye3Color": "#3F6B2B",
            "eyeBall1Color": "#60A541",
            "eyeBall2Color": "#60A541",
            "eyeBall3Color": "#60A541",
            "gradientColor1": "#10B28A",
            "gradientColor2": "#2682B9",
            "gradientType": "linear",
            "gradientOnEyes": True,
            "logoMode": "clean",
            "logo": "https://res.cloudinary.com/edward-campbell/image/upload/v1713354321/asset-management/jjy9zfcjgeoqcswmbrbl.png"
        },
        "size": 500,
        "download": False,
        "file": "png"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "b4ca98730dmsh5ea4dc480f6a3bbp1558c5jsn7a8367c636a8",
        "X-RapidAPI-Host": "qrcode-monkey.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.headers['Content-Type'] == 'image/png':
        with open('output.png', 'wb') as f:
            f.write(response.content)
        print("Image saved as output.png.")
    else:
        print("Not an image response. Here's the returned data:", response.text)

    return "saved"