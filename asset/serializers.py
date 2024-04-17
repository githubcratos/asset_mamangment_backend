from rest_framework import serializers
from .models import Asset


def generate_qr_code_url(obj):
    print(obj)
    return "url"


class AssetSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()
    class Meta:
        model = Asset
        fields = '__all__'

    def get_qr_code_url(self, obj):
        return generate_qr_code_url(obj)

