prompt_recipe_main_info = """
            Your goal is to find the elements in the page source that represent the recipe main info and return them in valid json format. 
            Output json:

            ```json
            { "name": "The title or name of the recipe as string", "servings": "The servings (only number as integer must not be null)", "description": "The description of the recipe", "image": "Image src path", "video" "Video source path (if available), "difficulty": "string one of 'Easy', 'Intermediate', 'Advanced' or 'Expert'", "chef": "The chef of the recipe if any else null as NULL value", "prep_time": "preparation time in minutes integer value", "cook_time": "The cook time in minutes integer" }
            ```

            Make sure to return a plain json dict object with the values found on the page source as described.
            If description is not present in thr source add your based on the recipe name and steps.
            If no data.json is available return empty json as:
            ```json
            {}
            ```
            Or if field is missing return null for value except the servings.Make sure the image url pointing to a image file not blob or else.
            !Note return only the json not conversions!
            """

prompt_recipe_instructions = """ 
            Your goal is to find the instructions of the recipe in the provided page source and return them as list of json objects
            Output json:

            ```json
            [ { "text": "Instruction value start from first" }, { "text": "Second instruction value" }, {"text": "Third instruction value"} ]"
            ```

            You must combine all instructions from the page source at the single list of json objects.
            If no data.json is available return empty json as:
            ```json
            {}
            ```
            !Note return only the json not conversions!
            """

prompt_recipe_ingredients = """
            Your goal is to find the ingredients of the recipe in the provided page source and return them as list of json objects
            Output json:

            ```json
            [ { "name": "Full text of the ingredient name", "quantity": "an string value of the quantity if the ingredient", "metric": "the metric of the ingredient eg. g, ml, pcs etc." } , { "name": "Full text of the second ingredient name", "quantity": "an string value of the quantity if the second ingredient", "metric": "the metric of the second ingredient eg. g, ml, pcs etc." } ]"
            ```

            You must combine all ingredients from the page source at the single list of json objects.
            If no data.json is available return empty json as:
            ```json
            {}
            ```
            !Note return only the json not conversions!
            """

prompt_generate_recipe = """
            Your goal is to generate 5 recipes from the provided ingredients. 
            Output json:

            ```json
            [ { "name": "Full name of the recipe"}, .... ]
            ```

            You must not make up a recipe names.
            Some times there will be 2 or more ingredients generate recipe names in all cases that has this ingredients.
            Be creative and supply the names even for 2 ingredients.
            If no data.json is available return empty json as:
            ```json
            {}
            ```
            !Note return only the json not conversions!
            """

prompt_translate_recipe = """
            Your task is to translate the given recipe and return it in structured json format:
            ```json
            { "name": "Translated name string", "description": "Translated description string", "ingredients" : [ { "name": "Full text of the ingredient name", "quantity": "an string value of the quantity if in the ingredient", "metric": "the metric of the ingredient eg. g, ml, pcs etc."}, ... ], "steps" : [{ "text": "Instruction value start from first" }, { "text": "Second instruction value" }, {"text": "Third instruction value"} ]
            ```
            !Note you must translate only the: `name`, `description`, `ingredients` and `steps`
            as described in the json example and the ingredients metrics and quantity should be the correct by the standard of the language.
            !Note return only the json not conversions!
            """

prompt_tts_audio = """
            Speak as professional cooking chef assistant with pause of 0.5 sec on each item (name, ingredient and instruction). You must spell the recipe `name`, the `ingredients` and \
            `instruction` from the provided json string object on the provided language: {0} including the name, instruction and ingredients words to the same language: {0}. \
            Important: You must not skip any ingredient and instruction or mix them also the ingredients \
            must be read with all available information for each of them without skipping nothing! (Pay attention to this).\
            And finish the speach after all are spelled.
            """