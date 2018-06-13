from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('semanal/', views.semanal_template , name='semanal'),
    path('semanal/<slug:slug>', views.ResultSemanalView , name='diario'),
    path('about/', TemplateView.as_view(template_name="polls/about.html")),
]
