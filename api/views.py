import json
from django.core.serializers import serialize, deserialize
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from webapp.models import Product


def product_list_view(request, *args, **kwargs):
    if request.method == 'GET':
        products = Product.objects.all()              # Достаем все данные из модели
        products_data = serialize('json', products)   # сериализуем в формате json
        response = HttpResponse(products_data)        # отправка данных с помощью http запроса
        response['Content-Type'] = 'application/json'
        return response


def product_list_view_v2(request,*args, **kwargs):
    if request.method == 'GET':
        products = Product.objects.values('pk', 'name', 'category', 'photo', 'in_order', 'price')  # вывод список данных
        return JsonResponse(list(products), safe=False)  # сокращенный вариант через JsonResponse

        # products_data = json.dumps(list(products))     # Другой вариант отправки сериализованных данных
        # response = HttpResponse(products_data)
        # response['Content-Type'] = 'application/json'
        # return response


@csrf_exempt
def product_create_view(request, *args, **kwargs):
    if request.method == 'POST':
        if request.body:
            product_data = json.loads(request.body)
            product = Product.objects.create(**product_data)
            return JsonResponse({'id': product.pk})
        else:
            response = JsonResponse({'error': 'No data provided!'})
            response.status_code = 400
            return response


