from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def recommendation(request):
    return render(request, 'recommendation.html')

def result(request):
    return render(request, 'result.html')