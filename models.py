from django.db import models

class Word(models.Model):
    name = models.CharField(max_length=100)
    correct_transcription = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Sentence(models.Model):
    name = models.CharField(max_length=100)
    correct_transcription = models.CharField(max_length=255)

    def __str__(self):
        return self.name
