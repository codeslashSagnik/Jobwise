from django.http import JsonResponse

def handle500error(request):
    message=('Internal Server Error')
    response=JsonResponse(data={'error':message})
    response.status_code=500
    return response

def handle404error(request,exception):
    message=('Route Not Found')
    response=JsonResponse(data={'error':message})
    response.status_code=404
    return response