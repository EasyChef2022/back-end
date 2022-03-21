import json
import time
from django.http import HttpResponse
from rest_framework import generics
import middlewares.middlewares
import util.jwt_auth
from .models import User
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from util.salt_password import salt_password, compare_password
from django.forms.models import model_to_dict


# TODO: Swagger
# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


@csrf_exempt
def user_sign_up(request):
    # Submit in JSON
    form = UserForm()
    response = {"success": "0", "message": ""}
    if request.method == 'POST':
        request_data = json.loads(request.body)
        user = form.save(commit=False)

        # Make sure the username and password is valid
        if len(request_data['username']) < 5 or ' ' in request_data['username']:
            response['message'] = "Invalid username"
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)
        if len(request_data['password']) < 6 or ' ' in request_data['password']:
            response['message'] = "Invalid password"
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)

        user.username = request_data['username']
        user.password = salt_password(request_data['password'])
        try:
            user.save()
            response['success'] = "1"
            response['message'] = "User created"
            return HttpResponse(json.dumps(response), content_type="application/json", status=200)
        except Exception as e:
            response['message'] = str(e)
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    else:
        response['message'] = "Method Not Allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)


@csrf_exempt
def user_sign_in(request):
    response = {"success": "0", "message": ""}
    if request.method == 'POST':
        request_data = json.loads(request.body)
        try:
            user_info = User.objects.get(username=request_data['username'])
        except Exception as e:
            response['message'] = "User not found"
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)

        try:
            if compare_password(request_data['password'], user_info.password):
                response['success'] = "1"
                response['message'] = "Login successful"
                try:
                    response['token'] = util.jwt_auth.generate_token(payload={"username": user_info.username,
                                                                              "timestamp": time.time()},
                                                                     secret=middlewares.middlewares.JWT_secret)
                    response['user'] = model_to_dict(user_info)
                except Exception as e:
                    response['message'] = str(e)
                    return HttpResponse(json.dumps(response), content_type="application/json", status=500)
                return HttpResponse(json.dumps(response), content_type="application/json", status=200)
            else:
                response['message'] = "Invalid password"
                return HttpResponse(json.dumps(response), content_type="application/json", status=400)
        except Exception as e:
            response['message'] = "Missing password"
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    else:
        response['message'] = "Method Not Allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)


@csrf_exempt
def user_change_password(request):
    response = {"success": "0", "message": ""}
    if request.method == 'POST':
        request_data = json.loads(request.body)
        if 'password' not in request_data:
            response['message'] = "Missing password"
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)
        user = User.objects.get(username=request_data['username'])
        new_pass = salt_password(request_data['password'])
        if len(request_data['password']) < 6 or ' ' in request_data['password']:
            response['message'] = "Invalid password"
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)
        if user.password == new_pass:
            response['message'] = "New password is same as old password"
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)
        user.password = new_pass

        try:
            user.save()
            response['success'] = "1"
            response['message'] = "Password changed"
            return HttpResponse(json.dumps(response), content_type="application/json", status=200)
        except Exception as e:
            response['message'] = str(e)
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    else:
        response['message'] = "Method Not Allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)


@csrf_exempt
def user_add_pantry(request):
    response = {"success": "0", "message": ""}
    if request.method == 'POST':
        request_data = json.loads(request.body)
        indicator = request_data['type']
        user = User.objects.get(username=request_data['username'])

        # Hardcoded for now
        if indicator == 'herbs':
            user.herbs.append(request_data['item'])
        elif indicator == "proteins":
            user.proteins.append(request_data['item'])
        elif indicator == 'vegetables':
            user.vegetables.append(request_data['item'])
        elif indicator == 'spices':
            user.spices.append(request_data['item'])
        elif indicator == 'favorite':
            user.favorite.append(request_data['item'])
        elif indicator == 'ban':
            user.ban.append(request_data['item'])
        else:
            response['message'] = "Invalid type"
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)

        try:
            user.save()
            response['success'] = "1"
            response['message'] = "Successfully added"
            return HttpResponse(json.dumps(response), content_type="application/json", status=200)
        except Exception as e:
            response['message'] = str(e)
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    else:
        response['message'] = "Method Not Allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)

@csrf_exempt
def user_remove_pantry(request):
    response = {"success": "0", "message": ""}
    if request.method == 'POST':
        request_data = json.loads(request.body)
        indicator = request_data['type']
        user = User.objects.get(username=request_data['username'])

        # Hardcoded for now
        if indicator == 'herbs':
            for item in user.herbs:
                if item == request_data['item']:
                    user.herbs.remove(item)
        elif indicator == "proteins":
            for item in user.proteins:
                if item == request_data['item']:
                    user.proteins.remove(item)
        elif indicator == 'vegetables':
            for item in user.vegetables:
                if item == request_data['item']:
                    user.vegetables.remove(item)
        elif indicator == 'spices':
            for item in user.spices:
                if item == request_data['item']:
                    user.spices.remove(item)
        elif indicator == 'favorite':
            for item in user.favorite:
                if item == request_data['item']:
                    user.favorite.remove(item)
        elif indicator == 'ban':
            for item in user.ban:
                if item == request_data['item']:
                    user.ban.remove(item)
        else:
            response['message'] = "Invalid type"
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)

        try:
            user.save()
            response['success'] = "1"
            response['message'] = "Successfully removed"
            return HttpResponse(json.dumps(response), content_type="application/json", status=200)
        except Exception as e:
            response['message'] = str(e)
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    else:
        response['message'] = "Method Not Allowed"
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)