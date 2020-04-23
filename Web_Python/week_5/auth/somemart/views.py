import json
import jsonschema

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.forms import ValidationError
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Item, Review
from django import forms


ITEM_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 64,
        },
        'description': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024,
        },
        'price':{
            'type': 'integer',
            'minimum': 1,
            'maximum': 1000000,
        },
    },
    'required': ['title', 'description', 'price'],
}

REVIEW_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'text': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024,
        },
        'grade':{
            'type': 'integer',
            'minimum': 1,
            'maximum': 10,
        },
    },
    'required': ['text', 'grade'],
}


def basicauth(view_func):
    """Декоратор реализующий HTTP Basic AUTH."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    token = base64.b64decode(auth[1].encode('ascii'))
                    username, password = token.decode('utf-8').split(':')
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        request.user = user
                        return view_func(request, *args, **kwargs)

        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = 'Basic realm="Somemart staff API"'
        return response
    return _wrapped_view

def staff_required(view_func):
    """Декоратор проверяющший наличие флага is_staff у пользователя."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        response = HttpResponse(status=403)
        return response
    return _wrapped_view

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(basicauth, name='dispatch')
@method_decorator(staff_required, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        
        try:
            json_data = json.loads(request.body)
            jsonschema.validate(json_data, ITEM_SCHEMA)
            Item.objects.create(title=json_data['title'], description=json_data['description'], price=json_data['price'])
            item_id = Item.objects.get(title=json_data['title']).id
            return JsonResponse(data={'id':item_id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors':'Invalid JSON'}, status=400)
        except jsonschema.exceptions.ValidationError as exc:
            return JsonResponse({'error': exc.message}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return JsonResponse(status=404, data={})
        
        try:
            json_data = json.loads(request.body)
            jsonschema.validate(json_data, REVIEW_SCHEMA)
            json_data['item'] = item
            Review.objects.create(text=json_data['text'], grade=json_data['grade'], item=json_data['item'])
            review_id = Review.objects.get(text=json_data['text']).id
            return JsonResponse(data={'id': review_id}, status = 201)
        except json.JSONDecodeError:
            return JsonResponse({'errors':'Invalid JSON'}, status=400)
        except jsonschema.exceptions.ValidationError as exc:
            return JsonResponse({'error': exc.message}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        
        try:
            item = Item.objects.get(pk=item_id)
            if item:
                item_dict = model_to_dict(item)
                reviews = item.review_set.all().order_by('-id')[:5]
                reviews = [model_to_dict(review) for review in reviews]
                for review in reviews:
                    review.pop('item', None)
                item_dict['reviews'] = reviews
            return JsonResponse(data=item_dict, status=200)
        except Item.DoesNotExist:
            return JsonResponse(status=404, data={})
        except:
            return JsonResponse(status=400, data={})
