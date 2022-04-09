import json
from util import jwt_auth
import time

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

JWT_Required_Paths = ['/user/change_password', '/user/delete_user', '/user/add_pantry', '/user/remove_pantry']
JWT_secret = 'easychef'


class JWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path not in JWT_Required_Paths:
            return None
        else:
            body = json.loads(request.body)
            header = request.headers
            try:
                token = header['Authorization'].split(' ')[1]
            except:
                response = {'success': 0, 'message': 'Missing token in header or invalid token'}
                return HttpResponse(json.dumps(response), content_type="application/json", status=403)

            # Token authentication
            try:
                payload = jwt_auth.decode_token(token, JWT_secret)
            except:
                response = {'success': 0, 'message': 'Invalid token'}
                return HttpResponse(json.dumps(response), content_type="application/json", status=403)
            # Check if username are the same
            if 'username' not in payload or payload['username'] != body['username']:
                response = {'success': 0, 'message': 'Invalid token and username'}
                return HttpResponse(json.dumps(response), content_type="application/json", status=403)
            # Check if token is expired
            if 'timestamp' not in payload or int(time.time()) - int(payload['timestamp']) > 60 * 60:
                response = {'success': 0, 'message': 'Token expired'}
                return HttpResponse(json.dumps(response), content_type="application/json", status=403)
            return None
