from django.test import TestCase
from rest_framework.test import APITestCase
from core.models import Subject, StudySession
from django.urls import reverse
from datetime import datetime

# Create your tests here.
class SubjectTests(APITestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(
            name ="Test Name",
            description ="Test Description"
        )
        self.subject2= Subject.objects.create(
            name ="Test 2",
            description="Test2"
        )

    def test_all_subjects(self):
        url = reverse("all-subjects")
        response =self.client.get(url)


        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data[0]["name"],"Test Name")
        self.assertEqual(response.data[0]["description"],"Test Description")
    
    def test_all_subjects_post(self):
        payload = {"name": "Test 3", "description": "Test3"}

        url = reverse("all-subjects")
        response = self.client.post(url,payload,format="json")

        new_subject = Subject.objects.get(name="Test 3")
        self.assertIsNotNone(new_subject)
        self.assertEqual(response.status_code,201)
        self.assertEqual(new_subject.name,payload["name"])
        self.assertEqual(response.data["name"],payload["name"])
        self.assertEqual(new_subject.description,payload["description"])

    def test_all_subjects_post_invalid(self):
        payload = {"name": "", "description":"Test3"}
        

        url = reverse("all-subjects")
        response = self.client.post(url,payload, format="json")
        self.assertEqual(response.status_code,400)
        self.assertEqual(Subject.objects.count(),2)

    
    def test_subject_detail(self):
        url= reverse("subject" , args=[self.subject1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data["name"],"Test Name")
        self.assertEqual(response.data["description"],"Test Description")
    
    def test_subject_detail_not_found(self):
        url = reverse("subject", args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code,404)
        self.assertEqual(response.data["error"],"Subject not found")

 
 

class StudySessionTests(APITestCase):
    def setUp(self):
        self.math = Subject.objects.create(
            name="Math",
            description="Mathematics Subject"
        )
        self.history = Subject.objects.create(
            name="History",
            description="WW2 History"
        )
        self.studysession1 = StudySession.objects.create(
            subject = self.math,
            duration_minutes = 60,
            notes = "Basic Concepts"
        )
        self.studysession2=StudySession.objects.create(
            subject = self.history,
            duration_minutes=120,
            notes ="France during WW2"
        )
    def test_study_session_detail(self):
        url =reverse("study-session", args=[self.studysession1.id])
        response =self.client.get(url)


        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data["subject"], self.math.id)
        self.assertEqual(response.data["duration_minutes"],60)

    def test_total_time_async(self):
        # StudySession.objects.create(
        #     subject=self.subject1,
        #     datetime="2026-01-29",
        #     duration_minutes=30,
        #     notes="Test Notes",
        # )
        url = reverse("total-time-all-subjects-async")
        response = self.client.get(url)
        breakpoint()
    
    #def test_study_session_detail_not_found(self):

    # def test_all_study_sessions(self):
    #     url = reverse("all-study-sessions")
    #     response = self.client.get (url)

    #     self.assertEqual(response.status_code,200)
    #     self.assertEqual(response.data[0]["subject"],self.math.id)
    #     self.assertEqual(response.data[0]["duration_minutes"],60)
    #     self.assertEqual(response.data[1]["subject"],self.history.id)
    #     self.assertEqual(response.data[1]["duration_minutes"],120)
        
    
    