from urllib import request
from django.shortcuts import render
from .models import Subject, StudySession
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json

# Create your views here.

def index(request):
    #Serve the frontend home page
    return render(request, 'core/index.html')

def test_view(request):
    return JsonResponse({"message":"view is working."})

@csrf_exempt
def subject_list(request):
    if request.method == 'GET':
        subject_qs = Subject.objects.all().values("id","name","description")
        subjects = list(subject_qs)
        return JsonResponse(subjects, safe=False)
    
    if request.method =='POST':
        #duhen marre te dhenat nga request:
        try:
            data =json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse ({"error": "Invalid JSON"}, status = 400)
        
        name = data.get('name')
        if not name:
            return JsonResponse ({"error": "Name is required"}, status = 400)
        description = data.get('description', '')


        #duhen krijuar te dhenat  objekti ne database

        subject = Subject.objects.create(name=name, description=description)
        #dergo mesazhin e suksesit
        return JsonResponse ({"message": "Post created Successfully"}, status = 201)




@csrf_exempt
def subject(request, numri):
    if request.method == 'GET':
        try:
            subject = Subject.objects.get(id=numri)
        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)


        subject_dict ={
            "id": subject.id,
            "name": subject.name,
            "description": subject.description
        }

        return JsonResponse(subject_dict, safe=False)
    
#how to make a post request in django
  

    if request.method == 'POST':
          #duhen marre te dhenat nga request:
        try:
            data =json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse ({"error": "Invalid JSON"}, status = 400)
        
        name = data.get('name')
        if not name:
            return JsonResponse ({"error": "Name is required"}, status = 400)
        description = data.get('description', '')


        #duhen krijuar te dhenat  objekti ne database
        subject = Subject.objects.create(name=name, description=description)

        #dergo mesazhin e suksesit
        return JsonResponse ({"message": f"{name} and {description} was created successfully"}, status = 201)
    
    if request.method == 'PATCH':
        #Marrim te dhenat nga request(id, name, description) 
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        name = data.get("name")
        description = data.get("description", "")
        # Duhet marr objekti nga db me id
        try:
            subject = Subject.objects.get(id=numri)
        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)
        # Duhet ndryshuar name dhe description
        if name:
            subject.name = name
        if description:
            subject.description = description
        # Duhet ber save objekti ne db
        subject.save()
        return JsonResponse({"message":"Object Updated succesfully"})

        
    
    
    if request.method == "DELETE":
        try:
            subject = Subject.objects.get(id=numri)
        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)

        if subject:
                subject.delete()
                return JsonResponse({"message": "Deleted succesfully"})
        return JsonResponse({"error": "Subject not found"})

    return JsonResponse({"error":"Method not allowed."})

def study_session_list(request):
    if request.method == "GET":
        #get all requests from db
        ss_qs = StudySession.objects.select_related('subject').all()
        ss_list = []
        #optimize
        for ss in ss_qs:
            ss_list.append({
                "id": ss.id,
                "subject": ss.subject.name,
                "subject_id": ss.subject.id,
                "datetime": ss.datetime.isoformat() if ss.datetime else None,
                "duration_minutes": ss.duration_minutes,
                "notes": ss.notes
        })

        return JsonResponse(ss_list, safe =False)
    return JsonResponse({"error":"Method not allowed."})


@csrf_exempt
def study_session(request, numri):
    if request.method == 'GET':
        try:
            ss = StudySession.objects.get(id=numri)
        except StudySession.DoesNotExist:
            return JsonResponse({"error": "Study Session not found"}, status=404)


        ss_dict = {
         "id": ss.id,
            "subject_name": ss.subject.name,
            "subject_id": ss.subject.id,
            "datetime": ss.datetime.isoformat() if ss.datetime else None,
            "duration_minutes": ss.duration_minutes,
            "notes": ss.notes
        }

        return JsonResponse(ss_dict, safe=False)
    
    if request.method == "POST":
        # Duhen marre te dhenat nga requesti
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        subject_id = data.get("subject")
        session_datetime = data.get("datetime")
        duration_minutes = data.get("duration_minutes", 60)
        notes = data.get("notes", "")

        # Get the Subject object
        try:
            subject_obj = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return JsonResponse({"error": "Subject not found"}, status=404)


        # Duhet krijuar objekti ne db
        ss = StudySession.objects.create(
            subject=subject_obj, 
            datetime=session_datetime,
            duration_minutes=duration_minutes,
            notes=notes
        )

        # Dergo mesazh suksesi
        return JsonResponse({"message":"Study Session was created succesfully"})
    
    if request.method == "PATCH":
        # Marrim te dhenat nga requesti (id, name, description)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        subject_id = data.get("subject", None)
        session_datetime = data.get("datetime", None)
        duration_minutes = data.get("duration_minutes", None)
        notes = data.get("notes", None)

        # Duhet marr objekti nga db me id
        ss = StudySession.objects.get(id=numri)
        # Duhet ndryshuar name dhe description
        if subject_id:
            try:
                subject_obj = Subject.objects.get(id=subject_id)
                ss.subject = subject_obj
            except Subject.DoesNotExist:
                return JsonResponse({"error": "Subject not found"}, status=404)
        if session_datetime:
            ss.datetime = session_datetime
        if duration_minutes:
            ss.duration_minutes = duration_minutes
        if notes:
            ss.notes = notes
        # Duhet ber save objekti ne db
        ss.save()

        # return successful message, Old dhe new
        return JsonResponse({"message":"Object Updated succesfully"})

    if request.method == "DELETE":
        ss = StudySession.objects.get(id=numri)
        if ss:
            ss.delete()
            return JsonResponse({"message": "Deleted succesfully"})
        return JsonResponse({"Error": "Study Session not found"})
    
    return JsonResponse({"Error":"Method not allowed."})

# Krijo endpoint te ri GET, me url /total-time/
# Ku useri do te japi id e nje subjecti
# Dhe do te marri total time te shpenzuar ne study sessions per ate subject
def total_time(request, id):
    if request.method == "GET":
        try:
            subject = Subject.objects.get(id=id)
        except Subject.DoesNotExist:
            return JsonResponse({"Error":"Subject not found"})
        
        
        # Duhet te marrim duration_minutes nga Study Session
        ss_qs = StudySession.objects.filter(subject=subject)

        # For loop te mbledhi kohen dhe do printoj totalin
        sum_total_time = 0 
        for ss in ss_qs:
                sum_total_time = sum_total_time + ss.duration_minutes 
        
        if not ss_qs:
            return JsonResponse({"Error":"Subject has no Study Sessions"})
        
        
        # Return Total time spent on a subject
        return JsonResponse({"Total Time": sum_total_time})
    
def search_by_date(request, date_string):
    if request.method == "GET":
        # Supozojm qe date_string eshte 2025-12-10 YYYY-MM-DD
        if int(date_string[:4]) > 2100:
            return JsonResponse({"Error":"Invalid year"})
        datetime_search = datetime.fromisoformat(date_string)
        
        ss_qs = StudySession.objects.filter(datetime__year=datetime_search.year,
                                                datetime__month=datetime_search.month,
                                                datetime__day=datetime_search.day)
            
        ss_list = []
        for ss in ss_qs:
            print("ERROR ",ss)
            ss_list.append({
                "id": ss.id,
                "subject": ss.subject.name,
                "subject_id": ss.subject.id,
                "datetime": ss.datetime.isoformat() if ss.datetime else None,
                "duration_minutes": ss.duration_minutes,
                "notes": ss.notes
            })
        if ss_list == []:
            return JsonResponse({"Error":"StudySession not found"})
        return JsonResponse(ss_list, safe=False)
