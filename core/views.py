from django.shortcuts import render
from .models import Subject
from django.http import JsonResponse

# Create your views here.

def detail(request):
    return JsonResponse({"message":"view is working"})

def subjects_list(request):
    if request.method == 'GET':
        subject_qs = Subject.objects.all().values("id","name","description")
        subjects = list(subject_qs)
        return JsonResponse(subjects, safe=False)
    return JsonResponse({"error":"Method not allowed"})

def subject(request, numri):
    if request.method == 'GET':
        subject = Subject.objects.first(id=numri)
        subject_dict ={
            "id": subject.id,
            "name": subject.name,
            "description": subject.description
        }
        return JsonResponse(subject, safe=False)
    return JsonResponse({"error":"Method not allowed"})

             
