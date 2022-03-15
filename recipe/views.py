import json

from django.http import HttpResponse
from .models import Recipe
from .forms import RecipeForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_recipe(request):
    response = {"success": 0, "message": ""}
    if request.method != 'GET':
        response["message"] = "Method not allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)
    result = []
    sql = f"select  * from (select *, unnest(ingredients) as ing from recipe) as ing like ''"
    print(sql)
    try:
        for r in  Recipe.objects.raw(sql):
            result.append(r)
    except Exception as e:
        response["message"] = str(e)
        return HttpResponse(json.dumps(response), content_type="application/json", status=500)
    # print(type(r))

    # for r in Recipe.objects.raw(f"select * from recipe where array_to_string(tags, ',', '*') like '%Dairy Free%' limit 10"):
    #     print(10)
    #     result.append(r)
    return HttpResponse(json.dumps(result, cls=Recipe.RecipeEncoder, indent=4), content_type="application/json")
    # return HttpResponse(json.dumps(recipe_info, indent=4, cls=RecipeEncoder), content_type="application/json")
