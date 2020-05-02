from django.shortcuts import render
#from . import crawling
#from pixabay import Image, Video
from .crawling import scrap
#
from .models import Image

# Create your views here.
def create(request):
    image.photo = request.FILES['photo']
    
def home(request):
    images = Image.objects
    return render(request, 'home.html', {'images':images})

def recommendation(request):
    #testData = "test"
    testData = scrap()
    info = {}
    for number in range(len(testData)):
        temp = {}
        if(testData[number]['webformatWidth'] == 640 and testData[number]['webformatHeight'] == 426):
            temp['url'] = testData[number]['webformatURL']
            if(len(testData[number]['user']) > 10):
                temp['user'] = testData[number]['user'][0:10] + ".."
            else:
                temp['user'] = testData[number]['user']
            month = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
            d = testData[number]['previewURL'].split('/')
            temp['date'] = month[int(d[5])-1] + " " + str(int(d[6])) + ", " + d[4]
            temp['likes'] = testData[number]['likes']
            temp['comments'] = testData[number]['comments']
            info[len(info)] = temp
            if(len(info) == 6):
                break
    return render(request, 'recommendation.html', {'info':info})
    #return render(request, 'recommendation.html', {'testData':testData})

def result(request):
    return render(request, 'result.html')