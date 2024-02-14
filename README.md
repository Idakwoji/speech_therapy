Building a Robust dutch speech therapy website

#### API DOCUMENTATION

###### ADMIN DASHBOARD
Includes various admin functionalities listed out below:

1. The thema page will fetch all the currently existing (public) themes in the database. It would be fetching the names of all the pages that have been created and saved in a list (array) as a json response since it contains just text. This can be iterated through to display the name of each theme in the themes page. It would return an empty list if there are no themes so the front end should handle the empty list and not display anything. It strictly expects a GET request.
- Endpoint: api/fetch_all_pages
- the name of the pages is tagged 'pages' in the response.

2. *****edited***** When any of the theme pages are clicked (existing themes I mean), It should fetch all the blocks under that theme page. It would be returning the name of the words for each block, as well as the file(s) associated with it. The data structure is a bit tricky so beware. It is going to be a HTTP response since it contains files. The structure looks like this:
 {
            'page_name': page_name,
            'blocks': [{'name': name_of_block1, 'associated_files': {"files": the_zip_files_for_the_block, "content_type":'application/zip'}}, {'name': name_ofblock2, 'associated_files': {"files": the_zip_files_for_the_block, "content_type":'application/zip'}}, etc etc],
        }
The associated files contain a zip file that has the file (or files) associated with that block. remember that when the blocks were being created, there were options to choose which file or files to add to the block. If its only image, only an image file will be in the zip file, if its all three, then all three (image, audio, and video) will be in the zip file. Like I said, the structure us a but tricky. The value of 'associated_files' key is also another dictionary that includes the actual zip file itself and its content type. This is so that you can get the content type from the response too. So basically, the response is a HTTPResponse Dictionary (I dont know what you call dictionaries, I mean the data structure with the curly braces "{}"), and this dictionary contains two keys 'page_name', and 'blocks'. I dont think you need the page name  again anyways because I already sent it in the previous request, but wont hurt. The 'blocks' key is a list of dictionaries and each dictionay represents one block on the page. each block dictinary has two keys "name" for the name of the block (which you might not nee dot display but I'm not sure I'll ask Oga), and the second key is the "associated files" that has another dictionary like I described above. It strictly expects a POST request with the name of the page accompanying it.
- Endpoint: api/fetch_page_blocks

2. This has been edited to just return a list of dictionaries with the "name" and "option" of each block in each dictionary. The "option" would help you map which of the blocks has what option. So you can gray out the unrequired options.
- Endpoint: api/fetch_page_blocks

3. When a new page is to be created, The first thing is to type in the name of the page. We want to do a check to see if that page name is available or not. The response is a Json response with the key "exists" set to a True if the name exists (meaning you shouldnt allow them use it) and False if the name does not exist meaning they can use it. It strictly expects a POST request with the page name that was typed accompanying it.
- Endpoint: api/check_page_existence

4. Once the name of the page is set and the blocks are created, the user should be able to interact with each block that leads to another page. That new page allows them to do a dynamic search or manually check for the words on the database. The dynamic search expects a query (that contains the letters or word that has been typed), and returns a Json file that is a list(array) under the key "results". This array then consists of a key "table_name" for the table that it was matched from and a "name" key that is a list(array) of all the matching words from that table. The table name is relevant because when any word is selected by the user, I will need you to send that word, the table it was found, and the "option" that was selected so I can fetch you the files as shown in 7 below.
- Endpoint: api/dynamic_search

5. If the person chooses to find the words manually, we first of all get the names of all the tables in the database (about 103 right now so they should be able to scroll through). The request to get all the names of the tables would return a list (array) of the names of all the tables in a Json respones under the key "table_names".
- Endpoint: api/get_table_names

6. Once the user clicks on any of the table names, it should send a request to fetch all the words under that table name. The endpoint strictly espects a POST request with the name of the table that was clicked. It would return a JSON response with a list (array) of all the words using the key "table_data".
- Endpoint: api/get_table_data

7. ******I have removed the fetch_files endpoint totally****** once the word has been gotten from either 4 or 6, I expect that the user would be allowed to choose which file they want to add to the block "Image only, audio only, video only, and all_options" Once they have chosen what they want, a request should then be sent to fetch the files for them. The endpoint strictly expects a POST request with the following info accompanying: the "name" of the word, the "table_name" the word belongs to, and the "option" they selected. I expect the options to be tagged either "image_only", "audio_only", "video_only", or "all_options". The endpoint will be returning a HTTP response carrying a zip file that containes the file or (files for "all options"). The name of the file should be "matching_files.zip".  Remember that this is just for displaying the image or audio or video after the admin or client selects the word. (I know, all this stress just to achieve that).
- Endpoint: api/fetch_files


7. I included three endpoints to fetch images, audios and videos. these endpoints can be accessed from the three buttons to view image, play audio, or play video. They all return HTTPResponse byte files. The issue however is that the endpoints are designed to access the pages database, so would not be able to fetch anything while the blocks are being created. we should look at either creating new endpoints for those, or some other solution. We basically have to think of how to get the files for the person creating the blocks to view the onmes they have created. I dont know if it is wise to save the blocks as they are created instead of having a "save page button", but that may be problematic too. 
- Endpoint: api/get_image
- Endpoint: api/get_audio
- Endpoint: api/get_video


8. after all the blocks have been chosen the page can be saved. I strictly expect a POST request with the data structure as a JSON with two keys: "thema_name" for the name of the page, and "blocks" which will be a list (array) that contains all the blocks. each block should be a dictionary that has the keys "name" for the name of the word, "table_name" for the table the word was chosen from, and "option" for the option of file selected by the user. I'll then save the block and return a JSON response with "success" = TRUE if it was successfully saved.
- Endpoint: api/save_page