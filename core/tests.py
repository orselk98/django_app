import json
from django.test import TestCase
from core.models import Subject , StudySession
from django.test import Client

# Create your tests here.

class SubjectTests(TestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(
            name ="Test Name",
            description ="Test Description"
        )
        self.subject2= Subject.objects.create(
            name ="Test 2",
            description="Test2"
        )
    def test_get_subject_not_found(self):
        c=Client()
        response = c.get("/subject/9999/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"],"Subject not found")

    def test_get_subject(self):
        c = Client()
        subject_id=self.subject1.id
        response =c.get(f"/subject/{subject_id}/")
        self.assertEqual(response.json()["name"],"Test Name")
    
    def test_subject_list_get(self):
        c = Client()
        response=c.get(f"/subject-list/")
        #IS the response a list?
        self.assertEqual(isinstance(response.json(), list),True)
        #Does the list contain 2 items?
        self.assertEqual(len(response.json()),2)
        #Are the correct subject names present?
        names =[item["name"] for item in response.json()]
        self.assertIn("Test Name",names)
        self.assertIn("Test 2",names)

    def test_subject_post(self):
        c=Client()
        subject_count=Subject.objects.count()
        response=c.post(f"/subject-list/",json.dumps({"name":"Test Name3","description":"Test3"}),content_type="application/json")
        self.assertEqual(response.json()["message"],"Post created Successfully")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subject.objects.count(),subject_count+1)
        self.assertTrue(Subject.objects.filter(name="Test Name3").exists())
    
    def test_subject_post_invalid_json(self):
        c=Client()
        response=c.post(f"/subject-list/","Invalid Json",content_type="application/json")
        self.assertEqual(response.json(),{"error": "Invalid JSON"})
    
    def test_subject_post_missing_name(self):
        c=Client()
        response=c.post("/subject-list/",json.dumps({"description":"no-description"}),content_type="application/json")
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()["error"], "Name is required")



    def test_patch_subject(self):
        c=Client()
        subject_id = self.subject1.id
        response =c.patch(f"/subject/{subject_id}/",json.dumps({"name":"New Name",
                                                     "description": "New description"}))
        self.assertEqual(response.json()["message"],"Object Updated succesfully")
        updated_subject=Subject.objects.get(id=subject_id)
        self.assertEqual (updated_subject.name,"New Name")
    
    def test_patch_subject_not_found(self):
        c=Client()
        response=c.patch(f"/subject/9999/",json.dumps({"name":"new Name"}))
        self.assertEqual(response.status_code,404)
        self.assertEqual(response.json(),{"error":"Subject not found"})
    
    def test_patch_subject_invalid_json(self):
        c=Client()
        subject_id = self.subject1.id
        response=c.patch(f"/subject/{subject_id}/","Invalid JSON",json.dumps({"name":"new Name"}))
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),{"error":"Invalid JSON"})



    def test_delete_subject(self):
        c=Client()
        old_subject=self.subject1
        response =c.delete(f"/subject/{old_subject.id}/")
        self.assertEqual(response.json()["message"],"Deleted succesfully")
    def test_delete_subject_not_found(self):
        c=Client()
        response=c.delete(f"/subject/9999/")
        self.assertEqual(response.status_code,404)
        self.assertEqual(response.json(),{"error": "Subject not found"})

class StudySessionTests(TestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(
            name ="Test Name",
            description ="Test Description"
        )
        self.ss1 = StudySession.objects.create(
            subject = self.subject1,
            datetime="2025-12-12",
            duration_minutes=60,
            notes="Test Description"
        )
        self.ss2=StudySession.objects.create(
            subject=self.subject1,
            datetime="2025-12-12",
            duration_minutes=60,
            notes="Test Description"
        )
    def test_search_date_invalid_year(self):
        c=Client()
        response= c.get(f"/search-by-date/3000-12-12/")
        self.assertEqual(response.json(),{"Error":"Invalid year"})
    
    def test_search_date(self):
        c=Client()
        response= c.get(f"/search-by-date/2025-12-12/")
        self.assertEqual(len(response.json()),2)
        self.assertEqual(response.json()[0]['subject'], "Test Name")
    def test_ss_not_found(self):
        c=Client()
        response=c.get(f"/search-by-date/2024-12-12/")
        self.assertEqual(response.json(),{"Error":"StudySession not found"})

    def test_total_time_subject_not_found(self):
        c=Client()
        response=c.get(f"/total-time/4545/")
        self.assertEqual(response.json(),{"Error":"Subject not found"})

    def test_total_time_subject(self):
        c=Client()
        subject_id = self.subject1.id
        response =c.get(f"/total-time/{subject_id}/")
        self.assertEqual(response.json(),{"Total Time":120})

    def test_total_time_no_ss(self):
        c=Client()
        new_subject =Subject.objects.create(
            name="No SS Subject",
            description="No SS Description"
        )

        response=c.get(f"/total-time/{new_subject.id}/")
        self.assertEqual(response.json(),{"Error":"Subject has no Study Sessions"})

    def test_search_by_date_no_ss(self):
        c=Client()
        response=c.get(f"/search-by-date/2024-11-11/")
        self.assertEqual(response.json(),{"Error":"StudySession not found"})
    
    def test_get_study_session_list(self):
        c=Client()
        response=c.get(f"/study-session-list/")
        self.assertEqual(isinstance(response.json(),list),True)
        self.assertEqual(len(response.json()),2)

    def test_get_single_study_session(self):
        c=Client()
        ss_id=self.ss1.id
        response=c.get(f"/study-session/{ss_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"],ss_id)

    def test_get_study_session_not_found(self):
        c=Client()
        response=c.get(f"/study-session/9999/")
        self.assertEqual(response.status_code,404)
        self.assertEqual(response.json(),{"error":"Study Session not found"})


        



        



    


    

