from django.http import JsonResponse
from django.conf import settings
from rest_framework import status

def api_key_required(view_func):
    def wrapper(request, *args, **kwargs):
        api_key = request.GET.get("api_key")
        if api_key != settings.API_KEY:
            return JsonResponse({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(request, *args, **kwargs)
    return wrapper
