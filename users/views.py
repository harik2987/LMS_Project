from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import HttpResponse, HttpResponseForbidden
from users.models import CustomUser, Branch
from courses.models import Course, SCORM
from django.contrib.auth.decorators import login_required
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/shared/register.html', {'form': form})


# SuperAdmin dashboard view
@login_required
def super_admin_dashboard(request):
    if request.user.role != 'superadmin':
        logger.warning(f"Unauthorized access attempt by user {request.user.username} to SuperAdmin dashboard.")
        return HttpResponseForbidden("Unauthorized")

    total_users = CustomUser.objects.count()
    total_courses = Course.objects.count()

    return render(request, 'users/dashboards/superadmin.html', {
        'total_users': total_users,
        'total_courses': total_courses,
    })


# Admin dashboard view
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        logger.warning(f"Unauthorized access attempt by user {request.user.username} to Admin dashboard.")
        return HttpResponseForbidden("Unauthorized")

    admin_branch = request.user.branch
    if not admin_branch:
        logger.error(f"Admin {request.user.username} does not have an assigned branch.")
        return HttpResponseForbidden("No branch assigned to this admin.")

    # Correctly filter courses and users by branch
    branch_courses = Course.objects.filter(branch=admin_branch)
    total_users = CustomUser.objects.filter(branch=admin_branch).count()
    total_courses = branch_courses.count()

    return render(request, 'users/dashboards/admin.html', {
        'branch_name': admin_branch.name,
        'branch_courses': branch_courses,
        'total_users': total_users,
        'total_courses': total_courses,
    })


# Instructor dashboard view
@login_required
def instructor_dashboard(request):
    if request.user.role != 'instructor':
        logger.warning(f"Unauthorized access attempt by user {request.user.username} to Instructor dashboard.")
        return HttpResponseForbidden("Unauthorized")

    # Fetch courses assigned to the instructor
    assigned_courses = Course.objects.filter(instructor=request.user)

    # Fetch learners enrolled in these courses
    learners = CustomUser.objects.filter(role='learner', enrolled_courses__in=assigned_courses).distinct()

    # Prepare SCORM progress for each learner
    learner_scorm_progress = [
        {
            "learner": learner,
            "scorm_progress": SCORM.objects.filter(course__in=assigned_courses, course__enrolled_users=learner)
        }
        for learner in learners
    ]

    return render(request, 'users/dashboards/instructor.html', {
        'assigned_courses': assigned_courses,
        'learner_scorm_progress': learner_scorm_progress,
    })


# Learner dashboard view
@login_required
def learner_dashboard(request):
    if request.user.role != 'learner':
        logger.warning(f"Unauthorized access attempt by user {request.user.username} to Learner dashboard.")
        return HttpResponseForbidden("Unauthorized")

    # Fetch courses the learner is enrolled in
    enrolled_courses = Course.objects.filter(enrolled_users=request.user)

    # Fetch SCORM content for the enrolled courses
    scorm_content = SCORM.objects.filter(course__in=enrolled_courses)

    return render(request, 'users/dashboards/learner.html', {
        'enrolled_courses': enrolled_courses,
        'scorm_content': scorm_content,
    })


# Role-based redirection view
def role_based_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')

    role_redirects = {
        'superadmin': 'dashboard_superadmin',
        'admin': 'dashboard_admin',
        'instructor': 'dashboard_instructor',
        'learner': 'dashboard_learner',
    }
    redirect_url = role_redirects.get(request.user.role, 'login')
    logger.info(f"Redirecting user {request.user.username} to {redirect_url} dashboard.")
    return redirect(redirect_url)


# Home view
def home(request):
    # Placeholder home view for the LMS
    return HttpResponse("Welcome to the LMS Home Page!")


# User list view
@login_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/shared/user_list.html', {'users': users})
