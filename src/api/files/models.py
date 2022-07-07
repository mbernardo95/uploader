from django.db import models


class FileTask(models.Model):
    """
    FileTask contains the information about the input_file with song data,
    the processing state of the task, and also the output_file once it's
    completed.
    """

    inputFile = models.FileField(blank=False, null=False)
    outputFile = models.FileField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)

    DEFAULT_STATE = "pending"
    STATE_CHOICES = [
        (DEFAULT_STATE, "PENDING"),
        ("started", "STARTED"),
        ("finished", "FINISHED"),
        ("failed", "FAILED"),
    ]
    state = models.CharField(
        default=DEFAULT_STATE,
        choices=STATE_CHOICES,
        max_length=10,
    )

    def __str__(self):
        return f"{self.inputFile} - {self.state}"
