#from pixabay import Image, Video

#API_KEY = '16114175-7f138daad5a59db53fac2b925'

# image operations
#image = Image(API_KEY)

# default image search
#image.search()

# custom image search
#ims = image.search(q='flower',
            #  lang='es',
            #  image_type='photo',
            #  orientation='horizontal',
            #  category='flower',
            #  safesearch='true',
            #  order='popular',
            #  page=1,
            #  per_page=18)

#print(ims.get('hits'))
# for i in range(18):
#     print(i)
#     print(ims.get('hits')[i])
#     print("\n")
    #print(ims.get('hits')[1])
    #print(ims.get('hits')[2])
    #print(ims.get('hits')[3])
#print(ims)

# def scraping():
#     API_KEY = '16114175-7f138daad5a59db53fac2b925'
#     image = Image(API_KEY)
#     testData = "hello"
#     return testData

import requests
from ast import literal_eval

def scrap():
    url = "https://pixabay.com/api/?key=16114175-7f138daad5a59db53fac2b925&q=yellow+flower&image_type=photo"
    req = requests.get(url).content
    #allData = req['total']
    req = req.decode('utf-8')
    allData = literal_eval(req)

    print("previewURL: ", allData['hits'][0]['previewURL'])
    #print("webformatURL: ", allData['hits'][0]['webformatURL'])
    #print("largeImageURL: ", allData['hits'][0]['largeImageURL'])


    #
        # for key, value in allData['hits'][i]:
        #     print(key, value)
    #print(allData['hits'].shape)

    return allData['hits']

scrap()