from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datauri import DataURI
from base64 import b64encode
import os
import datetime


from . import compress as cp
from . import restore as rs


# Create your views here.

def restore(req):
    return render(req, 'index/restore.html')

@csrf_exempt
def uploadRestore(request):

    img = request.POST.get('img')
    mask = request.POST.get('mask')
    fname = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    user_folder = 'media'
    src = f'{user_folder}/input/{fname}.png'
    maskdir=f'{user_folder}/input/m-{fname}.png'
    dest = f'{user_folder}/output/o-{fname}.png'

    uri=DataURI(img)

    fd=open(src,'wb')
    fd.write(uri.data)
    fd.close()


    uri=DataURI(mask)
    fd=open(maskdir,'wb')
    fd.write(uri.data)
    fd.close()


    cp.saveCompressed(src)
    rs.restore(src,maskdir,dest)   
    output_uri =b64encode(DataURI.from_file(dest).data)

    os.remove(src)
    os.remove(maskdir)
    os.remove(dest)


    return HttpResponse(output_uri)



    











    

