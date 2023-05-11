from django.http import JsonResponse
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
 
def paymentService(APIView):
    def post(self, request):
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


def convertService(request):
    return JsonResponse({'status': 'success'})

def serviceOrchester(request):
    fileInput = request.FILES.get('fileInput')
    imageFormat = request.POST.get('imageFormat')
    singleOrMultiple = request.POST.get('singleOrMultiple')
    colorType = request.POST.get('colorType')
    dpi = request.POST.get('dpi')
    username = request.POST.get('username')

    paymentResponse = requests.post('/api/payment/upgrade-membership',
        data = {'username': username})

    if paymentResponse.status_code != 200:
        return JsonResponse({'error': 'Payment failed'})
    elif paymentResponse.status_code == 400:
        return JsonResponse({'message': 'You are already a Premium user of ilovelaw'})
    
    convertResponse = requests.post('api/convert/pdf-to-img', 
        data={'fileInput': fileInput,
              'imageFormat': imageFormat,
              'singleOrMultiple': singleOrMultiple,
              'colorType': colorType,
              'dpi': dpi
              })
    
    if convertResponse.status_code != 200:
        return JsonResponse({'error': 'Conversion process failed!'})
    
    return JsonResponse({'data': convertResponse.content})






