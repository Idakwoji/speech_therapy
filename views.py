from django.http import JsonResponse, HttpResponse,StreamingHttpResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import connections, transaction
import requests
from django.http import FileResponse
from io import BytesIO
import json
import base64
import os
#import zipfile
import mimetypes
from random import sample
from .models import ThemeName, PageName, PageBlock, HumorEnGeluiden, FysiekeGedrag, MuziekEnGeluid, TafelDekken, PersoonlijkenBezittelijkVoornaamwoord, Gevaarlijk, OmgaanMetSpullen, TandenVerzorgen, VerbondenheidEnGevoelens,Gevoel,Ontbijten, Tekenen, AanUitkleding, Groente, OpDeBeurt, Tellen, Afscheid,Groeten,OpReis,Tijd,AlgemeenMensen,Gymnastiek,OpenEnDichtDoen,Toeval,AvondEten,HaarVerzorgen,Overig,TuinEnPark,Badkamer,HebbenEnDelen,Personen,Uitjes,Bal,Herfst, Planten,Vergelijken, BelangrijkeWoordjes,Huis,PoepenEnPlassen,Verjaardag,Boerderij,HuisWerken,Rekenen,Voortuigen,BoodschappenDoen,Huisdieren,RichtingDeWeg,Vormen,Bos,Kerst,RollenspelEnSprookjes,Vraagwoorden, Buiten,Kleding,Ruimte,Vuur,Communiceren,KleineDiertjes,SamenAktiviteiten,Wassen,Denken,Kleuren,Schoen,Water,Dieren,Knutselen, Schrijven, Weer, Dierentuin,Koken,Sinterklaas,WegwijsInDeGroep,Doen,KopjesEnBakers,Smaken,Welkom, Drankjes,Kringroutines,Snoep,Winter,Drinken,Kruipen,Speelgoed,WinterKleding,Emotie,Lente,Speeltuin,ZeeSwembad,Eruitzien,Lichaamsdelen,Spelen,Ziek,Eten,Lunch,SpelenEnWerken,Zintuigen,Familie,MensenEnRelaties,Spelletje,Zomer,Fruit,Meten,StraatEnVerkeer

#set user sessions
def set_session(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Get the username from the POST data
        request.session['username'] = username
        return HttpResponse('Session data set.')
    else:
        return HttpResponse('Invalid request method', status=400)

def get_session(request):
    username = request.session.get('username', 'DefaultUsername')
    return HttpResponse(f'Username from session: {username}')


    



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

options = {
            'image': ('.jpeg', '.jpg', '.png', '.svg', '.gif'),
            'audio': ('.mp3', '.wav'),
            'video': ('.mp4')
        }
#to check if table can be used or not
def check_theme_existence(request):
    if request.method == 'POST':
        data = request.json()
        theme_name = data.get('theme_name')

        # Check if the specified theme_name exists in the "Theme Names" table of the public_templates database
        with connections['public_templates'].cursor() as cursor:
            cursor.execute(
                "SELECT theme_name FROM public.\"Theme Names\" WHERE theme_name = %s",
                [theme_name]
            )
            result = cursor.fetchone()

        # Prepare the response based on whether the theme_name exists or not
        response_data = {'exists': False}
        if result:
            response_data['exists'] = True
            
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

#use dynamic search to find words (create theme page for admin and therapist)
def dynamic_search(request):
    if request.method == 'POST':
        data = request.json()  # Assuming the data is sent in the POST form data
        query = data.get('query')
        if query:
            results = []
            for model_class in model_classes:
                table_name = model_class._meta.db_table
                table_result = model_class.objects.filter(
                    Q(name__istartswith=query) | Q(name__icontains=f" {query}")
                ).values('name', 'url')
                # Check if there are matching names before appending to results
                if table_result.exists():
                    for entry in table_result:
                        result = {'name': entry['name'], 'table_name': table_name}
                        url = entry['url']
                        for option, extensions in options.items():
                            for ext in extensions:
                                file_path = os.path.join(url, f"{url}{ext}")
                                if os.path.exists(file_path):
                                    result[option] = file_path
                        results.append(result)
            return JsonResponse({'results': results})

    return JsonResponse({'error': 'Invalid request method or missing query'}, status=400)
#find words by going through all the tables (create theme page for admin and therapist)
# def get_table_names(request):
#     table_names = [model_class._meta.db_table for model_class in model_classes]
#     return JsonResponse({'table_names': table_names})

# #get all the words for the selected table
# def get_table_data(request):
#     if request.method == 'POST':
#         table_name = request.POST.get('table_name')
#         model_class = None
#         for potential_model in model_classes:
#             if potential_model._meta.db_table == table_name:
#                 model_class = potential_model
#                 break

#         if model_class:
#             table_data = model_class.objects.values('name')
#             return JsonResponse({'table_data': list(table_data)})

#         return JsonResponse({'error': 'Table not found'})

#save the page that was created to the public templates database
def save_theme(request):
    if request.method == 'POST':
        data = request.json()
        theme_name_value = data.get('theme_name')
        theme = ThemeName.objects.create(theme_name=theme_name_value)
        if theme:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'There was an issue saving the theme'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def save_page(request):
    if request.method == 'POST':
        data = request.json()  # Assuming JSON data is sent in the request body
        theme_name = data.get("theme_name")
        page_name_value = data.get('page_name')
        rows = data.get("rows")
        columns = data.get("columns")
        blocks_data = data.get('blocks', [])

        try:
            with transaction.atomic():
                # Create PageName
                page = PageName.objects.create(page_name=page_name_value, block_row = rows, block_column = columns, theme_name=theme_name)

                # Create PageBlock instances and add them to the PageName's blocks field
                for block_data in blocks_data:
                    name = block_data.get('name')
                    table_name = block_data.get('table_name')
                    option = block_data.get('option')

                    # Dynamically get the model class based on table_name
                    model_class = None
                    for potential_model in model_classes:
                        if potential_model._meta.db_table == table_name:
                            model_class = potential_model
                            break

                    if model_class:
                        # Query the database for the URL based on name
                        try:
                            url = model_class.objects.get(name=name).url
                        except model_class.DoesNotExist:
                            return JsonResponse({'error': 'File not found'}, status=404)

                        # Create a new PageBlock instance
                        PageBlock.objects.create(name=name, url=url, option=option, page_name=page)

                return JsonResponse({'success': True})

        except Exception as e:
            # Handle exceptions or log errors
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


#fetch public themas (theme names or page names corresponding to the names of all the current tables in the database) 

# def fetch_all_pages(request):
#     if request.method == 'GET':
#         # Fetch all available pages (table names) from the public_templates database
#         with connections['public_templates'].cursor() as cursor:
#             cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
#             all_pages = [row[0] for row in cursor.fetchall()]
#         return JsonResponse({'pages': all_pages})

#     return JsonResponse({'error': 'Invalid request method'}, status=400)


def fetch_all_themes(request):
    if request.method == 'GET':
        #fetch all available theme names from the ThemeName table
        all_themes = ThemeName.objects.values_list('theme_name', flat=True)
        return JsonResponse({'themes': list(all_themes)})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def fetch_theme_pages(request):
    if request.method == 'POST':
        data = request.json()
        theme_name = data.get('theme_name')
        try:
            # Fetch the ThemeName instance
            theme = ThemeName.objects.get(theme_name=theme_name)
        except ThemeName.DoesNotExist:
            return JsonResponse({'error': f'Theme with name {theme_name} does not exist'}, status=404)
        pages =theme.pages.all().values("page_name", "block_row", "block_column")
        theme_pages = list(pages)
        return JsonResponse({'pages': theme_pages})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def fetch_page_blocks(request):
    if request.method == 'POST':
        data = request.json()
        page_name = data.get('page_name')

        try:
            # Fetch the PageName instance
            page = PageName.objects.get(page_name=page_name)
        except PageName.DoesNotExist:
            return JsonResponse({'error': f'Page with name {page_name} does not exist'}, status=404)

        # Fetch all blocks associated with the specified PageName
        blocks = page.blocks.all().values('name', 'url', 'option')
        results = []
        for block in blocks:
            result = {'name': block['name'], 'option': block['option']}
            url = block['url']
            for option, extensions in options.items():
                for ext in extensions:
                    file_path = os.path.join(url, f"{url}{ext}")
                    if os.path.exists(file_path):
                        result[option] = file_path
            results.append(result)
        return JsonResponse({'blocks': results})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

#problem with two databases, which to fetch from on the two different scenarios??????????????
# def get_image(request):
#     if request.method == "POST":
#         data = request.json()
#         name = data.get("name")
#         try:
#             page_block = PageBlock.objects.get(name=name)
#         except PageBlock.DoesNotExist:
#             return JsonResponse({'error': f'Block with name {name} does not exist'}, status=404)

#         url = page_block.url

#         option = options.get("image_only")  # Fix typo: square brackets instead of parentheses

#         file_path = None
#         for ext in option:
#             path = os.path.join(url, f"{name}{ext}")
#             if os.path.exists(path):
#                 file_path = path
#                 break

#         if file_path:
#             with open(file_path, 'rb') as image_file:
#                 image = image_file.read()
#                 response = HttpResponse(image, content_type='image/*')  # Fix content_type to 'image/*'
#                 return response
#         else:
#             return HttpResponse("Image file not found", status=404)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)
                
#fetch audio
# def get_audio(request):
#     if request.method == "POST":
#         data = request.json()
#         name = data.get("name")
#         try:
#             page_block = PageBlock.objects.get(name=name)
#         except PageBlock.DoesNotExist:
#             return JsonResponse({'error': f'Block with name {name} does not exist'}, status=404)

#         url = page_block.url

#         option = options.get("audio_only")

#         file_path = None
#         for ext in option:
#             path = os.path.join(url, f"{name}{ext}")
#             if os.path.exists(path):
#                 file_path = path
#                 break

#         if file_path:
#             with open(file_path, 'rb') as audio_file:
#                 audio = audio_file.read()
#                 response = HttpResponse(audio, content_type='audio/*')
#                 return response
#         else:
#             return HttpResponse("Audio file not found", status=404)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)

# #fetch video
# def get_video(request):
#     if request.method == "POST":
#         data = request.json()
#         name = data.get("name")
#         try:
#             page_block = PageBlock.objects.get(name=name)
#         except PageBlock.DoesNotExist:
#             return JsonResponse({'error': f'Block with name {name} does not exist'}, status=404)

#         url = page_block.url

#         option = options.get("video_only")

#         file_path = None
#         for ext in option:
#             path = os.path.join(url, f"{name}{ext}")
#             if os.path.exists(path):
#                 file_path = path
#                 break

#         if file_path:
#             with open(file_path, 'rb') as video_file:
#                 video = video_file.read()
#                 response = HttpResponse(video, content_type='video/mp4')
#                 return response
#         else:
#             return HttpResponse("Video file not found", status=404)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)

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
