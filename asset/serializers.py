from rest_framework import serializers
from .models import Asset
import requests

def generate_qr_code_url(obj):
    print(obj)
    return "url"


class AssetSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()
    name_key = serializers.SerializerMethodField()
    class Meta:
        model = Asset
        fields = '__all__'

    def get_name_key(self, obj):
        # Static prefix
        prefix = "NVRI"

        # Helper function to get the initial of each word
        def get_initials(text):
            return ''.join([word[0].upper() for word in text.split() if word])

        # Get initials for Department and Location
        department_initials = get_initials(obj.Department) if obj.Department else ''
        location_initials = get_initials(obj.Location) if obj.Location else ''

        # Forming the code
        key_name = f"{prefix}/{department_initials}/{location_initials}/{obj.id:04d}"  # Formats ID with leading zeros
        return key_name
    def get_qr_code_url(self, obj):
        # return generate_qr_code(obj)
        return f"https://res.cloudinary.com/edward-campbell/image/upload/v1713388402/asset-management1/{obj.id}.png"


def generate_qr_code(obj):
    asset_id = obj.id
    url = "https://qrcode-monkey.p.rapidapi.com/qr/custom"

    payload = {
        "data": f"https://app.assetmanagement.com.ng/qr-code/{asset_id}",
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
        with open(f"{asset_id}.png", 'wb') as f:
            f.write(response.content)
        print("Image saved as output.png.")
    else:
        print("Not an image response. Here's the returned data:", response.text)

    return "saved"