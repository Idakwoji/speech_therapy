Building a Robust dutch speech therapy website

#### API DOCUMENTATION

###### ADMIN DASHBOARD
Includes various admin functionalities listed out below:

*New Documentation*
1. Check for existence of a theme: once someone clicks on create new theme, a window should pop up for them to type the name of the theme. I want us to check for the existence of that theme and not allow them proceed if the name exists. If the name does not exist, they can proceed to create the new theme.
- endpoint: /api/check_theme_existence
- ⁠expects a json with one key “theme_name”.
- ⁠returns a JSON with structure: {‘exists’: False} if the page doesn’t exist and True if the page exists.

2. Save theme: This step should come immediately after checking for existence of the theme.
- endpoint: /api/save_theme
- ⁠expects a JSON with key “theme_name”
- ⁠returns a json with key “success” to indicate if theme was saved successfully.

3. Dynamic search: to search for words in a page like we discussed, when the new page is created. I still have to return the table_name to you because I would need that info later to save the urls to the database. 
- endpoint: /api/dynamic_search
- ⁠expects a json with a key “query”
- ⁠returns a JSON with key “results”, whose value is a list of objects(dictionaries). Each dictionary contains the details of the matched words with the keys: ‘name’, ‘table_name’, ‘image’ for image path, ‘audio’ for audio path, ‘video’ for video path.

4. Save page: after all the words they want have been chosen, we then allow them to pick how they want to arrange the bocks (number of rows and number of columns). Afterwards, the blocks will be arranged according to that and the page can be saved. 
- endpoint: /api/save_page
- ⁠expects a json with the following keys: “theme_name”, “page_name”, “rows” which is an integer of the number of rows they chose, “columns” which is an integer of the number of columns they chose, and “blocks” which should be a list that contains a dictionary (object) of each block. Each dictionary in the “blocks” list must contain details of the word in the block such as  “name” (name of the word), “table_name” (table of the word that I sent earlier in the dynamo search endpoint), and ‘option’. Remember I said the ‘option’ key for each block should consist of either of the seven possible combinations we discussed. This is helpful because it would let you know which option they chose when we are trying to fetch the blocks back later on. The options are integers with 1 for image only, 2 for audio only, 3 for video only, 4 for image and audio, 5 for image and video, 6 for audio and video, and 7 for image, audio and video. 
- ⁠returns a json with key “success” for if its successful, else it returns an error if there is an issue while trying to save. 

5. Fetch themes: this endpoint fetches all the existing themes. It is a get request.
- endpoint: /api/fetch_all_themes
- ⁠expects nothing
- ⁠returns a json with key “themes” and a list of all the themes.

6. Fetch pages: this is when one themes has been clicked and we want to fetch all the pages under that theme
- endpoint: /api/fetch_theme_pages
- ⁠expects a json with a key “theme_name”
- ⁠returns a json with key “pages” and a value that is a list of dictionaries one for each page. Each dictionary contains the “page_name”, “block_row”, and “block_column” for each page. The block row and block column are integers that be used to arrange the blocks once that page is clicked. So basically each page has its own number of block rows and columns that was initially set by the person that created the page. So when the next request below for blocks are made, those blocks can then be arranged according to the rows and columns of the page above.

7. Fetch blocks: this is basically to fetch the details of all the blocks once the page is clicked. 
- endpoint: /api/fetch_page_blocks
- ⁠expects a json with a key “page_name”.
- ⁠returns a JSON with the key ‘blocks’ which is a list of all the blocks present in that page. The list contains dictionaries and each dictionary stands for one block. The keys in each dictionary are key “name” for the word name, key “option” which is the integer that helps you know which of the files to include (remember the pattern to the options I described under the endpoint for “save page” above), key “image” for image path, key “audio” for audio path, key “video” for video path.