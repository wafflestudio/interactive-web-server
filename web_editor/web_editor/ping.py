from django.http import JsonResponse

def ping(request, *args, **kwargs):
    return JsonResponse({"success" : True})