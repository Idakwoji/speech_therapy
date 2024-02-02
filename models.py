from django.db import models

class Word(models.Model):
    name = models.CharField(max_length=255)
    correct_transcription = models.CharField(max_length=255)

    class Meta:
        db_table = 'words'

    def __str__(self):
        return f'{self.id}: {self.name}'

class Sentence(models.Model):
    name = models.CharField(max_length=255)
    correct_transcription = models.CharField(max_length=255)

    class Meta:
        db_table = 'sentences'

    def __str__(self):
        return f'{self.id}: {self.name}'

