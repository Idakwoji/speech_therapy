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
from .models import CatLev0, CatLev1, CatLev2, CatLev3, ThemeName, PageName, PageBlock, HumorEnGeluiden, FysiekeGedrag, MuziekEnGeluid, TafelDekken, PersoonlijkenBezittelijkVoornaamwoord, Gevaarlijk, OmgaanMetSpullen, TandenVerzorgen, VerbondenheidEnGevoelens,Gevoel,Ontbijten, Tekenen, AanUitkleding, Groente, OpDeBeurt, Tellen, Afscheid,Groeten,OpReis,Tijd,AlgemeenMensen,Gymnastiek,OpenEnDichtDoen,Toeval,AvondEten,HaarVerzorgen,Overig,TuinEnPark,Badkamer,HebbenEnDelen,Personen,Uitjes,Bal,Herfst, Planten,Vergelijken, BelangrijkeWoordjes,Huis,PoepenEnPlassen,Verjaardag,Boerderij,HuisWerken,Rekenen,Voortuigen,BoodschappenDoen,Huisdieren,RichtingDeWeg,Vormen,Bos,Kerst,RollenspelEnSprookjes,Vraagwoorden, Buiten,Kleding,Ruimte,Vuur,Communiceren,KleineDiertjes,SamenAktiviteiten,Wassen,Denken,Kleuren,Schoen,Water,Dieren,Knutselen, Schrijven, Weer, Dierentuin,Koken,Sinterklaas,WegwijsInDeGroep,Doen,KopjesEnBakers,Smaken,Welkom, Drankjes,Kringroutines,Snoep,Winter,Drinken,Kruipen,Speelgoed,WinterKleding,Emotie,Lente,Speeltuin,ZeeSwembad,Eruitzien,Lichaamsdelen,Spelen,Ziek,Eten,Lunch,SpelenEnWerken,Zintuigen,Familie,MensenEnRelaties,Spelletje,Zomer,Fruit,Meten,StraatEnVerkeer

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


    


category_levels = [CatLev0, CatLev1, CatLev2, CatLev3]
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
            'video': ('.mp4',)
        }
#to check if table can be used or not
@csrf_exempt
def check_theme_existence(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        theme_name = data.get('theme_name')

        # Query the ThemeName model to check if the specified theme_name exists
        theme_exists = ThemeName.objects.filter(theme_name=theme_name).exists()

        # Prepare the response based on whether the theme_name exists or not
        response_data = {'exists': theme_exists}
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def perform_category_search(request):
    # Implement the logic to search all category levels for the query
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get("query")

        if query is not None:  # Check if query is not None
            for model in category_levels:
                match = model.objects.filter(name__icontains=query).first()
                if match:
                    return fetch_subcategories_or_data(match, model)
            return JsonResponse({'message': 'No matching category found.'})
        else:
            return JsonResponse({'message': 'Query parameter is None.'}, status=400)

def fetch_subcategories_or_data(match, model):
    next_level_query = None
    response_data = {}
    new_level = None 
    # Using the match level to determine the next level's query
    if model == CatLev0:
        next_level_query = CatLev1.objects.filter(cat_lev0=match)
        new_level = "CatLev1"
    elif model == CatLev1:
        next_level_query = CatLev2.objects.filter(cat_lev1=match)
        new_level = "CatLev2"
    elif model == CatLev2:
        next_level_query = CatLev3.objects.filter(cat_lev2=match)
        new_level = "CatLev3"

    if next_level_query and next_level_query.exists():
        response_data["category_level"] = new_level
        response_data["categories"] = list(next_level_query.values('id', 'name'))
        return JsonResponse(response_data, safe=False)
    
    # If no subcategories found, find the related data table
    return fetch_data_table_entries(match)

@csrf_exempt
def fetch_next_subcategories_or_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        word_id = data.get('id')
        model = data.get("category_level")
        next_level_query = None
        new_level= None
        match = None
        response_data = {}
        # Using the match level to determine the next level's query
        if model == "CatLev0":
            match = CatLev0.objects.get(id=word_id)
            next_level_query = CatLev1.objects.filter(cat_lev0=match)
            new_level = "CatLev1"
            # If no subcategories found, find the related data table
            if not next_level_query:
                return fetch_data_table_entries(match)
            
        elif model == "CatLev1":
            match = CatLev1.objects.get(id=word_id)
            next_level_query = CatLev2.objects.filter(cat_lev1=match)
            new_level = "CatLev2"
            # If no subcategories found, find the related data table
            if not next_level_query:
                return fetch_data_table_entries(match)
            
        elif model == "CatLev2":
            match = CatLev2.objects.get(id=word_id)
            next_level_query = CatLev3.objects.filter(cat_lev2=match)
            new_level = "CatLev3"
            # If no subcategories found, find the related data table
            if not next_level_query:
                return fetch_data_table_entries(match)
            
        if next_level_query and next_level_query.exists():
            response_data["category_level"] = new_level
            response_data["categories"] = list(next_level_query.values('id', 'name'))
            return JsonResponse(response_data, safe=False)
        
        

def collect_category_ids(match):
    category_ids = {'cat_lev0': None, 'cat_lev1': None, 'cat_lev2': None, 'cat_lev3': None}

    # Traverse back from CatLev3 to CatLev0, collecting IDs
    if isinstance(match, CatLev3):
        category_ids['cat_lev3'] = match.id
        match = match.cat_lev2
    if isinstance(match, CatLev2):
        category_ids['cat_lev2'] = match.id
        match = match.cat_lev1
    if isinstance(match, CatLev1):
        category_ids['cat_lev1'] = match.id
        match = match.cat_lev0
    if isinstance(match, CatLev0):
        category_ids['cat_lev0'] = match.id

    return category_ids

def find_matching_data_table(category_ids):
    # Assuming a list of your data table models and a generic way to access their first row's category information
   # Replace with your actual data table models
    for model in model_classes:
        first_row = model.objects.first()
        if first_row:
            # Assuming each model has a method or properties to access its category level IDs
            if (first_row.cat_lev0 == category_ids['cat_lev0'] and
                first_row.cat_lev1 == category_ids['cat_lev1'] and
                first_row.cat_lev2 == category_ids['cat_lev2'] and
                first_row.cat_lev3 == category_ids['cat_lev3']):
                return model  # Found the matching table
    
    return None  # No matching table found

def fetch_data_table_entries(match):
    # Collect category IDs
    category_ids = collect_category_ids(match)
    
    # Find the matching data table
    matching_table = find_matching_data_table(category_ids)
    
    if matching_table:
        results = []
        # Logic to return data from the matching table
        # For example, return all entries from the matching table as a JsonResponse
        entries = matching_table.objects.all().values('id', 'name', "url")
        table_name = matching_table._meta.db_table
        for entry in entries:
            result = {"id": entry["id"], 'name': entry['name'], 'table_name': table_name}
            url = entry['url']
            for option, extensions in options.items():
                for ext in extensions:
                    file_path = os.path.join(url, f"{url}{ext}")
                    if os.path.exists(file_path):
                        result[option] = file_path
            results.append(result)
        return JsonResponse({"words_data": results}, safe=False)
    
    # Handle case where no matching table is found
    return JsonResponse({'message': 'No matching data table found.'})


#use dynamic search to find words (create theme page for admin and therapist)
# @csrf_exempt
# def dynamic_search(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)  # Assuming the data is sent in the POST form data
#         query = data.get('query')
#         if query:
#             results = []
#             for model_class in model_classes:
#                 table_name = model_class._meta.db_table
#                 table_result = model_class.objects.filter(
#                     Q(name__istartswith=query) | Q(name__icontains=f" {query}")
#                 ).values('name', 'url')
#                 # Check if there are matching names before appending to results
#                 if table_result.exists():
#                     for entry in table_result:
#                         result = {'name': entry['name'], 'table_name': table_name}
#                         url = entry['url']
#                         for option, extensions in options.items():
#                             for ext in extensions:
#                                 file_path = os.path.join(url, f"{url}{ext}")
#                                 if os.path.exists(file_path):
#                                     result[option] = file_path
#                         results.append(result)
#             return JsonResponse({'results': results})

#     return JsonResponse({'error': 'Invalid request method or missing query'}, status=400)
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

@csrf_exempt
def save_theme(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        theme_name_value = data.get('theme_name')
        theme = ThemeName.objects.create(theme_name=theme_name_value)
        if theme:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'There was an issue saving the theme'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def save_page(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Assuming JSON data is sent in the request body
        theme_name_value = data.get("theme_name")
        page_name_value = data.get('page_name')
        columns = data.get("columns")
        blocks_data = data.get('blocks', [])

        try:
            with transaction.atomic():
                theme = ThemeName.objects.get(theme_name=theme_name_value)
                # Create PageName
                page = PageName.objects.create(page_name=page_name_value, block_column = columns, theme_name=theme)

                # Create PageBlock instances and add them to the PageName's blocks field
                for block_data in blocks_data:
                    name = block_data.get('name')
                    table_name = block_data.get('table_name')
                    image = block_data.get('image')
                    audio = block_data.get("audio")
                    video = block_data.get("video")

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
                        PageBlock.objects.create(name=name, url=url, image=image, audio=audio, video=video, page_name=page)

                return JsonResponse({'success': True})

        except Exception as e:
            # Handle exceptions or log errors
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def delete_theme(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        theme_id = data.get('id')

        try:
            with transaction.atomic():
                # Delete ThemeName and its related records
                ThemeName.objects.filter(id=theme_id).delete()

                return JsonResponse({'success': True})

        except Exception as e:
            # Handle exceptions or log errors
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_page(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        page_id = data.get('id')  # The unique ID of the page to be deleted

        try:
            with transaction.atomic():
                # Attempt to find and delete the specified page
                page_to_delete = PageName.objects.get(id=page_id).delete()

                return JsonResponse({'success': True})

        except PageName.DoesNotExist:
            return JsonResponse({'error': f'Page with id {page_id} does not exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_blocks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        page_id = data.get('id')
        blocks_to_delete = data.get('blocks', [])  # Assume this is a list of block IDs to delete

        try:
            with transaction.atomic():
                # Delete specified blocks for the page
                for block_id in blocks_to_delete:
                    try:
                        block = PageBlock.objects.get(id=block_id, page_name_id=page_id)
                        block.delete()
                    except PageBlock.DoesNotExist:
                        # If a specific block doesn't exist, you can choose to ignore or log this
                        continue  # Or log.error("Block with id {block_id} not found.")

                return JsonResponse({'success': True})

        except Exception as e:
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

@csrf_exempt
def fetch_all_themes(request):
    if request.method == 'GET':
        # Fetch all available theme details from the ThemeName table
        all_themes = ThemeName.objects.values('id', 'theme_name')
        return JsonResponse({'themes': list(all_themes)})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def fetch_theme_pages(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        theme_id = data.get('id')
        try:
            # Fetch the ThemeName instance
            theme = ThemeName.objects.get(id=theme_id)
        except ThemeName.DoesNotExist:
            return JsonResponse({'error': f'Theme with id {theme_id} does not exist'}, status=404)

        # Fetch pages with IDs associated with the specified ThemeName
        pages = theme.pages.all().values('id', 'page_name', 'block_column')
        theme_pages = list(pages)
        theme_name = theme.theme_name
        
        # Include the name of the theme in the response
        response_data = {
            'theme_name': theme_name,
            'pages': theme_pages
        }
        
        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def fetch_page_blocks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        page_id = data.get('id')
        try:
            # Fetch the PageName instance
            page = PageName.objects.get(id=page_id)
        except PageName.DoesNotExist:
            return JsonResponse({'error': f'Page with id {page_id} does not exist'}, status=404)

        # Fetch all blocks with IDs associated with the specified PageName
        blocks = page.blocks.all().values('id', 'name', 'url', 'image', 'audio', 'video')
        page_name = page.page_name  # Retrieve the page_name once

        results = []
        for block in blocks:
            result = {
                'id': block['id'],
                'name': block['name'],
                'image': block['image'],
                'audio': block['audio'],
                'video': block['video'],
            }
            url = block['url']
            for option, extensions in options.items():
                for ext in extensions:
                    file_path = os.path.join(url, f"{url}{ext}")
                    if os.path.exists(file_path):
                        result[option] = file_path
            results.append(result)

        # Include the page_name in the final response
        response_data = {'page_name': page_name, 'blocks': results}
        return JsonResponse(response_data)
    
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
