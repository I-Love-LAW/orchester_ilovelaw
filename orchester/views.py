from django.http import JsonResponse
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view

#TODO: 
# Explore Consul for service registry (low priority, refactor after orchestration works)


def payment_service(request):
    username = request.data.get('username')
    header = {'Authorization':request.headers['Authorization']}
    return requests.post('http://localhost:8000/api/payment/create-payment',
                         data = {'username': username}, headers=header)


def upgrade_service(request):
    username = request.data.get('username')
    header = {'Authorization':request.headers['Authorization']}
    return requests.put('http://localhost:8082/api/user/upgrade-membership?username=' + username,
                        headers=header)


def convert_service(request):
    # fileInput = request.FILES.get('fileInput')
    fileInput = request.FILES.getlist('fileInput[]')
    imageFormat = request.data.get('imageFormat')
    singleOrMultiple = request.data.get('singleOrMultiple')
    colorType = request.data.get('colorType')
    dpi = request.data.get('dpi')
    username = request.data.get('username')

    convert_url = 'http://localhost:8080/api/convert/pdf-to-img'
    header = {'Authorization':request.headers['Authorization']}

    for file in fileInput:
        files = {'fileInput': file}
        data = {
            'imageFormat': imageFormat,
            'singleOrMultiple': singleOrMultiple,
            'colorType': colorType,
            'dpi': dpi,
            'username': username
        }
        print(file)

        requests.post(convert_url, files=files, data=data, headers=header)

    return JsonResponse({'data': 'Success'}, status=200)


@api_view(['POST'])
def service_orchester_convert(request):
    paymentResponse = payment_service(request)

    if paymentResponse.status_code == 400:
        return JsonResponse({'message': 'You have made a payment'}, status=400)
    elif paymentResponse.status_code != 200:
        return JsonResponse({'error': 'Payment failed'}, status=paymentResponse.status_code)

    upgradeResponse = upgrade_service(request)

    if upgradeResponse.status_code == 400:
        return JsonResponse({'message': 'You are already a Premium user of ilovelaw'}, status=400)
    elif upgradeResponse.status_code != 200:
        return JsonResponse({'error': 'Upgrade failed'}, status=paymentResponse.status_code)
    
    convertResponse = convert_service(request)

    return JsonResponse({'data': 'Success'}, status=200)


@api_view(['POST'])
def service_orchester(request):
    paymentResponse = payment_service(request._request)

    if paymentResponse.status_code == 400:
        return JsonResponse({'message': 'You have made a payment'})
    elif paymentResponse.status_code != 200:
        return JsonResponse({'error': 'Payment failed'})

    upgradeResponse = upgrade_service(request._request)

    if upgradeResponse.status_code == 400:
        return JsonResponse({'message': 'You are already a Premium user of ilovelaw'})
    elif upgradeResponse.status_code != 200:
        return JsonResponse({'error': 'Upgrade failed'})

    return JsonResponse({'message': 'Membership upgraded successfully to Premium!'})
