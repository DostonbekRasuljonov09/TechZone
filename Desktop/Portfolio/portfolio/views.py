from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import SkillCategory, Project, Message


def index(request):
    categories = SkillCategory.objects.all()
    projects = Project.objects.all()
    context = {
        'categories': categories,
        'projects': projects,
    }
    return render(request, 'portfolio/index.html', context)


def about(request):
    return render(request, 'portfolio/about.html')


def category_projects(request, slug):
    category = get_object_or_404(SkillCategory, slug=slug)
    projects = Project.objects.filter(category=category)
    context = {
        'category': category,
        'projects': projects,
    }
    return render(request, 'portfolio/category_projects.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    images = project.images.all()
    context = {
        'project': project,
        'images': images,
    }
    return render(request, 'portfolio/project_detail.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        text = request.POST.get('text', '').strip()
        if name and email and subject and text:
            Message.objects.create(name=name, email=email, subject=subject, text=text)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': "Barcha maydonlarni to'ldiring."})
    return render(request, 'portfolio/contact.html')
