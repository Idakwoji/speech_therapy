from django.http import JsonResponse, HttpResponse,StreamingHttpResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import connections
import requests
from django.http import FileResponse
from io import BytesIO
import json
import base64
import os
import zipfile
import mimetypes
from random import sample
from .models import PageBlock, HumorEnGeluiden, FysiekeGedrag, MuziekEnGeluid, TafelDekken, PersoonlijkenBezittelijkVoornaamwoord, Gevaarlijk, OmgaanMetSpullen, TandenVerzorgen, VerbondenheidEnGevoelens,Gevoel,Ontbijten, Tekenen, AanUitkleding, Groente, OpDeBeurt, Tellen, Afscheid,Groeten,OpReis,Tijd,AlgemeenMensen,Gymnastiek,OpenEnDichtDoen,Toeval,AvondEten,HaarVerzorgen,Overig,TuinEnPark,Badkamer,HebbenEnDelen,Personen,Uitjes,Bal,Herfst, Planten,Vergelijken, BelangrijkeWoordjes,Huis,PoepenEnPlassen,Verjaardag,Boerderij,HuisWerken,Rekenen,Voortuigen,BoodschappenDoen,Huisdieren,RichtingDeWeg,Vormen,Bos,Kerst,RollenspelEnSprookjes,Vraagwoorden, Buiten,Kleding,Ruimte,Vuur,Communiceren,KleineDiertjes,SamenAktiviteiten,Wassen,Denken,Kleuren,Schoen,Water,Dieren,Knutselen, Schrijven, Weer, Dierentuin,Koken,Sinterklaas,WegwijsInDeGroep,Doen,KopjesEnBakers,Smaken,Welkom, Drankjes,Kringroutines,Snoep,Winter,Drinken,Kruipen,Speelgoed,WinterKleding,Emotie,Lente,Speeltuin,ZeeSwembad,Eruitzien,Lichaamsdelen,Spelen,Ziek,Eten,Lunch,SpelenEnWerken,Zintuigen,Familie,MensenEnRelaties,Spelletje,Zomer,Fruit,Meten,StraatEnVerkeer
#from .compare import find_mistakes

# Dictionary to store correct transcriptions
#correct_transcriptions = {}
# Fetch all audio instances from the database once
#all_words = Word.objects.all()
#all_sentences = Sentence.objects.all()

# @csrf_exempt
# def get_therapist_profile(request):
#     #implemant a code to fetch the profile of the therapist
#     #return details that will be displayed on the profile
    
# @csrf_exempt
# def get_client_profile(request):
#     #implement a code to fetch the client profile from the database
#     #return client details that will be displayed on the profile
    
# @csrf_exempt
# def get_word(request):
    
#@csrf_exempt
#def get_random_words(request):
 # Randomly select 10 audio instances
 #   audio_instances_for_response = sample(list(all_words), min(10, len(all_words)))
    # # Prepare data for response and store correct transcriptions
    # audio_data = []
    # for audio_instance in audio_instances_for_response:
    #     audio_id = audio_instance.id
    #     audio_name = audio_instance.name
    #     correct_transcription = audio_instance.correct_transcription
    #     audio_data.append({
    #         'id':audio_id,
    #         'name': audio_name,
    #         })
    #     cache.set(audio_name, correct_transcription)
    #     #print(audio_data)
    # return JsonResponse(audio_data, safe=False)

# @csrf_exempt
# def get_random_sentences(request):
#     # Randomly select 10 audio instances
#     audio_instances_for_response = sample(list(all_sentences), min(10, len(all_sentences)))
#     # Prepare data for response and store correct transcriptions
#     audio_data = []
#     for audio_instance in audio_instances_for_response:
#         audio_id = audio_instance.id
#         audio_name = audio_instance.name
#         correct_transcription = audio_instance.correct_transcription
#         audio_data.append({
#             'id':audio_id,
#             'name': audio_name,
#             })
#         cache.set(audio_name, correct_transcription)
#         #print(audio_data)
#     return JsonResponse(audio_data, safe=False)

#initialize all database model classes in the existing words database
model_classes = [
            HumorEnGeluiden, FysiekeGedrag, MuziekEnGeluid, TafelDekken,
            PersoonlijkenBezittelijkVoornaamwoord, Gevaarlijk, OmgaanMetSpullen,
            TandenVerzorgen, VerbondenheidEnGevoelens, Gevoel, Ontbijten, Tekenen,
            AanUitkleding, Groente, OpDeBeurt, Tellen, Afscheid, Groeten, OpReis, Tijd,
            AlgemeenMensen, Gymnastiek, OpenEnDichtDoen, Toeval, AvondEten, HaarVerzorgen,
            Overig, TuinEnPark, Badkamer, HebbenEnDelen, Personen, Uitjes, Bal, Herfst,
            Planten, Vergelijken, BelangrijkeWoordjes, Huis, PoepenEnPlassen, Verjaardag,
            Boerderij, HuisWerken, Rekenen, Voortuigen, BoodschappenDoen, Huisdieren,
            RichtingDeWeg, Vormen, Bos, Kerst, RollenspelEnSprookjes, Vraagwoorden, Buiten,
            Kleding, Ruimte, Vuur, Communiceren, KleineDiertjes, SamenAktiviteiten, Wassen,
            Denken, Kleuren, Schoen, Water, Dieren, Knutselen, Schrijven, Weer, Dierentuin,
            Koken, Sinterklaas, WegwijsInDeGroep, Doen, KopjesEnBakers, Smaken, Welkom,
            Drankjes, Kringroutines, Snoep, Winter, Drinken, Kruipen, Speelgoed, WinterKleding,
            Emotie, Lente, Speeltuin, ZeeSwembad, Eruitzien, Lichaamsdelen, Spelen, Ziek, Eten,
            Lunch, SpelenEnWerken, Zintuigen, Familie, MensenEnRelaties, Spelletje, Zomer, Fruit,
            Meten, StraatEnVerkeer
        ]

#to check if table can be used or not
def check_table_existence(request, page_name):
    if request.method == 'GET':
        # Check if the provided page_name exists as a table in the public_templates database
        with connections['public_templates'].cursor() as cursor:
            cursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s",
                [page_name]
            )
            result = cursor.fetchone()

        # Prepare the response based on whether the table exists or not
        response_data = {'exists': False}
        if result:
            response_data['exists'] = True

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

#use dynamic search to find words (create theme page for admin and therapist)
def dynamic_search(request, query):
    results = []

    for model_class in model_classes:
        table_name = model_class._meta.db_table
        table_results = model_class.objects.filter(
            Q(name__istartswith=query) | Q(name__icontains=f" {query}")
        ).values('name', 'url')

        results.extend(list(table_results))

    return JsonResponse({'results': results})

#find words by going through all the tables (create theme page for admin and therapist)
def get_table_names(request):
    table_names = [model_class._meta.db_table for model_class in model_classes]
    return JsonResponse({'table_names': table_names})

#get all the words for the selected table
def get_table_data(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        model_class = None
        for potential_model in model_classes:
            if potential_model._meta.db_table == table_name:
                model_class = potential_model
                break

        if model_class:
            table_data = model_class.objects.values('name')
            return JsonResponse({'table_data': list(table_data)})

        return JsonResponse({'error': 'Table not found'})

def generate_zip_stream(matching_files):
    # Create an in-memory ZIP file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for file_path in matching_files:
            # Add each file to the ZIP file
            zipf.write(file_path)

    # Move the buffer's position to the beginning for reading
    zip_buffer.seek(0)
    
    return zip_buffer

#fetch the files to be displayed as the blocks are being created (create theme page for admin and therapist)
def fetch_files(request):
    if request.method == 'POST':
        data = request.json()  # Assuming JSON data is sent in the request body

        name = data.get('name')
        table_name = data.get('table_name')
        option = data.get('option')  # Default to option 0 if not provided

        options = {
            'image_only': ('.jpeg', '.jpg', '.png', '.svg', '.gif'),
            'audio_only': ('.mp3', '.wav'),
            'video_only': ('.mp4'),
            'all_options': ('.jpeg', '.jpg', '.png', '.svg', '.gif', '.mp3', '.wav', '.mp4')
        }

        file_extensions = options.get(option, [])
        matching_files = []

        # Dynamically get the model class based on table_name
        model_class = None
        for potential_model in model_classes:
            if potential_model._meta.db_table == table_name:
                model_class = potential_model
                break

        if model_class:
            # Query the database for the url based on name
            try:
                url = model_class.objects.get(name=name).url
            except model_class.DoesNotExist:
                return JsonResponse({'error': 'File not found'}, status=404)

            for ext in file_extensions:
                #file_path = f"{url}{ext}"
                file_path = os.path.join(url, f"{ext}")
                if os.path.exists(file_path):
                    matching_files.append(file_path)

            if not matching_files:
                return JsonResponse({'error': 'Files not found'}, status=404)

            # Prepare a ZIP archive containing all matching files
            zip_stream = generate_zip_stream(matching_files)
            response = HttpResponse(zip_stream, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename=matching_files.zip'
            return response

    return JsonResponse({'error': 'Invalid request method'}, status=400)

#save the page that was created to the public templates database
def save_page(request):
    if request.method == 'POST':
        data = request.json()  # Assuming JSON data is sent in the request body

        page_name = data.get('thema_name')
        blocks = data.get('blocks', [])

        # Create PageBlocks for each item in the Blocks list
        for block_data in blocks:
            name = block_data.get('name')
            table_name = block_data.get('table_name')
            option = block_data.get('option')

            
            # Fetch the URL from the existing database using table_name and name
            for potential_model in model_classes:
                if potential_model._meta.db_table == table_name:
                    url = potential_model.objects.get(name=name).url
                    break

            # Set the schema for the table
            PageBlock._meta.db_table = page_name

            # Create a new PageBlock
            PageBlock.objects.create(name=name, url=url, option=option)

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


#fetch public themas (theme names or page names corresponding to the names of all the current tables in the database) 


def fetch_all_pages(request):
    if request.method == 'GET':
        # Fetch all available pages (table names) from the public_templates database
        with connections['public_templates'].cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            all_pages = [row[0] for row in cursor.fetchall()]

        return JsonResponse({'pages': all_pages})

    return JsonResponse({'error': 'Invalid request method'}, status=400)



#fetch the page and its blocks based on the table name (page name) that was sent
def fetch_page_blocks(request, page_name):
    if request.method == 'GET':
        # Set the schema for the table
        PageBlock._meta.db_table = page_name

        # Fetch all blocks (rows) from the specified page (table)
        blocks = PageBlock.objects.all().values('name', 'url', 'option')

        # Prepare the response data
        response_data = {
            'page_name': page_name,
            'blocks': [],
        }

        options = {
            'image_only': ('.jpeg', '.jpg', '.png', '.svg', '.gif'),
            'audio_only': ('.mp3', '.wav'),
            'video_only': ('.mp4'),
            'all_options': ('.jpeg', '.jpg', '.png', '.svg', '.gif', '.mp3', '.wav', '.mp4')
        }

        for block in blocks:
            block_data = {'name': block['name'], 'associated_files': []}
            file_extensions = options.get(block['option'], [])
            url = block['url']
            matching_files = []
            for ext in file_extensions:
                file_path = os.path.join(url, f"{ext}")
                if os.path.exists(file_path):
                    matching_files.append(file_path)
                    #block_data['associated_files'].append(file_path)
            zip_stream = generate_zip_stream(matching_files)
            block_data['associated_files'].append({"files": zip_stream, "content_type":'application/zip'})

            response_data['blocks'].append(block_data)

        return HttpResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


# @csrf_exempt
# def get_audio(request):
#     if request.method == "POST":
#         try:
#             json_data = json.loads(request.body.decode('utf-8'))
#             audio_name = json_data.get('name')
#             file_formats = ['.mp3', '.wav']
#             audio_file_path = None
#             for file_format in file_formats:
#                 potential_path1 = f'media/words/{audio_name}{file_format}'
#                 potential_path2 = f'media/sentences/{audio_name}{file_format}'
#                 if os.path.exists(potential_path1):
#                     audio_file_path = potential_path1
#                     break
#                 elif os.path.exists(potential_path2):
#                     audio_file_path = potential_path2
#                     break
#             # Read the audio file and convert it to base64
#             if audio_file_path:
#                 # Read the audio file and convert it to base64
#                 with open(audio_file_path, 'rb') as audio_file:
#                     audio = audio_file.read()
#                     response = HttpResponse(audio, content_type='audio/mpeg')
#                     return response
#             else:
#                 return HttpResponse("Audio file not found", status=404)
#         except json.JSONDecodeError:
#             return HttpResponse("Invalid JSON payload", status=400)
        
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
