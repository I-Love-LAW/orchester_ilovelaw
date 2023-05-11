from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from .models import Pembayaran

class PembayaranSerializer(ModelSerializer):
    class Meta:
        model = Pembayaran
        fields = ['username']
        extra_kwargs = {
            "username": 
                {"error_messages": 
                    {"required": "Missing requirement.",
                    }
                },
        }

    def create(self, validated_data):
        # set default valued attributes
        validated_data["date"] = timezone.now()

        # create instance (Pembayaran)
        pesanan_instance = Pembayaran.objects.create(**validated_data)
        return pesanan_instance

class DetailPembayaranSerializer(ModelSerializer):
        class Meta:
            model = Pembayaran
            fields = "__all__"