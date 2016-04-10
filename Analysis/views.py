from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
import time
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
import os
from . import models
from . import netAnalysis
import os
# Create your views here.
def index(request):
    #return HttpResponse("received!")

    return render(request,'Analysis/home.html')

def analysis(request):
    #return HttpResponse('received!')
    return render(request,'Analysis/analysis.html')

def _upload(file):

     if file:
        file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'uploadDirectory')
        if not os.path.isdir(file_name):
            os.makdir(file_name)
        file_name = os.path.join(file_name,'' + time.strftime("%m_%d_%H_%M_%S_")+ file.name)
        with open(file_name,'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
        return file_name
     return None

@csrf_exempt
def upload_file(request):
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    ret = 1
    file = request.FILES.get('file_upload',None)
    UPLOAD_FILE_PATH = _upload(file)
    if UPLOAD_FILE_PATH != None:
        response.write(UPLOAD_FILE_PATH)
        return response
    else:
        return Http404("File Error!")

def resultsJson(request):
    try:
        GraphInfo = {}
        file = request.GET['file']
        net = models.Net.create(file)
        net.save()
        (GraphInfo,DegreeCountMax,Degree,DegreeCount,CluDegree,Clu) = netAnalysis.getBasicInfo(file, net)
        GraphInfo['description'] = " "
        GraphInfo['result'] = 0
        GraphInfo['Degree'] = Degree
        GraphInfo['DegreeCount'] = DegreeCount
        GraphInfo['CluDegree'] = CluDegree
        GraphInfo['Clu'] = Clu
        GraphInfo['DegreeCountMax'] = DegreeCountMax
    except Exception as e:
        GraphInfo['result'] = 1
    return JsonResponse(GraphInfo)