from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, SCORM
from .forms import CourseForm
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import logging
import json

# Set up logging
logger = logging.getLogger(__name__)

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/list/course_list.html', {'courses': courses})

@login_required
def upload_content(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['content_file']
            allowed_types = ['application/zip', 'video/mp4', 'application/pdf']
            if uploaded_file.content_type not in allowed_types:
                return JsonResponse({"error": "Unsupported file type"}, status=400)
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/upload/upload_content.html', {'form': form})

@login_required
def scorm_playback(request, course_id):
    try:
        scorm_package = get_object_or_404(SCORM, course_id=course_id)
        logger.info(f"SCORM Package Found: {scorm_package.title}, ID: {scorm_package.id}")
        return render(request, 'courses/scorm/playback.html', {
            'scorm_title': scorm_package.title,
            'launch_url': scorm_package.launch_url,
            'course_id': course_id
        })
    except Exception as e:
        logger.error(f"Error during SCORM playback: {str(e)}")
        return HttpResponse("An unexpected error occurred.", status=500)

@login_required
def play_scorm(request, course_id):
    """
    Retrieve SCORM metadata and provide a launch URL for playback.
    """
    try:
        scorm = get_object_or_404(SCORM, course_id=course_id)
        if request.GET.get('format') == 'json':
            return JsonResponse({
                'title': scorm.title,
                'description': scorm.course.description,
                'launch_url': scorm.launch_url,
            })
        return render(request, 'courses/play_scorm.html', {'scorm': scorm})
    except Exception as e:
        logger.error(f"Error in play_scorm: {str(e)}")
        return JsonResponse({"error": "SCORM playback failed"}, status=500)

@login_required
@csrf_exempt
def scorm_runtime_update(request, course_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            scorm_package = get_object_or_404(SCORM, course_id=course_id)

            progress = data.get('progress', 0)
            score = data.get('score')
            completion_status = data.get('completion_status', 'not_started')

            scorm_package.time_spent += progress
            scorm_package.score = score or scorm_package.score
            scorm_package.completion_status = completion_status
            scorm_package.last_accessed = scorm_package.updated_at
            scorm_package.save()

            logger.info(f"SCORM Runtime Updated: Course ID: {course_id}, Data: {data}")
            return JsonResponse({"status": "success"})
        except Exception as e:
            logger.error(f"Runtime tracking error: {str(e)}")
            return JsonResponse({"error": "Unexpected error"}, status=500)
