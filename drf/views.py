from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import viewsets
from rest_framework import status
from datetime import datetime, date
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
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        
@api_view(["GET"])
def subject(request, numri):
        try:
            subject = Subject.objects.get(id=numri)
            serializer = SubjectSerializer(subject, many=False)
            return Response(serializer.data)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def study_session(request, numri):
     try:
          study_session = StudySession.objects.get(id=numri)
          serializer = StudySessionserializer(study_session)
          return Response(serializer.data)
     except StudySession.DoesNotExist:
          return Response({"error": "Study session not found"}, status=status.HTTP_404_NOT_FOUND)

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
    qs = StudySession.objects.all()
    #Get all filter parameters
    subject_id =request.GET.get("subject_id", None)
    duration_minutes = request.GET.get("duration_minutes", None)
    start_date =request.GET.get('start_date')
    end_date =request.GET.get('end_date')
    ordering = request.GET.get('ordering', None)

    #Apply filters only if they exist
    if subject_id:
         qs = qs.filter(subject__id=subject_id)

    if duration_minutes:
         qs = qs.filter(duration_minutes__gte=duration_minutes)

    if start_date and end_date:
         start = datetime.fromisoformat(start_date)
         end = datetime.fromisoformat(end_date)
         qs = qs.filter(datetime__gte=start, datetime__lte=end)

    if ordering:
        if ordering.startswith('-'):
            try:
                date_obj = date.fromisoformat(ordering[1:])
            except ValueError:
                return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
            qs = StudySession.objects.all().filter(date__lte=date_obj).order_by("-datetime")
            
            
        else:
            try:
                date_obj=date.fromisoformat(ordering)
            except ValueError:
                return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
            qs=StudySession.objects.all().filter(date__gte=date_obj).order_by("datetime")
            serializer = StudySessionserializer(qs,many=True)
            return Response(serializer.data)
        
        serializer = StudySessionserializer(qs, many=True)
        return Response(serializer.data)
    #Apply pagination
    paginator = StudySessionPagination()
    paginated_qs = paginator.paginate_queryset(qs, request)

    serializer = StudySessionserializer(paginated_qs, many=True)

    return paginator.get_paginated_response(serializer.data)


class SubjectViewSET(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class StudySessionViewSET(viewsets.ModelViewSet):
    queryset = StudySession.objects.all()
    serializer_class = StudySessionserializer


  
    