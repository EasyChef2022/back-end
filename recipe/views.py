import json

from django.http import HttpResponse

from util.reverse_search_sql import search_by_ingredients
from .models import Recipe
from .forms import RecipeForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_recipe_by_ingredients(request):
    response = {"success": 0, "message": ""}
    if request.method != 'POST':
        response["message"] = "Method not allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)

    request_data = json.loads(request.body)
    ingredients = request_data['ingredients']
    exclude = request_data['exclude']

    if 'limit' in request_data:
        limit = request_data['limit']
    else:
        limit = 10
    if 'offset' in request_data:
        offset = request_data['offset']
    else:
        offset = 0

    result = []
    sql = search_by_ingredients(ingredients, exclude, offset, limit)

    try:
        for r in Recipe.objects.raw(sql):
            result.append(r)
    except Exception as e:
        response["message"] = str(e)
        return HttpResponse(json.dumps(response), content_type="application/json", status=500)

    return HttpResponse(json.dumps(result, cls=Recipe.RecipeEncoder, indent=4), content_type="application/json")


@csrf_exempt
def get_recipe_by_name(request):
    response = {"success": 0, "message": ""}
    if request.method != 'POST':
        response["message"] = "Method not allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)
