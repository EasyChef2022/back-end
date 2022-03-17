import json
import time
from django.http import HttpResponse
from rest_framework import generics
import middlewares.middlewares
import util.jwt_auth
from EasyChef.serializer import UserSerializer
from .models import User
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from util.salt_password import salt_password, compare_password

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
        # match with the username
        try:
            user_info = User.objects.get(username=request_data['username'])
        except Exception as e:
            response['message'] = "User not found"
            return HttpResponse(json.dumps(response), content_type="application/json", status=400)

        try:
            if compare_password(request_data['password'], user_info.password):
                if len(request_data['new_password']) < 6 or ' ' in request_data['new_password']:
                    # check the new_password valid
                    response['message'] = "Invalid new_password"
                    return HttpResponse(json.dumps(response), content_type="application/json", status=400)
                if request_data['new_password'] == request_data['password']:
                    # check the new_password same or not with old password
                    response['message'] = "new_password same as old_password"
                    return HttpResponse(json.dumps(response), content_type="application/json", status=400)
                # all condition are good, change password below
                user_info.password = salt_password(request_data['new_password'])
                response['success'] = "1"
                response['message'] = "Password changed successful"
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
