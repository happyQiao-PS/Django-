from django.conf.urls import url

from Student_grade import views

urlpatterns = [
    url(r"showGrade/$",views.showGrade,name='showGrades'),
    url(r"^showGrade/(\d+)/",views.showGrade_id,name='showGrade')
]