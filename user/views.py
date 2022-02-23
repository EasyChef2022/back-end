import json
from django.http import HttpResponse
from .models import User
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def create_user(request):
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
        user.password = request_data['password']
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
