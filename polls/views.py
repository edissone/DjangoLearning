from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, this my first app on Django/Python")