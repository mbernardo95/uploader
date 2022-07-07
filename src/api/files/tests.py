import os

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from unittest.mock import patch

from files.models import FileTask


class ScheduleFileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        example_csv = SimpleUploadedFile(
            "test_ScheduleFileViewTest.csv",
            b"testing_content",
        )
        self.endpoint = reverse("files:schedule-file")
        self.body = {"file": example_csv}

    @patch("files.views.start_processing_file")
    def test_file_task_created_with_file(self, _):
        self.client.post(self.endpoint, self.body)
        task_created = FileTask.objects.last()
        stored_file = open(task_created.inputFile.path).read()

        self.assertEqual(stored_file, "testing_content")
        os.remove(task_created.inputFile.path)

    @patch("files.views.start_processing_file.delay")
    def test_start_processing_is_called(self, mock_processing_file):
        self.client.post(self.endpoint, self.body)
        task_created = FileTask.objects.last()

        mock_processing_file.assert_called_with(task_created.id)
        os.remove(task_created.inputFile.path)

    @patch("files.views.start_processing_file")
    def test_task_id_returned(self, _):
        result = self.client.post(self.endpoint, self.body)
        task_created = FileTask.objects.last()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json().get("id"), task_created.id)
        os.remove(task_created.inputFile.path)


class DownloadResultViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.input_example = SimpleUploadedFile(
            "test_DownloadResultViewTest_input.csv",
            b"testing_content_input",
        )
        self.output_example = SimpleUploadedFile(
            "test_DownloadResultViewTest_output.csv",
            b"testing_content_output",
        )
        self.file_task = FileTask.objects.create(
            inputFile=self.input_example,
            outputFile=self.output_example,
        )
        self.endpoint = reverse(
            "files:download-result",
            kwargs={
                "pk": self.file_task.id,
            },
        )

    def test_task_is_not_started(self):
        self.file_task.state = "pending"
        self.file_task.save()
        result = self.client.get(self.endpoint)

        self.assertEqual(result.json().get("msg"), "Task doesn't started.")

    def test_task_is_already_running(self):
        self.file_task.state = "started"
        self.file_task.save()
        result = self.client.get(self.endpoint)

        self.assertEqual(result.json().get("msg"), "Task is being processed.")

    def test_task_has_failed(self):
        self.file_task.state = "failed"
        self.file_task.save()
        result = self.client.get(self.endpoint)

        self.assertEqual(result.json().get("msg"), "Task failed.")

    def test_task_is_finished(self):
        self.file_task.state = "finished"
        self.file_task.save()
        result = self.client.get(self.endpoint)

        self.assertEqual(next(result.streaming_content), b"testing_content_output")

    def tearDown(self):
        os.remove(self.file_task.inputFile.path)
        os.remove(self.file_task.outputFile.path)
