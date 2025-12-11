from django.shortcuts import render
from .models import Subject
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def detail(request):
    return JsonResponse({"message":"view is working"})

def subjects_list(request):
    if request.method == 'GET':
        subject_qs = Subject.objects.all().values("id","name","description")
        subjects = list(subject_qs)
        return JsonResponse(subjects, safe=False)
    return JsonResponse({"error":"Method not allowed"})

@csrf_exempt
def subject(request, numri):
    if request.method == 'GET':
        subject = Subject.objects.first(id=numri)
        subject_dict ={
            "id": subject.id,
            "name": subject.name,
            "description": subject.description
        }
        return JsonResponse(subject, safe=False)
    
#how to make a post request in django
    #duhen marre te dhenat nga request:

    if request.method == 'POST':
        try:
            data =json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse ({"error": "Invalid JSON"}, status = 400)
        
        name = data.get('name')
        description = data.get('description', '')


        #duhen krijuar te dhenat  objekti ne database

        subject = Subject.objects.create(name=name, description=description)
        #dergo mesazhin e suksesit
        return JsonResponse ({"message": f"{name} and {description} was created successfully"}, status = 201)
    
    if request.method == 'PATCH':
        #Marrim te dhenat nga request(id, name, description) 
        try:
            subject = Subject.objects.get(id=numri)
            data = json.loads(request.body)
            if 'name' in data:
                subject.name = data['name']
            if 'description' in data:
                subject.description = data['description']
                subject.save()
        except:
            



        
        #Duhet marre objekti nga db me id
            return JsonResponse({"error": "Subject not found"}, status=404)

        #duhet ndryshu name dhe description 



        #duhet bere save objekti ne db

        #return succesful message : Old dhe new
    
    return JsonResponse({"error":"Method not allowed"})





