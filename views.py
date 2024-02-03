from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import FileResponse
import json
import base64
import os
from random import sample
from .models import Word, Sentence
#from .compare import find_mistakes

# Dictionary to store correct transcriptions
#correct_transcriptions = {}
# Fetch all audio instances from the database once
all_words = Word.objects.all()
all_sentences = Sentence.objects.all()

@csrf_exempt
def get_random_words(request):
 # Randomly select 10 audio instances
    audio_instances_for_response = sample(list(all_words), min(10, len(all_words)))
    # Prepare data for response and store correct transcriptions
    audio_data = []
    for audio_instance in audio_instances_for_response:
        audio_id = audio_instance.id
        audio_name = audio_instance.name
        correct_transcription = audio_instance.correct_transcription
        audio_data.append({
            'id':audio_id,
            'name': audio_name,
            })
        cache.set(audio_name, correct_transcription)
        #print(audio_data)
    return JsonResponse(audio_data, safe=False)

@csrf_exempt
def get_random_sentences(request):
    # Randomly select 10 audio instances
    audio_instances_for_response = sample(list(all_sentences), min(10, len(all_sentences)))
    # Prepare data for response and store correct transcriptions
    audio_data = []
    for audio_instance in audio_instances_for_response:
        audio_id = audio_instance.id
        audio_name = audio_instance.name
        correct_transcription = audio_instance.correct_transcription
        audio_data.append({
            'id':audio_id,
            'name': audio_name,
            })
        cache.set(audio_name, correct_transcription)
        #print(audio_data)
    return JsonResponse(audio_data, safe=False)

@csrf_exempt
def get_audio(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            audio_name = json_data.get('name')
            file_formats = ['.mp3', '.wav']
            audio_file_path = None
            for file_format in file_formats:
                potential_path1 = f'media/words/{audio_name}{file_format}'
                potential_path2 = f'media/sentences/{audio_name}{file_format}'
                if os.path.exists(potential_path1):
                    audio_file_path = potential_path1
                    break
                elif os.path.exists(potential_path2):
                    audio_file_path = potential_path2
                    break
            # Read the audio file and convert it to base64
            if audio_file_path:
                # Read the audio file and convert it to base64
                with open(audio_file_path, 'rb') as audio_file:
                    audio = audio_file.read()
                    response = HttpResponse(audio, content_type='audio/mpeg')
                    return response
            else:
                return HttpResponse("Audio file not found", status=404)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON payload", status=400)
        
@csrf_exempt
def compare_sentences(request):
    if request.method == 'POST':
        try:
            
            # Access audio data from the form data
            audio_data = request.FILES['audio']
            # Access name from the form data
            name = request.POST.get('name')
            #print(f"file name: {name}")
            #print(audio_data)

            if not audio_data:
                return JsonResponse({'error': 'Audio data not found in the request'}, status=400)

            file_content = audio_data.read()
            
            # Send the audio file content to the model server for transcription
            transcription_url = 'http://192.168.178.12:5001/transcribe'
            headers = {'Content-Type': 'application/octet-stream'}
            params = {"name": name}
            response = requests.post(transcription_url, data=file_content, headers=headers, params=params)
            result = response.json()
            transcribed_sentence = result.get('transcription', '')
            transcribed_sentence = transcribed_sentence.strip().lower()
            transcribed_sentence = transcribed_sentence.replace('.', '')
            #print(f"transcribed sentence: {transcribed_sentence}")

            # Fetch a correct sentence from the database (you need to handle this based on your requirements)
            correct_sentence = cache.get(name)
            #print(f"correct sentence from database: {correct_sentence}")
            correct_sentence = correct_sentence.lower()
            # Compare sentences and find missing phonemes
            #mistakes = find_mistakes(correct_sentence, transcribed_sentence)
            #print(mistakes)

            # Return the results to the frontend
            response_data = {
                'correct_sentence': correct_sentence,
                'transcribed_sentence': transcribed_sentence,
                #'missing_phonemes': mistakes,
            }
            #print(response_data)
            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': f'Error processing the request: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
