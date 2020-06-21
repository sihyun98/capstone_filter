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
import itertools

def scrap(array):
    #array = ["sky", "flower", "tree"]
    # array = ["sky", "tree", "potted plant", "car"]
    # c = itertools.combinations(array, i)

    # url1 = "https://pixabay.com/api/?key=16114175-7f138daad5a59db53fac2b925&q=sky&image_type=photo"
    # url2 = "https://pixabay.com/api/?key=16114175-7f138daad5a59db53fac2b925&q=flower&image_type=photo"
    # url3 = "https://pixabay.com/api/?key=16114175-7f138daad5a59db53fac2b925&q=tree&image_type=photo"

    info = {}
    if array == []:
        url = "https://pixabay.com/api/?key=16114175-7f138daad5a59db53fac2b925&order=popular&image_type=photo"
        req = requests.get(url).content
        req = req.decode('utf-8')
        allData = literal_eval(req)
        testData = allData['hits']

        for number in range(len(testData)):
            temp = {}
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
            temp['pageURL'] = testData[number]['pageURL']
            info[len(info)] = temp
            if(len(info) == 30):
                break

    else:
        for i in range(len(array)):
            c = list(itertools.combinations(array, len(array)-i))
            for j in range(len(c)):
                add = c[j][0]
                for case in range(1, len(c[0])):
                    add += "+" + c[j][case]
                url = "https://pixabay.com/api/?key=16114175-7f138daad5a59db53fac2b925&q=" + add + "&image_type=photo"
                req = requests.get(url).content
                req = req.decode('utf-8')
                allData = literal_eval(req)
                testData = allData['hits']

                for number in range(len(testData)):
                    temp = {}
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
                    temp['pageURL'] = testData[number]['pageURL']
                    info[len(info)] = temp
                    if(len(info) == 30):
                        break

    return info
# scrap()