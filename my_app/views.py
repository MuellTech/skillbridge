from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Resume, CareerAnalysis
import openai
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.http import JsonResponse, HttpResponse
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile
from django.db.models import Count
from reportlab.pdfgen import canvas
from io import BytesIO
import json

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    analyses = CareerAnalysis.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'analyses': analyses})

@login_required
def upload_resume(request):
    if request.method == 'POST':
        if 'resume' not in request.FILES:
            messages.error(request, 'Please select a file to upload')
            return redirect('upload_resume')
        
        resume_file = request.FILES['resume']
        target_field = request.POST.get('target_field')
        
        # Save the resume
        resume = Resume.objects.create(
            user=request.user,
            file=resume_file
        )
        
        # Extract text from resume
        content = resume_file.read().decode('utf-8')
        resume.parsed_content = content
        resume.save()
        
        # Analyze with OpenAI
        try:
            analysis = analyze_resume(content, target_field)
            
            CareerAnalysis.objects.create(
                user=request.user,
                resume=resume,
                target_field=target_field,
                transferable_skills=analysis['transferable_skills'],
                suggested_activities=analysis['suggested_activities']
            )
            
            messages.success(request, 'Resume analyzed successfully!')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error analyzing resume: {str(e)}')
            return redirect('upload_resume')
    
    return render(request, 'upload_resume.html')

def analyze_resume(content, target_field):
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    prompt = f"""
    Analyze this resume content and provide recommendations for transitioning to {target_field}.
    Resume content: {content}
    
    Please provide:
    1. List of transferable skills relevant to {target_field}
    2. Suggested activities, courses, or projects to develop relevant skills
    
    Format the response as JSON with 'transferable_skills' and 'suggested_activities' keys.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a career counselor expert in skill analysis and career transitions."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse the response and return as dictionary
    try:
        return eval(response.choices[0].message.content)
    except:
        return {
            'transferable_skills': ['Error parsing skills'],
            'suggested_activities': ['Error parsing activities']
        }

@login_required
def history(request):
    analyses = CareerAnalysis.objects.filter(user=request.user)
    return render(request, 'history.html', {'analyses': analyses})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return render(request, 'registration/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

@login_required
def profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    analyses = CareerAnalysis.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'profile.html', {
        'profile': profile,
        'recent_analyses': analyses
    })

@login_required
def edit_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def search_analysis(request):
    query = request.GET.get('q', '')
    analyses = CareerAnalysis.objects.filter(
        user=request.user,
        target_field__icontains=query
    ).order_by('-created_at')
    
    return render(request, 'search_results.html', {'analyses': analyses, 'query': query})

@login_required
def generate_pdf_report(request, analysis_id):
    analysis = get_object_or_404(CareerAnalysis, id=analysis_id, user=request.user)
    
    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # Add content to PDF
    p.drawString(100, 800, f"Career Analysis Report - {analysis.target_field}")
    p.drawString(100, 750, f"Generated on: {analysis.created_at.strftime('%Y-%m-%d')}")
    
    y = 700
    p.drawString(100, y, "Transferable Skills:")
    y -= 20
    for skill in analysis.transferable_skills:
        p.drawString(120, y, f"• {skill}")
        y -= 15
    
    y -= 20
    p.drawString(100, y, "Suggested Activities:")
    y -= 20
    for activity in analysis.suggested_activities:
        p.drawString(120, y, f"• {activity}")
        y -= 15
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'analysis_{analysis_id}.pdf')

@login_required
def skills_analytics(request):
    return render(request, 'analytics.html')

@login_required
def analytics_data(request):
    # Get skill statistics
    analyses = CareerAnalysis.objects.filter(user=request.user)
    
    # Prepare data for charts
    target_fields = analyses.values('target_field').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Collect all skills across analyses
    all_skills = {}
    for analysis in analyses:
        for skill in analysis.transferable_skills:
            all_skills[skill] = all_skills.get(skill, 0) + 1
    
    # Sort skills by frequency
    top_skills = dict(sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:10])
    
    data = {
        'target_fields': {
            'labels': [field['target_field'] for field in target_fields],
            'data': [field['count'] for field in target_fields]
        },
        'top_skills': {
            'labels': list(top_skills.keys()),
            'data': list(top_skills.values())
        }
    }
    
    return JsonResponse(data)

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
