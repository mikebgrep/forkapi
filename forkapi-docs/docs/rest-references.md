---
hide:
  - navigation
---

### RestAPI reference

###### *On this page you can check the RestAPI endpoints.*

!!! note 
    
    The API has build in csrf protection you may need to attach Cookie
    with value csrftoken=token to work proparly

------------------------------------------------------------------------------------------

# Authentication
#### Create admin user

??? pied-piper "POST /api/auth/signup"

    ##### Payload
    ``` json title="authentication.UserSerializer"
    {
        "username": "username",
        "password": "password",
        "email": "email",
        "is_superuser": true
    }
    ```

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 
    
    
    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `201`         | `application/json`                | `User created successfully`                                         |
    | `400`         | `application/json`                | `{"username":["user with this username already exists."]}`          |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/auth/signup' --header 'X-Auth-Header: X_AUTH_HEADER' --header 'Content-Type: application/json' --data '{"username":"username","password":"password","email":"email","is_superuser":true}'
    > ```


#### Obtain access token

??? pied-piper "POST /api/auth/token"

    ##### Payload
    ``` json title="authentication.UserSerializer"
    {
        "email": "email",
        "password": "password"
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 
    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{"token":"token","user":{"username":"username","email":"email","is_superuser":true}}`|
    | `404`         | `application/json`                | `{"detail":"No User matches the given query."}`                       |
    | `403`         | `application/json`                | `{"detail": "You must use authentication header"}`                    |

    ##### Example cURL
    
    > ``` bash
    >  `curl --location 'host/api/auth/token' --header 'X-Auth-Header: X_AUTH_HEADER' --header 'Content-Type: application/json' --data '{"email":"email","password":"password"}''
    > ```

#### Get user profile info

??? pied-piper-get "GET /api/auth/user/info"


    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `200`         | `application/json`                | `{"username":"username","email":"email","date_joined":"date"}`                                |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`        |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'localhost:8080/api/auth/user/info' --header 'Authorization: Token token_value' 
    > ```

#### Change user password
    
??? pied-piper-put "PUT /api/auth/user"

    ##### Payload
    ``` json 
    {
        "old_password": "password",
        "new_password": "password"
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `204`         | `application/json`                | `{}`                                                                  |
    | `400`         | `application/json`                | `{"message": "Old password does not match current password"}`         |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PUT 'host/api/auth/user' --header 'Authorization: Token token_value' --header 'Content-Type: application/json'  --data '{"old_password":"old_password","new_password":"new_password"}'
    > ```

#### Update user email and username
    
??? pied-piper-patch "PATCH /api/auth/user"
    
    ???+ Info 
        
        Individual fields can be updated only username or password.
    
    ##### Payload
    ``` json title="authentication.UserSerializer"
    {
        "username": "new_username",
        "email": "new_email"
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{"username":"new_username","email":"new_email","is_superuser":true}` |
    | `400`         | `application/json`                | `{"email":["Enter a valid email address and password."]}`             |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PATCH 'host/api/auth/user' --header 'Authorization: Token token_value'  --header 'Content-Type: application/json' --data-raw '{"username":"new_username","email":"new_email"}'
    > ```


#### Delete user account
    
??? pied-piper-delete "DELETE /api/auth/delete-account"
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint `                                 | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `204`         | `application/json`                | `No Content`                                                          |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request DELETE 'host/api/auth/delete-account' --header 'Authorization: Token token_value' 
    > ```

#### Request password reset token for user account
    
??? pied-piper "POST /api/auth/password_reset"

    ##### Payload
    ``` json title="authentication.ResetPasswordRequestSerializer"
    {
        "email": "user_email"
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{"token":"token_value"}`                                             |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                     |
    | `404`         | `application/json`                | `{"error":"User with provided email not found"}`                      |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/auth/password_reset' --header 'Content-Type: application/json' --header 'X-Auth-Header: auth_header_value'   --data-raw '{"email":"user_email"}' 
    > ```

#### Change user password with token
    
??? pied-piper "POST /api/auth/password_reset/reset"

     ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `token`   |`query (required)` | `string`        | `Token obtained from POST /api/auth/password_reset`                      | 

    ##### Payload
    ``` json 
    {
        "password": "new_password",
        "confirm_password": "new_password"
    }
    ```

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `204`         | `application/json`                | `No Content`                                                          |
    | `404`         | `application/json`                | `{"detail":"No PasswordResetToken matches the given query."}}`        |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/auth/password_reset/reset?token=token_value' --header 'Content-Type: application/json'  --data '{"password":"new_password","confirm_password":"new_password"}'
    > ```



------------------------------------------------------------------------------------------

# User Settings

#### Get User settings

??? pied-piper-get "GET /api/auth/settings/"



    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `200`         | `application/json`                | `{auth.models.UserSettingsSerializer}`                                |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`     |

    ##### Example cURL
    
    > ``` bash
    > curl --location --request GET 'host/api/auth/settings' --header 'Authorization: Token token_value' 
    > ```

#### Update user settings

??? pied-piper-patch "PATCH  /api/auth/settings/"
    
    ##### Payload
    ``` json title="auth.serializers.UserSettingsSerializer object"
    {
        "preferred_translate_language": LANGUAGES_CHOICES,
        "compact_pdf": bool,
        "emoji_recipes": bool
    }
    ```

    ##### Languages choices (LANGUAGES_CHOICES)
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
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `201`         | `application/json`                | `{auth.models.UserSettingsSerializer}`                                |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`     |

    ##### Example cURL
    
    > ``` bash
    > curl --location --request PATCH 'host/api/auth/settings' --header 'Authorization: Token token_value' --data '{"language":"recipe.models.LANGUAGES_CHOICES", "compact_pdf": true, "emoji_recipes": true}'
    > ```

------------------------------------------------------------------------------------------

# Recipe

#### Search for recipes

??? pied-piper-get "GET /api/recipe/home/"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `search`  |`query (optional)` | `string`        | `Part or fulll name of the recipe.Recipe object`                      | 
    | `page`    |`query (optional)` | `int`           | `Page number if there a mutilple pages result`                        | 
    

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `200`         | `application/json`                | `{"count":int,"next":string,"previous":string,"results":[recipe.Recipe obj list]}`                                |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`     |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'http://host:port/api/recipe/home/?name=name&page=1' --header 'X-Auth-Header: X_AUTH_HEADER
    > ```

#### Get favorite recipes

??? pied-piper-get "GET /api/recipe/home/favorites/"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `{"count":int,"next":string,"previous":string,"results":[recipe.Recipe obj list]}` |
    | `404`         | `application/json`                | `{"detail":"No Recipe matches the given query."}`                                  |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'http://host:port/api/recipe/home/favorites/' --header 'X-Auth-Header: X_AUTH_HEADER
    > ```



#### Get trending recipes

??? pied-piper-get "GET /api/recipe/trending"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `[recipe.Recipe objects list]`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'localhost:8080/api/recipe/trending' --header 'X-Auth-Header: X_AUTH_HEADER
    > ```

#### Search for recipes preview

??? pied-piper-get "GET /api/recipe/home/preview/"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `search`  |`query (optional)` | `string`        | `Part or fulll name of the recipe.Recipe object`                      | 
    | `page`    |`query (optional)` | `int`           | `Page number if there a mutilple pages result`                        | 
    

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `200`         | `application/json`                | `{"count":int,"next":string,"previous":string,"results":[recipe.RecipePreviewSerializer obj list]}`                                |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`     |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'http://host:port/api/recipe/home/preview/?name=name&page=1' --header 'X-Auth-Header: X_AUTH_HEADER
    > ```

#### Update favorite status

??? pied-piper-patch "PATCH /api/recipe/int:pk/favorite"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to be favorited or unfavorited`                   | 
    

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint`                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `201`         | `application/json`        | `"Success favorite recipe"`                                |
    | `201`         | `application/json`        | `"Success unfavorite recipe"`                                |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}     |
    | `404`         | `application/json`                | `Not Found`          |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PATCH 'host/api/recipe/1/favorite' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```

#### Get recipe by pk

??? pied-piper-get "GET /api/recipe/int:pk/"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to be updated`                   | 
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.Recipe object}`                                              | 
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                     |
    | `404`         | `application/json`                |  {"detail":"No Recipe matches the given query."}                      |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request GET 'host/api/recipe/1/' --header 'X-Auth-Header: X_AUTH_HEADER
    > ```


#### Create recipe

??? pied-piper "POST /api/recipe/"

    ##### Payload
    ``` json title="recipe.Recipe object"
    {
        "image": file,
        "name": string,
        "serves": int,
        "description": string,
        "difficulty": string (DIFFICULTY_CHOICES),
        "chef": string
        "video": file (optional),
        "tag": <int:pk> (optional), 
        "prep_time": int,
        "cook_time": int
    }
    ```

    ##### Dificulty choices (DIFFICULTY_CHOICES)
    ``` python title="recipe.models.DIFFICULTY_CHOICES (use only the key in the request)"
        ('Easy', 'Easy'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint `                         | 
    |`Content-Type`|`multipart/form-data`|  `Recipe object`  | `Recipe multipart/form-data object`                                | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{recipe.Recipe object}`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/' --header 'Authorization: Token token_value' --form  'image=@"/path/image.jpg"' --form 'name="Recipe name"' --form 'servings="5"' --form 'category="1"' --form 'tag="1"' --form 'prep_time="20"' --form 'video=@"/path/video.mp4"' --form 'description="This is cool recipe"' --form 'cook_time="45"'
    > ```


#### Update recipe main info (without ingredients and steps)

??? pied-piper-put "PUT /api/recipe/int:pk"

    ##### Payload
    ``` json title="recipe.Recipe object"
    {
        "image": file,
        "name": string,
        "serves": int,
        "description": string,
        "difficulty": string (DIFFICULTY_CHOICES),
        "chef": string
        "video": file (optional),
        "tag": <int:pk> (optional), 
        "prep_time": int,
        "cook_time": int,
        "clear_video": boolean (optional if you want to delete already set video)
    }
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to be updated`                   | 
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`    | `Token obtained from login endpoint `      | 
    |`Content-Type`|`multipart/form-data`|  `Recipe object`  | `Recipe multipart/form-data object`                                | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.Recipe object}`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PUT 'host/api/recipe/1' --header 'Authorization: Token token_value' --form  'image=@"/path/image.jpg"' --form 'name="Recipe name"' --form 'servings="5"' --form 'category="1"' --form 'tag="1"' --form 'prep_time="20"' --form 'video=@"/path/video.mp4"' --form 'description="This is cool recipe"' --form 'cook_time="45"'
    > ```


#### Update Recipe Category
    
??? pied-piper-patch "PATCH /api/recipe/int:pk/category"
    
     ##### Payload
    ``` json
    {
        "category_pk": int
    }
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key`                   | 
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `204`         | `application/json`                | `` |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |
    | `404`         | `application/json`                | `{"detail": "No Recipe matches the given query."]}`             |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PATCH 'host/api/recipe/<int:pk>/category' --header 'Authorization: Token TOKEN_VALUE'  --data '{"category_pk":2}'
    > ```

#### Delete recipes

??? pied-piper-delete "DELETE /api/recipe/pk:int/"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to be deleted`                   | 


    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`    | `Token obtained from login endpoint `      | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `204`         | `application/json`                |                                                                     |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request DELETE 'host/api/recipe/<int:pk>/' --header 'Authorization: Token token_value' 
    > ```



#### Get recipe variations (translation)

??? pied-piper-get "GET /api/recipe/int:pk/variations"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to be updated`                   | 
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.serializers.TranslateRecipeSerializer object}`                                              | 
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                     |
    | `404`         | `application/json`                |  {"detail":"No Recipe matches the given query."}                      |

    ##### Example cURL
    
    > ``` bash
    > curl --location 'host/api/recipe/20/variations' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```

#### Get recipe variations (translation)

??? pied-piper-get "GET /api/recipe/random"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.serializers.RecipePreviewSerializer object}`                                              | 
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                     |

    ##### Example cURL
    
    > ``` bash
    > curl --location 'host/api/recipe/random' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```

------------------------------------------------------------------------------------------

# Recipe OpenAI

#### Scrape recipes

??? pied-piper "POST /api/recipe/scrape"

    ???+ Info 
        
        Valid OpenAI API Key is nedded for this endpoint
    
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

    ???+ Info 
        
        Valid OpenAI API Key is nedded for this endpoint
    
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
    > curl --location 'host/api/recipe/generate' --header 'Authorization: Token token_value' --header 'Content-Type: application/json' --data '{"ingredients":["tomato","onion","cheese","pasta","milk","red peparz"], "meal_type": "Pasta"}'
    > ```

#### Translate recipe

??? pied-piper "POST /api/recipe/translate"
    
    ???+ Info 
        
        Valid OpenAI API Key is nedded for this endpoint

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
    
    ???+ Info 
        
        Valid OpenAI API Key is nedded for this endpoint. 
        Current model used is tts-4o-mini that translate English language good and struggle for other languages.

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

------------------------------------------------------------------------------------------

# Category

#### Get all categories

??? pied-piper-get "GET /api/recipe/category"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `[recipe.Category objects list]`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/category' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```


#### Get all categories recipes 

??? pied-piper-get "GET /api/recipe/category/int:pk/recipes"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Category primary key`                   | 
    

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `[recipe.Recipe objects list]`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/category/1/recipes' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```

#### Create category

??? pied-piper "POST /api/recipe/category/add"

    ##### Payload
    ``` json title="recipe.Category object"
    {
        "name": string
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`    | `Token obtained from login endpoint`              | 
    |`Content-Type`|`application/json`|                   | `Applicaton Json content header                                     | 
 

    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{recipe.Category object}`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/category/add' --header 'Authorization: Token token_value' --data '{"name":"Greek"}'
    > ```

#### Update category

??? pied-piper-put "PUT /api/recipe/category/int:pk"

    ##### Payload
    ``` json title="recipe.Category object"
    {
        "name": string,

    }
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Category primary key`                   | 
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`    | `Token obtained from login endpoint `              | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.Recipe object}`|
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |
    | `404`         | `application/json`                | `{"detail":"No Category matches the given query."}`                       |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PUT 'host/api/recipe/category/6' --header 'Authorization: Token token_value'  --header 'Content-Type: application/json'  --data '{"name":"Italiano"}'
    > ```

------------------------------------------------------------------------------------------

# Tag

#### Get all tags 

??? pied-piper-get "GET /api/recipe/tags"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `[recipe.Tag objects list]`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/tags' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```

#### Get all recipes from tag 

??? pied-piper-get "GET /api/recipe/tag/int:pk/recipes"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Tag primary key`                   | 
    

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `{"count":int,"next":string,"previous":string,"results":[recipe.Recipe obj list]}`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/tag/<int:pk>/recipes' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```

#### Create tag

??? pied-piper "POST /api/recipe/tag/add"

    ##### Payload
    ``` json title="recipe.Tag object"
    {
        "name": string
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint `      | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{recipe.Category object}`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/tag/add' --header 'Authorization: Token token_value' --data '{"name":"Summer vibes"}'
    > ```

#### Update tag

??? pied-piper-put "PUT /api/recipe/tag/int:pk"

    ##### Payload
    ``` json title="recipe.Category object"
    {
        "name": string,

    }
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Tag primary key`                   | 
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint `                         | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.Tag object}`|
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |
    | `404`         | `application/json`                | `{"detail":"No Category matches the given query."}`                       |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PUT 'host/api/recipe/tag/1' --header 'Authorization: Token token_value'  --header 'Content-Type: application/json'  --data '{"name":"Summer Vibes"}'
    > ```


------------------------------------------------------------------------------------------

# Ingredients

??? pied-piper "POST /api/recipe/int:pk/ingredients"

    ???+ Info 
        
        Override already existing ingredients for the recipe

    ##### Payload
    ``` json title="recipe.Igredient object list"
    [
        {
            "name": "string,
            "quantity": string,
            "metric": "string
        },
        {
            "name": "string,
            "quantity": string,
            "metric": "string
        },
    ....
    ]
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to which to link the ingredients`                   | 
    
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint `                         | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `[{recipe.Ingrediant object}]`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/ingredients' --header 'Authorization: Token token_value' --data '[{"name":"Kasher salt","quantity":"1/5","metric":"tbsp","recipe":24}]'
    > ```

------------------------------------------------------------------------------------------

# Steps

??? pied-piper "POST /api/recipe/int:pk/steps"

    ???+ Info 
        
        Override already existing steps for the recipe

    ##### Payload
    ``` json title="recipe.Step object list"
    [
        {
            "text": string
        },
        {
            "text": string
        },
    ....
    ]
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Recipe primary key to which to link the steps`                   | 
    
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`            | `Token obtained from login endpoint`                         | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `[{recipe.Step object}]`|
    | `400`         | `application/json`                | `{"tag":["Incorrect type. message"]}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/recipe/ingredients' --header 'Authorization: Token token_value' --data '[{"text":"Heat the oven","recipe":1}]'
    > ```

------------------------------------------------------------------------------------------

# Schedule (Meal Planner)
#### Get Schedule

??? pied-piper-get "GET /api/schedule/"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `date`    |`path (required)` | `int`        | `Schedule date eg. 2025-1-26`                   | 

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`X-Auth-Header`|`required `|       `UUID`            | `Header used for authentication with the API`                         | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `[schedule.ScheduleRepresentationSerializer objects list]`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/schedule/?date=2025-02-15' --header 'X-Auth-Header: X_AUTH_HEADER'
    > ```

#### Create schedule

??? pied-piper "POST /api/schedule/"

    ##### Payload
    ``` json title="recipe.Category object"
    {
        "timing": schedule.models.TIMING_CHOICES,
        "recipe": recipe.pk,
        "date": date-format-YYYY-MM-DD
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`    | `Token obtained from login endpoint`              | 
    |`Content-Type`|`application/json`|                   | `Applicaton Json content header                                     | 
 

    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{schedule.ScheduleRepresentationSerializer object}`|
    | `400`         | `application/json`                | `{"error": "Invalid date format. Use YYYY-MM-DD."}`                       |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/schedule/' --header 'Authorization: Token token_value' --data '{"timing":"Breakfast","recipe":26,"date":"2025-02-15"}'
    > ```

#### Delete schedule
    
??? pied-piper-delete "DELETE /api/schedule/<int:pk>"

     ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Schedule pk`                   |         

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint `                                 | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `204`         | `application/json`                | `No Content`                                                          |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request DELETE 'host/api/schedule/<int:pk>' --header 'Authorization: Token token_value' 
    > ```

------------------------------------------------------------------------------------------

# Shopping (Shopping List)

#### Get Shopping lists

??? pied-piper-get "GET /api/shopping/"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint `                                 | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `[recipe.ShoppingList objects list]`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/shopping/' --header 'Authorization: Token token_value' 
    > ```

#### Get Shopping list (single)

??? pied-piper-get "GET /api/shopping/single/int:pk/"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint `                                 | 

    ##### Responses
    
    | http code     | content-type                      | response                                                                           |
    |---------------|-----------------------------------|------------------------------------------------------------------------------------|
    | `200`         | `application/json`                | `[recipe.ShoppingList object]`                                                     |
    | `403`         | `application/json`                | `{"detail":"You must use authentication header"}`                                  |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/shopping/single/<int:pk>/' --header 'Authorization: Token token_value' 
    > ```

#### Create shopping

??? pied-piper "POST /api/shopping/"

    ##### Payload
    ``` json title="shopping.ShoppingListSerializer partial object"
    {
        "name": "string"
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`    | `Token obtained from login endpoint`              | 
    |`Content-Type`|`application/json`|                   | `Applicaton Json content header                                     | 
 

    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{schedule.SingleShoppingListSerializer object}`|
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/shopping/'  --header 'Authorization: Token token_value'  --data '{"name":"asd12"}'
    > ```

#### Update Schopping List

??? pied-piper-put "PUT /api/shopping/int:pk"

    ##### Payload
    ``` json title="recipe.ShoppingListSerializer parital object"
    {
        "recipe": integer
    }
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Shopping list primary key`                   | 
    
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|       `Access Token`    | `Token obtained from login endpoint `              | 
    |`Content-Type`|`application/json`|    | `Applicaton Json content header                         | 


    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{recipe.ShoppingList object}`|
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`                    |
    | `404`         | `application/json`                | `{"detail":"No ShoppingList matches the given query."}`                       |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PUT 'host/api/shopping/<int:recipe_pk>>/' --header 'Authorization: Token token_value' --data '{"recipe":recipe_pk}'
    > ```


#### Complete Shopping List
    
??? pied-piper-patch "PATCH /api/shopping/complete-list/int:pk/"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Shopping list primary key`                   | 
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{"Success complete shopping list"}` |
    | `201`         | `application/json`                | `{"Success incomplete shopping list"}` |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |
    | `404`         | `application/json`                | `{"detail": "No ShoppingList matches the given query."]}`             |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PATCH 'host/api/shopping/complete-list/<int:pk>/'  --header 'Authorization: Token token_value'
    > ```

#### Delete Shopping List
    
??? pied-piper-delete "DELETE /api/shopping/int:pk/"
    
     ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Shopping list primary key`                   | 

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint `                                 | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `204`         | `application/json`                | `No Content`                                                          |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |
    | `404`         | `application/json`                | `{"detail": "No ShoppingList matches the given query."}`         |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request DELETE 'host/api/shopping/<int:pk>/'  --header 'Authorization: Token token_value'
    > ```


#### Add Item to Shopping List
    
??? pied-piper-patch "PATCH /api/shopping/single/int:pk/"

    ##### Payload
    ``` json title="shopping.ShoppingItemPatchSerializer partial object"
    {
        "name": string,
        "quantity": string,
        "metric": string
    }
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Shopping list primary key`                   | 
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{shopping.ShoppingItemSerializer object}` |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |
    | `404`         | `application/json`                | `{"detail": "No ShoppingList matches the given query."]}`             |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PATCH 'host/api/shopping/single/<int:pk>/' --header 'Authorization: Token token_value'  --data '{"name":"Test ingredient11","quantity":"1231","metric":"gr"}' 
    > ```

#### Update Item in Shopping List
    
??? pied-piper-patch "PATCH /api/shopping/item/int:pk/"

    ##### Payload
    ``` json title="shopping.ShoppingItemPatchSerializer partial object"
    {
        "name": string,
        "quantity": string,
        "metric": string
    }
    ```

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Shopping list Item primary key`                   | 
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `200`         | `application/json`                | `{shopping.ShoppingItemSerializer object}` |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |
    | `404`         | `application/json`                | `{"detail": "No ShoppingList matches the given query."]}`             |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PATCH 'host/api/shopping/item/54/'  --header 'Authorization: Token token_value' --data '{"name":"Changed11","quantity":10001,"metric":"gr1"}' 
    > ```

#### Complete Item in Shopping List
    
??? pied-piper-patch "PATCH /api/shopping/item/int:pk/complete/"

    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Shopping list Item primary key`                   | 
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `201`         | `application/json`                | `{"Success completed item"}` |
    | `201`         | `application/json`                | `{"Success incompleted item"}` |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |
    | `404`         | `application/json`                | `{"detail": "No ShoppingItem matches the given query."]}`             |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PATCH 'localhost:8081/api/shopping/item/<int:pk>>/complete/'  --header 'Authorization: Token token_value'
    > ```

#### Delete Shopping List Item
    
??? pied-piper-delete "DELETE /api/shopping/item/int:pk/"
    
     ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `Shopping list item primary key`                   | 

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint `                                 | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `204`         | `application/json`                | `No Content`                                                          |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |
    | `404`         | `application/json`                | `{"detail": "No ShoppingItem matches the given query."}`         |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request DELETE 'host/api/shopping/<int:pk>/'  --header 'Authorization: Token token_value'
    > ```

------------------------------------------------------------------------------------------

# Backupper (backup database)

#### Create backup

??? pied-piper "POST /api/backupper/"


    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint `                                 | 
    
    
    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `201`         | `application/json`                | `Successfully created backup file: backups/file.zip`                                         |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request POST 'host/api/backupper/' --header 'Authorization: Token TOKEN_VALUE'
    > ```


#### Get all backups

??? pied-piper-get "GET /api/backupper/"


    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `200`         | `application/json`                | `[BackupSnapshotSerializer objects]`                                |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`        |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/backupper/' --header 'Authorization: Token TOKEN_VALUE' 
    > ```


#### Get single backups

??? pied-piper-get "GET /api/backupper/int:pk/"
    
    ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `BackupSnapshot.pk`                   | 

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 

    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `200`         | `application/json`                | `{BackupSnapshotSerializer object}`                                |
    | `401`         | `application/json`                | `{"detail":"Authentication credentials were not provided."}`        |

    ##### Example cURL
    
    > ``` bash
    >  curl --location 'host/api/backupper/2/' --header 'Authorization: Token TOKEN_VALUE' 
    > ```


#### Apply backup
    
??? pied-piper-patch "PATCH /api/backupper/"
    
    ##### Payload
    ``` json
    {
        "backup_pk": int"
    }
    ```
    
    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `204`         | `application/json`                | `{"Successfully loaded backup file: backups/file.zip}` |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |
    | `404`         | `application/json`                | `{"detail": "No BackupSnapshot matches the given query."}`         |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request PATCH 'host/api/backupper/' --header 'Authorization: Token TOKEN_VALUE' --data '{"backup_pk":2}'
    > ```

#### Import backup

??? pied-piper "POST /api/backupper/import/"

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint`      | 
    
    
    ##### Responses
    
    | http code     | content-type                      | response                                                            |
    |---------------|-----------------------------------|---------------------------------------------------------------------|
    | `201`         | `application/json`                | `File uploaded successfully`                                         |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |

    ##### Example cURL
    
    > ``` bash
    >  curl -X POST  --header 'Authorization: Token TOKEN_VALUE' -F "file=@file.zip" host/api/backupper/import/
    > ```


#### Delete backup
    
??? pied-piper-delete "DELETE /api/backupper/int:pk/"
    
     ##### Parameters
    
    | name      |  type     | data type               | description                                                           |
    |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    | `<int:pk>`    |`path (required)` | `int`        | `BackupSnapshot.pk`                   | 

    ##### Headers
    
    | name          |  type     | data type               | description                                                           |
    |---------------|-----------|-------------------------|-----------------------------------------------------------------------|
    |`Authorization`|`required `|   `Access Token`        | `Token obtained from login endpoint `                                 | 

    
    ##### Responses
    
    | http code     | content-type                      | response                                                              |
    |---------------|-----------------------------------|-----------------------------------------------------------------------|
    | `204`         | `application/json`                | `No Content`                                                          |
    | `403`         | `application/json`                | `{"detail": "Authentication credentials were not provided."}`         |
    | `404`         | `application/json`                | `{"detail": "No BackupSnapshot matches the given query."}`         |

    ##### Example cURL
    
    > ``` bash
    >  curl --location --request DELETE 'host/api/backupper/1/' --header 'Authorization: Token TOKEN_VALUE'
    > ```