from django.http import JsonResponse
import requests
 
def paymentService(request):
    # TODO
    return JsonResponse({'status': 'success'})

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






