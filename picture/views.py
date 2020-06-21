from django.shortcuts import render, get_object_or_404, redirect
#from . import crawling
#from pixabay import Image, Video
from django.http import JsonResponse, HttpResponse
from .crawling import scrap
#
from .color_transfer import get_mean_and_std, color_transfer
#from .models import Image
#from .forms import ImageForm

from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from PIL import ImageFile, Image
from io import BytesIO
import base64
import requests


@csrf_exempt
def detection_crawler(request):
    if request.method == 'POST':
        
        inputlist = []
        for f in request.FILES.values():
            p = ImageFile.Parser()
            while 1:
                s = f.read()
                if not s:
                    break
                p.feed(s)
            im = p.close()
            
            inputlist.append(im)
        if inputlist:
            from object_detection_capstone import capstone_detection 
            res = capstone_detection.detect_func(inputlist)
        elif not inputlist:
            res = []
        info = scrap(res)

        # ranges = range(0, 30)
        context = {'info':info}
        return JsonResponse(context)




def home(request):
    src_list = []
    if request.method == 'POST':
        #form = Image()
        for f in request.FILES.values():
            
            p = ImageFile.Parser()
            while 1:
                s = f.read()
                if not s:
                    break
                p.feed(s)
            im = p.close()
            
            src_list.append(im)
        

        if request.POST['reco']:
            recom = request.POST['reco']
            src_list.append(Image.open(BytesIO(requests.get(recom).content)))

        target = src_list[-1]
        del src_list[-1]

        r = color_transfer(src_list, target)

        re = {}
        for i in range(len(r)):
            x = r[i+1]
            output = BytesIO()
            x.save(output, "PNG")
            contents = base64.b64encode(output.getvalue()).decode('ascii')
            output.close() 
            re[i+1] = contents
        return render(request,'home.html',{'re': re})

    return render(request, 'home.html')



def search_crawler(request):
    search = request.GET['sh_input']
    query = search
    query = query.strip()
    query = query.split(",")
    searched = scrap(query)

    return JsonResponse({'searched':searched})