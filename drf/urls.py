from django.urls import include, path
from .views import (TotalTimeAllSubjectsAsync, ss_analytics, 
                    test2, 
                    all_subjects, 
                    study_session, 
                    subject, 
                    all_study_sessions, 
                    study_session_list, third_party_api, 
                    total_time_all_subjects,
)
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSET, StudySessionViewSET

router = DefaultRouter()
router.register (r"subjects",SubjectViewSET, basename ="subject")
router.register (r"study-sessions",StudySessionViewSET, basename ="study-session")




urlpatterns = [
    path('test2/', test2),
    path('all-subjects/', all_subjects,name ="all-subjects"),
    path('subject/<int:numri>/', subject, name="subject"),
    path('study-session/<int:numri>/', study_session, name="study-session"),
    path('all-study-sessions/', all_study_sessions),
    path('study-session-list/', study_session_list, name="study-session-filter"),
    path('total-time-all-subjects/', total_time_all_subjects),
    path("",include(router.urls)),
    path("total-time-all-subjects/", total_time_all_subjects, name="total-time-all-subjects"),
    path("total-time-all-subjects-async", TotalTimeAllSubjectsAsync.as_view(), name="total-time-all-subjects-async"),
    path("third-party-api/",third_party_api, name="third-party-api"),
    path("ss-analytics/", ss_analytics, name="ss-analytics"),
]