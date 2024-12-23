from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from users.models import CustomUser, Branch
from courses.models import Course, SCORM
from django.contrib.auth.decorators import login_required

# Registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/shared/register.html', {'form': form})

# Dashboard views
@login_required
def super_admin_dashboard(request):
    if not hasattr(request.user, 'role') or request.user.role != 'superadmin':
        return HttpResponse("Unauthorized", status=403)

    total_users = CustomUser.objects.count()
    total_courses = Course.objects.count()

    return render(request, 'users/dashboards/superadmin.html', {
        'total_users': total_users,
        'total_courses': total_courses,
    })

@login_required
def admin_dashboard(request):
    if not hasattr(request.user, 'role') or request.user.role != 'admin':
        return HttpResponse("Unauthorized", status=403)

    admin_branch = request.user.branch
    if not admin_branch:
        return HttpResponse("No branch assigned to this admin.", status=403)

    total_users = CustomUser.objects.filter(branch=admin_branch).count()
    total_courses = Course.objects.filter(branch=admin_branch).count()

    return render(request, 'users/dashboards/admin.html', {
        'branch_name': admin_branch.name,
        'total_users': total_users,
        'total_courses': total_courses,
    })

@login_required
def instructor_dashboard(request):
    if not hasattr(request.user, 'role') or request.user.role != 'instructor':
        return HttpResponse("Unauthorized", status=403)

    assigned_courses = Course.objects.filter(instructor=request.user)
    learners = CustomUser.objects.filter(role='learner', enrolled_courses__in=assigned_courses).distinct()

    learner_scorm_progress = []
    for learner in learners:
        scorm_progress = SCORM.objects.filter(course__in=assigned_courses, course__enrolled_users=learner)
        learner_scorm_progress.append({
            "learner": learner,
            "scorm_progress": scorm_progress,
        })

    return render(request, 'users/dashboards/instructor.html', {
        'assigned_courses': assigned_courses,
        'learner_scorm_progress': learner_scorm_progress,
    })

@login_required
def learner_dashboard(request):
    if not hasattr(request.user, 'role') or request.user.role != 'learner':
        return HttpResponse("Unauthorized", status=403)

    enrolled_courses = Course.objects.filter(enrolled_users=request.user)
    scorm_content = SCORM.objects.filter(course__in=enrolled_courses)

    return render(request, 'users/dashboards/learner.html', {
        'enrolled_courses': enrolled_courses,
        'scorm_content': scorm_content,
    })

@login_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/shared/user_list.html', {'users': users})

def role_based_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')

    role_redirects = {
        'superadmin': 'super_admin_dashboard',
        'admin': 'admin_dashboard',
        'instructor': 'instructor_dashboard',
        'learner': 'learner_dashboard',
    }
    return redirect(role_redirects.get(request.user.role, 'login'))

def home(request):
    return HttpResponse("Welcome to the LMS Home Page!")
