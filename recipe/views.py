import hashlib
import json
import random
from datetime import datetime

from django.http import HttpResponse

from util.reverse_search_sql import search_by_ingredients, search_by_name, sort_result
from .models import Recipe
from .forms import RecipeForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

Auth = 'dc05414dd18879df268456db4e29a5f2d045dea2176c19888cc91769a52436f9'
Day1 = datetime(day=21, month=1, year=2022)


@csrf_exempt
def get_recipe_by_exact_match(request):
    response = {"success": 0, "message": ""}
    if request.method != 'POST':
        response["message"] = "Method not allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)

    request_data = json.loads(request.body)
    try:
        ingredients = request_data['ingredients']
        exclude = request_data['ban']
    except Exception as e:
        response["message"] = str(e)
        return HttpResponse(json.dumps(response), content_type="application/json", status=500)

    result = []
    # Load all recipes from database
    all_recipes = Recipe.objects.values('id', "ingredients")

    # Find the recipes that match the ingredients
    for i in all_recipes:
        valid_recipe = True
        for ing in i['ingredients']:
            valid_ing = False
            for j in ingredients:
                if j.lower() in ing.lower():
                    valid_ing = True
                    break
            if not valid_ing:
                valid_recipe = False
                break
        if valid_recipe and i['id'] not in exclude:
            result.append(i['id'])

    r = []
    for i in result:
        r.append(Recipe.objects.get(id=i))
    recipes = sort_result(r, request_data['sort'] if 'sort' in request_data else 'name')

    if result:
        response['result'] = recipes
        response['success'] = 1
        response['exact'] = 1
        return HttpResponse(json.dumps(response, cls=Recipe.RecipeEncoder, indent=4), content_type="application/json",
                            status=200)
    else:
        return get_recipe_by_ingredients(request)


@csrf_exempt
def get_recipe_by_ingredients(request):
    response = {"success": 0, "message": ""}
    if request.method != 'POST':
        response["message"] = "Method not allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)

    request_data = json.loads(request.body)
    ingredients = request_data['ingredients']
    exclude = request_data['ban']

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
        recipes = sort_result(result, request_data['sort'] if 'sort' in request_data else 'name')
    except Exception as e:
        response["message"] = str(e)
        return HttpResponse(json.dumps(response), content_type="application/json", status=500)
    response['result'] = recipes
    response['success'] = 1
    response['exact'] = 0
    return HttpResponse(json.dumps(response, cls=Recipe.RecipeEncoder, indent=4), content_type="application/json")


@csrf_exempt
def get_recipe_by_id(request):
    response = {"success": 0, "message": ""}
    if request.method != 'GET':
        response["message"] = "Method not allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)
    try:
        recipe_info = Recipe.objects.get(id=request.GET['id'])
    except Exception as e:
        response["message"] = str(e)
        return HttpResponse(json.dumps(response), content_type="application/json", status=500)
    return HttpResponse(json.dumps(recipe_info, cls=Recipe.RecipeEncoder, indent=4), content_type="application/json")


@csrf_exempt
def get_recipe_by_name(request):
    response = {"success": 0, "message": ""}
    if request.method != 'POST':
        response["message"] = "Method not allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)

    request_data = json.loads(request.body)
    name = request_data['name']
    result = []
    sql = search_by_name(name)

    try:
        for r in Recipe.objects.raw(sql):
            result.append(r)
    except Exception as e:
        response["message"] = str(e)
        return HttpResponse(json.dumps(response), content_type="application/json", status=500)
    return HttpResponse(json.dumps(result, cls=Recipe.RecipeEncoder, indent=4), content_type="application/json")


@csrf_exempt
def get_recipe_random(request):
    while 1 == 1:
        try:
            return HttpResponse(
                json.dumps(Recipe.objects.get(id=random.randint(1, Recipe.objects.count())), cls=Recipe.RecipeEncoder,
                           indent=4), content_type="application/json")
        except Exception as e:
            continue


@csrf_exempt
def get_recipe_of_today(request):
    random.seed((datetime.now() - Day1).days)
    while 1 == 1:
        try:
            return HttpResponse(
                json.dumps(Recipe.objects.get(id=random.randint(1, Recipe.objects.count())), cls=Recipe.RecipeEncoder,
                           indent=4), content_type="application/json")
        except Exception as e:
            continue


@csrf_exempt
def add_recipe(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": 0, "message": "Method not allowed"}), 405)
    data = json.loads(request.body)
    recipes = data['recipes']
    form = RecipeForm()
    for recipe in recipes:
        r = form.save(commit=False)
        r.id = recipe[0]
        r.cook_time = recipe[1]
        r.prep_time = recipe[2]
        r.description = recipe[3]
        r.ingredients = recipe[4]
        r.instructions = recipe[5]
        r.photo_url = recipe[6]
        r.rating = recipe[7]
        r.title = recipe[8]
        r.recipe_url = recipe[9]
        try:
            r.save()
        except Exception as e:
            continue
    return HttpResponse(json.dumps({"success": 1}), 200)


# This is function should only be used by Junix
@csrf_exempt
def delete_all_recipe(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({"success": 0, "message": "Method not allowed"}), 405)
    data = json.loads(request.body)
    if hashlib.sha256(data['password'].encode()).hexdigest() == Auth:
        Recipe.objects.all().delete()
        return HttpResponse(json.dumps({"success": 1}), 200)
    else:
        return HttpResponse(json.dumps({"success": 0, "message": "Wrong password"}), 405)
