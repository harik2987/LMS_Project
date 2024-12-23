from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, SCORM
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import logging
import json

# Set up logging
logger = logging.getLogger(__name__)

# Role-based permission decorator
def role_required(roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# View to display the list of courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/list/course_list.html', {'courses': courses})

# View to handle content upload
@login_required
@role_required(['superadmin', 'admin', 'instructor'])
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

# View for SCORM playback
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

# API view for SCORM metadata
@login_required
def play_scorm(request, id):
    try:
        scorm_package = get_object_or_404(SCORM, id=id)
        logger.info(f"SCORM Package Found: {scorm_package.title}, ID: {scorm_package.id}")
        return JsonResponse({
            "id": scorm_package.id,
            "title": scorm_package.title,
            "launch_url": scorm_package.launch_url,
            "version": scorm_package.version
        })
    except SCORM.DoesNotExist:
        logger.warning(f"SCORM Package with ID {id} not found.")
        return JsonResponse({"error": "SCORM package not found"}, status=404)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)

# API to handle SCORM runtime tracking
@csrf_exempt  # Temporarily disable CSRF for testing
def scorm_runtime_update(request, course_id):
    if request.method == "POST":
        try:
            # Parse the JSON payload
            data = json.loads(request.body)
            scorm_package = get_object_or_404(SCORM, course_id=course_id)

            # Extract runtime data
            progress = data.get('progress', 0)
            score = data.get('score', None)
            completion_status = data.get('completion_status', 'not_started')

            # Update runtime tracking
            scorm_package.time_spent += progress  # Simulate time spent increment
            scorm_package.score = score if score is not None else scorm_package.score
            scorm_package.completion_status = completion_status
            scorm_package.last_accessed = scorm_package.updated_at  # Update last accessed timestamp
            scorm_package.save()

            logger.info(f"SCORM Runtime Updated: Course ID: {course_id}, Data: {data}")
            return JsonResponse({"status": "success", "message": "Runtime data updated successfully"})
        except json.JSONDecodeError:
            logger.error("Invalid JSON payload")
            return JsonResponse({"status": "error", "message": "Invalid JSON payload"}, status=400)
        except Exception as e:
            logger.error(f"Runtime tracking error: {str(e)}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)
