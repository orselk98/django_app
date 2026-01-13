from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import viewsets
from rest_framework import status
from core.models import Subject, StudySession
from .pagination import StudySessionPagination
from .serializers import SubjectSerializer, StudySessionserializer

@api_view(['GET'])
def test2(request):
    return Response({"message": "DRF view is working."})

@api_view(["GET", "POST"])
def all_subjects(request):
    if request.method == "GET":
        qs = Subject.objects.all()
        serializer = SubjectSerializer(qs, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
@api_view(["GET"])
def subject(request, numri):
        subject = Subject.objects.get(id=numri)
        serializer = SubjectSerializer(subject, many=False)
        return Response(serializer.data)

@api_view(["GET"])
def study_session(request, numri):
     study_session = StudySession.objects.get(id=numri)
     serializer = StudySessionserializer(study_session)
     return Response(serializer.data)

@api_view (["GET", "POST"])
def all_study_sessions(request):
     if request.method  == "GET":
          qs =StudySession.objects.all()
          serializers = StudySessionserializer(qs, many =True)
          return Response (serializers.data)
     
     if request.method == "POST":
          serializers = StudySessionserializer(data=request.data)
          if serializers.is_valid():
                serializers.save()
                return Response (serializers.data)
          return Response (serializers.errors, status.HTTP_400_BAD_REQUEST)
     
@api_view (["GET"])
def study_session_list(request):
    if request.method == "GET":
        subject_id = request.GET.get("subject_id", None)
        #Check if subject is is provided
        #Search for db for studysession with subject_id
        #return
        if subject_id:
            
            qs = StudySession.objects.filter(subject__id=subject_id)

            serializer = StudySessionserializer(qs, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        duration_minutes = request.GET.get("duration_minutes", None)
        if duration_minutes:
             qs = StudySession.objects.filter(duration_minutes__gte=duration_minutes)
             
             serializer = StudySessionserializer(qs, many=True)

             return Response(serializer.data,status=status.HTTP_200_OK)
        
        
        start_date =request.GET.get('start_date')
        end_date =request.GET.get('end_date')
        if start_date and end_date:
             start =datetime.fromisoformat(start_date)
             end =datetime.fromisoformat(end_date)
             qs = StudySession.objects.filter(datetime__gte=start_date,datetime__lte=end_date)
             
             serializer = StudySessionserializer(qs,many=True)

             return Response(serializer.data,status=status.HTTP_200_OK)


             


class SubjectViewSET(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class StudySessionViewSET(viewsets.ModelViewSet):
    queryset = StudySession.objects.all()
    serializer_class = StudySessionserializer


  
    