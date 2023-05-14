from django.http import JsonResponse
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *

#TODO: 
# Explore Consul for service registry (low priority, refactor after orchestration works)

 
@api_view(['POST'])
def payment_service(request):
    serializer = PembayaranSerializer(data=request.data)
    if serializer.is_valid():

        pembayaran = Pembayaran.objects.filter(username=serializer.validated_data['username']).first()
        if pembayaran is not None:
            return Response({"message": "You already make payment"}, status=status.HTTP_400_BAD_REQUEST)
        
        pembayaran = serializer.save()
        detail_serializer = DetailPembayaranSerializer(instance=pembayaran)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def convert_service(request, username):
    fileInput = request.FILES.get('fileInput')
    imageFormat = request.data.get('imageFormat')
    singleOrMultiple = request.data.get('singleOrMultiple')
    colorType = request.data.get('colorType')
    dpi = request.data.get('dpi')

    convert_url = 'http://localhost:8080/api/convert/pdf-to-img'
    files = {'fileInput': fileInput}
    data = {'imageFormat': imageFormat,
            'singleOrMultiple': singleOrMultiple,
            'colorType': colorType,
            'dpi': dpi,
            'username': username,}
    convert_response = requests.post(convert_url, files=files, data=data)

    if convert_response.status_code != 200:
        return JsonResponse({'error': 'Conversion process failed!'})
    
    return Response({'data': convert_response.content})

@api_view(['POST'])
def service_orchester(request):
    username = request.data.get('username')

    paymentResponse = requests.post('http://127.0.0.1:8000/api/payment/create-payment',
        data = {'username': username})

    if paymentResponse.status_code != 200:
        return JsonResponse({'error': 'Payment failed'})
    elif paymentResponse.status_code == 400:
        return JsonResponse({'message': 'You are already a Premium user of ilovelaw'})
    
    convertResponse = convert_service(request._request, username)

    return convertResponse






