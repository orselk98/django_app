from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
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
        ss_qs = StudySession.objects.select_related('subject').all()
        paginator = StudySessionPagination()
        page = paginator.paginate_queryset(ss_qs, request)
        serializer = StudySessionserializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
    return Response({"error": "Method not allowed."})
    