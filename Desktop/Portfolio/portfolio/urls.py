from django.urls import path
from .views import index, about, category_projects, project_detail, contact

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('category/<slug:slug>/', category_projects, name='category_projects'),
    path('project/<slug:slug>/', project_detail, name='project_detail'),
]
