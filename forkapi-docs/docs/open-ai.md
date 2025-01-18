---
hide:
  - navigation
---

# OpenAI integration
---

Here you can find how we use OpenAI model for the application. <br>
    
???+ Info  

    Available from 2.2.0+ release.

## Functionality with the AI model
Open AI chat gpt model `gpt-4o-mini` is the default model that we use it the API.
For the purpose of his task is working ok and is the lowest cost model from OpenAI.

1. We use it to scrape a recipe from external url.
2. We use it to generate an recipes from ingredients and after this we scrape the recipes from the available url online.

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
        "ingredients": []
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


## Requirements
To use this functionality you must have a valid API_KEY from OpenAI

