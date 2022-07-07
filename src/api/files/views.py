from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import FileTask
from .tasks import start_processing_file


@csrf_exempt
@require_http_methods(["POST"])
def schedule_file_view(request):
    file = request.FILES["file"]
    file_task = FileTask.objects.create(inputFile=file)
    start_processing_file.delay(file_task.id)
    return JsonResponse({"id": file_task.id})


@csrf_exempt
@require_http_methods(["GET"])
def download_result_views(request, pk):
    file_task = FileTask.objects.get(id=pk)

    if file_task.state == FileTask.DEFAULT_STATE:
        return JsonResponse({"msg": "Task doesn't started."})
    elif file_task.state == "started":
        return JsonResponse({"msg": "Task is being processed."})
    elif file_task.state == "failed":
        return JsonResponse({"msg": "Task failed."})
    else:
        return FileResponse(file_task.outputFile)
