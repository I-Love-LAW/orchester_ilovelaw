from django.http import JsonResponse
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view


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
    file_input = request.FILES.getlist('fileInput[]')
    image_format = request.data.get('imageFormat')
    single_or_multiple = request.data.get('singleOrMultiple')
    color_type = request.data.get('colorType')
    dpi = request.data.get('dpi')
    username = request.data.get('username')

    convert_url = 'http://localhost:8080/api/convert/pdf-to-img'
    header = {'Authorization':request.headers['Authorization']}

    for file in file_input:
        files = {'fileInput': file}
        data = {
            'imageFormat': image_format,
            'singleOrMultiple': single_or_multiple,
            'colorType': color_type,
            'dpi': dpi,
            'username': username
        }
        print(file)

        requests.post(convert_url, files=files, data=data, headers=header)

    return JsonResponse({'data': 'Success'}, status=200)


@api_view(['POST'])
def service_orchester_convert(request):
    payment_response = payment_service(request)

    if payment_response.status_code == 400:
        return JsonResponse({'message': 'You have made a payment'}, status=400)
    elif payment_response.status_code != 200:
        return JsonResponse({'error': 'Payment failed'}, status=payment_response.status_code)

    upgrade_response = upgrade_service(request)

    if upgrade_response.status_code == 400:
        return JsonResponse({'message': 'You are already a Premium user of ilovelaw'}, status=400)
    elif upgrade_response.status_code != 200:
        return JsonResponse({'error': 'Upgrade failed'}, status=upgrade_response.status_code)
    
    convert_service(request)

    return JsonResponse({'data': 'Success'}, status=200)


@api_view(['POST'])
def service_orchester(request):
    payment_response = payment_service(request._request)

    if payment_response.status_code == 400:
        return JsonResponse({'message': 'You have made a payment'})
    elif payment_response.status_code != 200:
        return JsonResponse({'error': 'Payment failed'})

    upgrade_response = upgrade_service(request._request)

    if upgrade_response.status_code == 400:
        return JsonResponse({'message': 'You are already a Premium user of ilovelaw'})
    elif upgrade_response.status_code != 200:
        return JsonResponse({'error': 'Upgrade failed'})

    return JsonResponse({'message': 'Membership upgraded successfully to Premium!'})
