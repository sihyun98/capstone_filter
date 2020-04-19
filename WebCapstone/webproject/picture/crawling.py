from pixabay import Image, Video

API_KEY = '16114175-7f138daad5a59db53fac2b925'

# image operations
image = Image(API_KEY)

# default image search
image.search()

# custom image search
ims = image.search(q='flower',
             lang='es',
             image_type='photo',
             orientation='horizontal',
             category='flower',
             safesearch='true',
             order='latest',
             page=1,
             per_page=3)

print(ims)