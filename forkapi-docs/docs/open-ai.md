---
hide:
  - navigation
---

# OpenAI integration
---

Here you can find how we use OpenAI model for the application. <br>
    
???+ Info  

    Available from 2.2.0+ release.
    TTS available from 5.0.0+ release.

## Functionality with the AI model
Open AI chat gpt model `gpt-4o-mini` is the default model that we use it the API.
For the purpose of his task is working ok and is the lowest cost model from OpenAI.
For TTS the model is `tts-4o-mini` which is the latest model can translate to any language but best results are for English.

1. We use it to scrape a recipe from external url.
2. We use it to generate a recipes from ingredients and after this we scrape the recipes from the available url online.
3. We use it to translate recipe to selected number of languages
4. We use it for generating of a recipe audio file that record the recipe name, ingredients and instructions
5. We use it to add emojis in the recipe name and ingredients if recognise a word that has representing emoji


## Edge cases
There a case where the model fails and we return empty response with status code `204` from the endpoint that are responsible for generating or scraping the recipes.

## Endpoint which work with the OpenAI
    
#### Scrape recipes

??? pied-piper "POST /api/recipe/scrape"
    
    ##### Payload
    ``` json title="recipe.RecipeLink object"
    {
        "url": file
    }
    ```

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`    | `Token obtained from login endpoint `      | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `200`         | `application/json`                |  `{recipe.Recipe object}`|                                          |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`        |

    ##### Example cURL
    
    > ``` bash
    > curl --location 'host/api/recipe/scrape' --header 'Authorization: Token token_value'  --data '{"url":"http://...."}'
    > ```
    

#### Generate recipes

??? pied-piper "POST /api/recipe/generate"

    ##### Payload
    ``` json title="GenerateRecipeSerializer list of strings"
    {
        "ingredients": [],
        "meal_type": string
    }
    ```

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`    | `Token obtained from login endpoint `      | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `200`         | `application/json`                |  `[GenerateRecipeResultSerializer objects]`                         |
    | `204`         | `application/json`                |  `{Empty response if there a openai empty response}`                |
    | `401`         | `application/json`                |  `{"detail":"Authentication credentials were not provided."}`       |

    ##### Example cURL
    
    > ``` bash
    > curl --location 'host/api/recipe/generate' --header 'Authorization: Token token_value' --header 'Content-Type: application/json' --data '{"ingredients":["tomato","onion","cheese","pasta","milk","red peparz"]}'
    > ```


#### Translate recipes

??? pied-piper "POST /api/recipe/translate"

     ##### Payload
        ``` json title="recipe.Recipe object"
        {
            "pk": recipe.pk,
            "language": recipe.models.LANGUAGES_CHOICES
        }
        ```

    ##### Language choices (LANGUAGES_CHOICES)
    ``` python title="recipe.models.LANGUAGES_CHOICES (use only the key in the request)"
            ('English', 'English'),
            ('Spanish', 'Español'),
            ('French', 'Français'),
            ('German', 'Deutsch'),
            ('Chinese', '中文'),
            ('Russian', 'Русский'),
            ('Italian', 'Italiano'),
            ('Japanese', '日本語'),
            ('Dutch', 'Nederlands'),
            ('Polish', 'Polski'),
            ('Greek', 'Ελληνικά'),
            ('Swedish', 'Svenska'),
            ('Czech', 'Čeština'),
            ('Bulgarian', 'Български'),
    ```
        
    ##### Headers
        
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint `                         | 

    
    ##### Responses
        
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.Recipe object}`|
    | `400`         | `application/json`                | `{"errors":["Default language for translation should be set"]}`                       |
    | `400`         | `application/json`                | `{"errors":["Translation must be performed only on original recipes"]}`                       |
    | `400`         | `application/json`                | `{"errors":["Translation language is already used and there a recipe translated with that language."]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
        
    > ``` bash
    >  curl --location 'host/api/recipe/translate' --header 'Authorization: Token token_value' --data '{"pk":15,"language":"German"}'
    > ```


#### Generate recipe audio
    
??? pied-piper "POST /api/recipe/audio"
        
    ##### Payload
    ``` json title="recipe.Recipe object"
    {
        "recipe_pk": int
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint `                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.AudioInstructionsSerializer object}`|
    | `400`         | `application/json`                | `{"errors":["Recipe is converted to audio instructions already"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |
    | `404`         | `application/json`                | `{"errors":["Recipe with that pk does not exists"]}`                       |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/audio' --header 'Authorization: Token token_value' --data '{"recipe_pk":15}'
    > ```

## Requirements
To use this functionality you must have a valid API_KEY from OpenAI

