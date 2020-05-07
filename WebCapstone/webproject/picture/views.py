from django.shortcuts import render, get_object_or_404, redirect
#from . import crawling
#from pixabay import Image, Video
from .crawling import scrap
#
from .models import Image
from .forms import ImageForm

# Create your views here.
# def create(request):
#     image.photo = request.FILES['photo']

# def new(request):
#         form=ImageForm()
#         return render(request,'home.html',{'form':form})

# def upload(request):
#     if request.method == 'POST':
#             form = ImageForm(request.POST, request.FILES)
#             if form.is_valid():
#                     info = form.save(commit=False)
                    
#                     info.save()
#                     return redirect('/home')

# def create(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             info = form.save(commit=False)
#             info.save()
#             return redirect('home')
#     else:
#         form = ImageForm()
#     return render(request,'home.html',{'form':form})


def home(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            info = form.save(commit=False)
            info.save()
            return redirect('home')
    else:
        form = ImageForm()



    images = Image.objects
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
    return render(request, 'home.html', {'images':images, 'info':info, 'form':form})

# def recommendation(request):
#     #testData = "test"
#     testData = scrap()
#     info = {}
#     for number in range(len(testData)):
#         temp = {}
#         if(testData[number]['webformatWidth'] == 640 and testData[number]['webformatHeight'] == 426):
#             temp['url'] = testData[number]['webformatURL']
#             if(len(testData[number]['user']) > 10):
#                 temp['user'] = testData[number]['user'][0:10] + ".."
#             else:
#                 temp['user'] = testData[number]['user']
#             month = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
#             d = testData[number]['previewURL'].split('/')
#             temp['date'] = month[int(d[5])-1] + " " + str(int(d[6])) + ", " + d[4]
#             temp['likes'] = testData[number]['likes']
#             temp['comments'] = testData[number]['comments']
#             info[len(info)] = temp
#             if(len(info) == 6):
#                 break
#     return render(request, 'recommendation.html', {'info':info})
    #return render(request, 'recommendation.html', {'testData':testData})

# def result(request):
#     return render(request, 'result.html')