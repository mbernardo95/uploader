from celery import shared_task

from uploader import process_file
from files.models import FileTask


@shared_task
def start_processing_file(file_task_id):
    # Mark the task as started
    file_task = FileTask.objects.get(id=file_task_id)
    file_task.state = "started"
    file_task.save()

    # Process the files. Only works on LocalStorageFiles
    input_file = file_task.inputFile.path
    output_file = input_file.replace(".csv", "_result.csv")
    completed, msg = process_file(input_file, output_file)

    # Store the result once finished or failed
    if completed:
        file_task.state = "finished"
        file_task.outputFile.name = output_file
    else:
        file_task.state = "failed"

    file_task.info = msg
    file_task.save()
