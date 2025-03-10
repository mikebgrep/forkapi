import os, uuid, random, pytest, json
import shutil

from authentication.models import User, PasswordResetToken
from recipe.models import Category, Tag, Recipe, Ingredient
from recipe.util import calculate_recipe_total_time
from .models import UserUpdateDetailsEnum, PasswordResetChoice
from .constants import LENGTH_PASSWORD_ERROR_MESSAGE, PASSWORD_TO_COMMON_ERROR_MESSAGE, \
    OLD_PASSWORD_DOES_NOT_MATCH_ERROR_MESSAGE, NUMERIC_PASSWORD_ERROR_MESSAGE, \
    CONFIRM_AND_NEW_PASSWORD_DOES_NOT_MATCH_ERROR_MESSAGE
from rest_framework.authtoken.models import Token
from dotenv import load_dotenv
from rest_framework.test import APIClient
from django.test import override_settings

load_dotenv()


@pytest.fixture(scope="function")
def api_client():
    client = APIClient()
    client.credentials(HTTP_X_AUTH_HEADER=os.getenv('X_AUTH_HEADER'))
    yield client

    #  Clean media from recipe creation after test, override location
    shutil.rmtree('tests/media', ignore_errors=True)


@pytest.mark.django_db
def create_user(api_client):
    admin_user_data = {
        "username": f"admin-{random.uniform(0, 10000)}",
        "password": "test123",
        "email": f"email-{uuid.uuid4()}@email.com",
        "is_superuser": True
    }

    response = api_client.post("/api/auth/signup", admin_user_data, format="json")
    assert response.status_code == 201
    admin_user = User.objects.get(username=admin_user_data['username'])

    return admin_user, admin_user_data


@pytest.mark.django_db
def get_token_and_admin_user(api_client):
    admin_user, admin_user_data = create_user(api_client)
    response = api_client.post("/api/auth/token", admin_user_data, format="json")

    assert response.status_code == 200
    token = Token.objects.get(user=admin_user)

    assert token is not None

    return token, admin_user, admin_user_data


def add_access_token_header(api_client):
    token, admin_user, admin_user_data = get_token_and_admin_user(api_client)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")


def remove_access_token_header_and_add_header_secret(api_client):
    api_client.credentials()
    api_client.credentials(HTTP_X_AUTH_HEADER=os.getenv('X_AUTH_HEADER'))


def request_password_reset_token(api_client):
    token, admin_user, admin_user_data = get_token_and_admin_user(api_client)

    data = {
        "email": admin_user.email
    }

    response = api_client.post("/api/auth/password_reset", data=data, format="json")
    assert response.status_code == 201

    response_data = json.loads(response.content)
    return response_data, data


def request_change_password_validation(api_client, password_reset_choice: PasswordResetChoice):
    response_data, data = request_password_reset_token(api_client)
    api_client.credentials()
    password = None
    confirm_password = None

    match password_reset_choice:
        case PasswordResetChoice.NUMERIC:
            password = "12345678910111210"
            confirm_password = "12345678910111210"

        case PasswordResetChoice.SHORT_ENTRY:
            password = "admin"
            confirm_password = "admin"

        case PasswordResetChoice.NON_MATCHING:
            password = f"password-{uuid.uuid4()}",
            confirm_password = f"password-{uuid.uuid4()}"

    change_password_data = {
        "password": password,
        "confirm_password": confirm_password
    }

    response = api_client.post(f"/api/auth/password_reset/reset?token={response_data['token']}",
                               data=change_password_data, format="json")
    response_data = json.loads(response.content)

    return response, response_data


def request_password_reset_for_user(api_client):
    token, admin_user, admin_user_data = get_token_and_admin_user(api_client)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    password_data = {
        "old_password": admin_user_data['password'],
        "new_password": f"password-{uuid.uuid4()}"
    }

    response = api_client.put("/api/auth/user", data=password_data, format="json")
    assert response.status_code == 204

    new_user_data = {
        "email": admin_user.email,
        "password": password_data['new_password']
    }

    return admin_user, new_user_data, password_data


def password_change_for_validation(api_client, password_reset_choice: PasswordResetChoice):
    token, admin_user, admin_user_data = get_token_and_admin_user(api_client)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    old_password = admin_user_data['password']
    new_password = None
    match password_reset_choice:
        case PasswordResetChoice.NUMERIC:
            new_password = "12345678910111210"
        case PasswordResetChoice.NON_MATCHING:
            old_password = f"password-{uuid.uuid4()}"
            new_password = f"password-{uuid.uuid4()}"
        case PasswordResetChoice.SHORT_ENTRY:
            new_password = "admin"

    password_data = {
        "old_password": old_password,
        "new_password": new_password
    }

    response = api_client.put("/api/auth/user", data=password_data, format="json")
    response_data = json.loads(response.content)

    return response, response_data


def request_user_patch_request(api_client, change_type: UserUpdateDetailsEnum):
    token, admin_user, admin_user_data = get_token_and_admin_user(api_client)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    user_data = {}

    match change_type:
        case change_type.BOTH:
            user_data = {
                "username": f"admin-{uuid.uuid4()}",
                "email": f"email-{uuid.uuid4()}@email.com"
            }
        case change_type.EMAIL:
            user_data = {
                "email": f"email-{uuid.uuid4()}@email.com",
            }
        case change_type.USERNAME:
            user_data = {
                "username": f"admin-{uuid.uuid4()}",
            }

    response = api_client.patch("/api/auth/user", data=user_data, format="json")
    assert response.status_code == 200

    return user_data, admin_user


@pytest.mark.django_db
def create_category(api_client):
    category_data = {
        "name": f"Category-{uuid.uuid4()}"
    }

    response = api_client.post("/api/recipe/category/add", category_data, format="json")
    assert response.status_code == 201

    category = Category.objects.get(name=category_data['name'])

    return category, category_data


@pytest.mark.django_db
def create_tag(api_client):
    tag_data = {
        "name": f"Tag-{uuid.uuid4()}"
    }

    response = api_client.post("/api/recipe/tag/add", tag_data, format="json")
    assert response.status_code == 201

    tag = Tag.objects.get(name=tag_data['name'])

    return tag, tag_data


@pytest.mark.django_db
@override_settings(MEDIA_ROOT='tests/media')
def create_recipe(api_client, original_recipe_pk=None):
    tag, tag_data = create_tag(api_client)
    category, category_data = create_category(api_client)

    recipe_data = {
        "name": f"Recipe-{uuid.uuid4()}",
        "servings": int(random.uniform(0, 20)),
        "category": category.pk,
        "tag": tag.pk,
        "prep_time": random.randrange(1, 60),
        "cook_time": random.randrange(1, 40),
        "description": f"Description-{uuid.uuid4()}",
        "image": open("tests/uploads/upload-image.png", 'rb'),
        "video": open("tests/uploads/upload-video.mp4", 'rb'),
    }

    response = api_client.post("/api/recipe/", recipe_data, format="multipart")
    assert response.status_code == 201

    recipe = Recipe.objects.get(name=recipe_data['name'])
    if original_recipe_pk:
        recipe.original_recipe_pk = original_recipe_pk
        recipe.language = "Bulgarian"
        recipe.save()

    return recipe, recipe_data


@pytest.mark.django_db
def create_ingredients_for_recipe(recipe: Recipe, api_client):
    ingredients_data = json.dumps([
        {"name": f"ingredient-{uuid.uuid4()}", "quantity": str(int(random.uniform(1, 100))), "metric": "pcs"},
        {"name": f"ingredient-{uuid.uuid4()}", "quantity": str(int(random.uniform(1, 100))), "metric": "tbsp"},
        {"name": f"ingredient-{uuid.uuid4()}", "quantity": str(int(random.uniform(1, 100))), "metric": "tbsp"}
    ])

    response = api_client.post(f"/api/recipe/{recipe.pk}/ingredients", data=ingredients_data,
                               content_type="application/json")
    assert response.status_code == 201

    ingredients = recipe.ingredient_set.all()
    return ingredients, json.loads(ingredients_data)


@pytest.mark.django_db
def create_steps_for_recipe(recipe: Recipe, api_client):
    steps_data = json.dumps([
        {"text": f"Prepare-{uuid.uuid4()}"},
        {"text": f"Mix-{uuid.uuid4()}"},
        {"text": f"Serve-{uuid.uuid4()}"},
        {"text": f"Enjoy-{uuid.uuid4()}"},
    ])

    response = api_client.post(f"/api/recipe/{recipe.pk}/steps", data=steps_data, content_type="application/json")
    assert response.status_code == 201

    steps = recipe.steps.all()
    return steps, json.loads(steps_data)


@pytest.mark.django_db
def test_create_admin_user(api_client):
    admin_user, admin_user_data = create_user(api_client)

    assert admin_user.username == admin_user_data['username']
    assert admin_user.is_superuser == True


@pytest.mark.django_db
def test_login_with_non_existing_user(api_client):
    login_data = {
        "email": "non_existing_user@email.com",
        "password": f"password-{random.uniform(1000, 100000)}"
    }
    response = api_client.post("/api/auth/token", login_data, format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_login_with_wrong_auth_header(api_client):
    admin_user, admin_user_data = create_user(api_client)
    api_client.credentials(HTTP_X_AUTH_HEADER=None)

    response = api_client.post("/api/auth/token", admin_user_data, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_user_creates_user_settings(api_client):
    add_access_token_header(api_client)
    response  = api_client.get("/api/auth/settings", format="json")

    assert response.status_code == 200
    response_content = json.loads(response.content)
    assert response_content['preferred_translate_language'] is None
    assert os.getenv("DEFAULT_RECIPE_DISPLAY_LANGUAGE") == "None"


@pytest.mark.django_db
def test_user_settings_are_changed_successfully(api_client):
    add_access_token_header(api_client)

    patch_request_data = {
        "language": "Bulgarian"
    }

    response =  api_client.patch("/api/auth/settings", patch_request_data, format="json")
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content['preferred_translate_language'] == patch_request_data['language']
    assert os.getenv("DEFAULT_RECIPE_DISPLAY_LANGUAGE") == patch_request_data['language']


@pytest.mark.django_db
def test_user_settings_are_returned_after_changes(api_client):
    add_access_token_header(api_client)

    patch_request_data = {
        "language": "Bulgarian"
    }

    response = api_client.patch("/api/auth/settings", patch_request_data, format="json")
    assert response.status_code == 201

    response = api_client.get("/api/auth/settings", format="json")
    response_content = json.loads(response.content)
    assert response_content['preferred_translate_language'] == patch_request_data['language']
    assert os.getenv("DEFAULT_RECIPE_DISPLAY_LANGUAGE") == patch_request_data['language']

@pytest.mark.django_db
def test_create_category(api_client):
    add_access_token_header(api_client)
    category, category_data = create_category(api_client)
    assert category.name == category_data['name']


@pytest.mark.django_db
def test_create_category_invalid_type(api_client):
    category_data = {
        "name": False
    }

    add_access_token_header(api_client)
    response = api_client.post("/api/recipe/category/add", category_data, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_category_without_token(api_client):
    category_data = {
        "name": False
    }

    response = api_client.post("/api/recipe/category/add", category_data, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_category(api_client):
    add_access_token_header(api_client)
    category, category_data = create_category(api_client)

    update_data = {
        "name": f"Category-{uuid.uuid4()}"
    }

    response = api_client.put(f"/api/recipe/category/{category.pk}", update_data, format="json")

    assert response.status_code == 200

    updated_category = Category.objects.get(pk=category.pk)
    assert updated_category.name == update_data['name']


@pytest.mark.django_db
def test_create_tag(api_client):
    add_access_token_header(api_client)
    tag, tag_data = create_tag(api_client)

    assert tag.name == tag_data['name']


@pytest.mark.django_db
def test_create_tag_incorrect_data(api_client):
    tag_data = {
        "name": False
    }

    add_access_token_header(api_client)
    response = api_client.post("/api/recipe/tag/add", tag_data, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_tag_without_token(api_client):
    tag_data = {
        "name": f"Tag-{uuid.uuid4()}"
    }

    response = api_client.post("/api/recipe/tag/add", tag_data, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_tag_name(api_client):
    add_access_token_header(api_client)
    tag, tag_data = create_tag(api_client)

    update_tag_data = {
        "name": f"Tag-{uuid.uuid4()}"
    }

    response = api_client.put(f"/api/recipe/tag/{tag.pk}", update_tag_data, format="json")
    assert response.status_code == 200

    tag = Tag.objects.get(pk=tag.pk)
    assert tag.name == update_tag_data['name']


@pytest.mark.django_db
def test_create_recipe(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    total = (int(recipe_data['prep_time']) + int(recipe_data['cook_time']))
    result_total_time = calculate_recipe_total_time(total)

    assert recipe.name == recipe_data['name']
    assert recipe.servings == recipe_data['servings']
    assert recipe.is_favorite == False
    assert recipe.tag.pk == recipe_data['tag']
    assert recipe.category.pk == recipe_data['category']
    assert recipe.created_at is not None
    assert recipe.image is not None
    assert recipe.video is not None
    assert recipe.prep_time == recipe_data['prep_time']
    assert recipe.cook_time == recipe_data['cook_time']
    assert recipe.total_time == result_total_time


@pytest.mark.django_db
def test_create_recipe_with_wrong_access_token(api_client):
    add_access_token_header(api_client)
    tag, tag_data = create_tag(api_client)
    category, category_data = create_category(api_client)

    recipe_data = {
        "name": f"Recipe-{uuid.uuid4()}",
        "servings": int(random.uniform(0, 20)),
        "category": category.pk,
        "tag": tag.pk,
        "prep_time": int(random.uniform(1, 60)),
        "image": open("tests/uploads/upload-image.png", 'rb'),
        "video": open("tests/uploads/upload-video.mp4", 'rb')
    }

    api_client.credentials(HTTP_AUTHORIZATION=f"Token {uuid.uuid4()}")
    response = api_client.post("/api/recipe/", recipe_data, format="multipart")
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_recipe_with_wrong_data(api_client):
    add_access_token_header(api_client)
    tag, tag_data = create_tag(api_client)
    category, category_data = create_category(api_client)

    recipe_data = {
        "name": f"Recipe-{uuid.uuid4()}",
        "servings": int(random.uniform(0, 20)),
        "category": "Category",
        "tag": tag.pk,
        "prep_time": int(random.uniform(1, 60)),
        "image": open("tests/uploads/upload-image.png", 'rb'),
        "video": open("tests/uploads/upload-video.mp4", 'rb')
    }

    api_client.credentials(HTTP_AUTHORIZATION=f"Token {uuid.uuid4()}")
    response = api_client.post("/api/recipe/", recipe_data, format="multipart")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_recipe_main_info(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    tag, tag_data = create_tag(api_client)
    category, category_data = create_category(api_client)

    update_recipe_data = {
        "name": f"Recipe-{uuid.uuid4()}",
        "servings": int(random.uniform(0, 20)),
        "category": category.pk,
        "tag": tag.pk,
        "description": f"Description{uuid.uuid4()}",
        "prep_time": int(random.uniform(1, 60)),
        "image": open("tests/uploads/upload-image.png", 'rb'),
        "video": open("tests/uploads/upload-video.mp4", 'rb')
    }

    response = api_client.put(f"/api/recipe/{recipe.pk}", update_recipe_data, format="multipart")
    assert response.status_code == 200

    updated_recipe = Recipe.objects.get(name=update_recipe_data['name'])
    assert updated_recipe.servings == update_recipe_data['servings']
    assert updated_recipe.tag.pk == tag.pk
    assert updated_recipe.description == update_recipe_data['description']
    assert updated_recipe.category.pk == category.pk
    assert updated_recipe.prep_time == update_recipe_data['prep_time']
    assert updated_recipe.image != recipe.image
    assert updated_recipe.video != recipe.video


@pytest.mark.django_db
def test_update_recipe_main_info_with_invalid_access_token(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    tag, tag_data = create_tag(api_client)
    category, category_data = create_category(api_client)

    update_recipe_data = {
        "name": f"Recipe-{uuid.uuid4()}",
        "servings": int(random.uniform(0, 20)),
        "category": category.pk,
        "tag": tag.pk,
        "prep_time": int(random.uniform(1, 60)),
        "image": open("tests/uploads/upload-image.png", 'rb'),
        "video": open("tests/uploads/upload-video.mp4", 'rb')
    }

    api_client.credentials(HTTP_AUTHORIZATION=f"Token {uuid.uuid4()}")
    response = api_client.put(f"/api/recipe/{recipe.pk}", update_recipe_data, format="multipart")
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_ingredients_for_recipe(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    ingredients, ingredients_data = create_ingredients_for_recipe(recipe, api_client)

    assert len(ingredients) == len(ingredients_data)
    assert len([x.name for x in ingredients if x.name in [y['name'] for y in ingredients_data]]) == len(ingredients)
    assert len([x.quantity for x in ingredients if x.quantity in [y['quantity'] for y in ingredients_data]]) == len(
        ingredients)
    assert len([x.metric for x in ingredients if x.metric in [y['metric'] for y in ingredients_data]]) == len(
        ingredients)


@pytest.mark.django_db
def test_create_ingredients_for_recipe_wrong_access_token(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)

    api_client.credentials(HTTP_AUTHORIZATION=f"Token {uuid.uuid4()}")

    ingredients_data = json.dumps([
        {"name": f"ingredient-{uuid.uuid4()}", "quantity": str(int(random.uniform(1, 100))), "metric": "pcs"},
        {"name": f"ingredient-{uuid.uuid4()}", "quantity": str(int(random.uniform(1, 100))), "metric": "tbsp"},
        {"name": f"ingredient-{uuid.uuid4()}", "quantity": str(int(random.uniform(1, 100))), "metric": "tbsp"}
    ])

    response = api_client.post(f"/api/recipe/{recipe.pk}/ingredients", data=ingredients_data,
                               content_type="application/json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_steps_for_recipe(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    steps, steps_data = create_steps_for_recipe(recipe, api_client)

    assert len(steps) == len(steps_data)
    assert len([x.text for x in steps if x.text in [y['text'] for y in steps_data]]) == len(steps)


@pytest.mark.django_db
def test_create_steps_for_recipe_wrong_access_token(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)

    api_client.credentials(HTTP_AUTHORIZATION=f"Token {uuid.uuid4()}")

    steps_data = json.dumps([
        {"text": f"Prepare-{uuid.uuid4()}"},
        {"text": f"Mix-{uuid.uuid4()}"},
        {"text": f"Serve-{uuid.uuid4()}"},
        {"text": f"Enjoy-{uuid.uuid4()}"},
    ])

    response = api_client.post(f"/api/recipe/{recipe.pk}/steps", data=steps_data, content_type="application/json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_steps_for_recipe_wrong_data(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)

    steps_data = json.dumps([
        {"text": False},
        {"text": f"Mix-{uuid.uuid4()}"},
        {"text": f"Serve-{uuid.uuid4()}"},
        {"text": f"Enjoy-{uuid.uuid4()}"},
    ])

    response = api_client.post(f"/api/recipe/{recipe.pk}/steps", data=steps_data, content_type="application/json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_favorite_a_recipe(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    remove_access_token_header_and_add_header_secret(api_client)

    response = api_client.patch(f"/api/recipe/{recipe.pk}/favorite", format="json")
    assert response.status_code == 201

    recipe = Recipe.objects.get(pk=recipe.pk)
    assert recipe.is_favorite == True


@pytest.mark.django_db
def test_unfavorite_recipe(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    remove_access_token_header_and_add_header_secret(api_client)

    response = api_client.patch(f"/api/recipe/{recipe.pk}/favorite", format="json")
    assert response.status_code == 201

    response = api_client.patch(f"/api/recipe/{recipe.pk}/favorite", format="json")
    assert response.status_code == 201

    recipe = Recipe.objects.get(pk=recipe.pk)
    assert recipe.is_favorite == False


@pytest.mark.django_db
def test_favorite_recipe_without_auth_header(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    api_client.credentials()

    response = api_client.patch(f"/api/recipe/{recipe.pk}/favorite", format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_favorite_non_existing_recipe(api_client):
    response = api_client.patch("/api/recipe/202/favorite", format="json")

    assert response.status_code == 404


@pytest.mark.django_db
def test_get_favorite_recipes(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    second_recipe, second_recipe_data = create_recipe(api_client)

    remove_access_token_header_and_add_header_secret(api_client)

    api_client.patch(f"/api/recipe/{recipe.pk}/favorite", format="json")
    api_client.patch(f"/api/recipe/{second_recipe.pk}/favorite", format="json")

    response = api_client.get("/api/recipe/home/favorites/", format="json")
    assert response.status_code == 200
    favorite_recipes = Recipe.objects.filter(is_favorite=True).all()

    assert len(favorite_recipes) == 2
    assert len([x for x in favorite_recipes if x.pk == recipe.pk or second_recipe.pk]) == 2

    response_data = json.loads(response.content)

    assert len([x.name for x in favorite_recipes if x.name in [y['name'] for y in response_data['results']]]) == 2
    assert len([x.is_favorite for x in favorite_recipes if
                x.is_favorite in [y['is_favorite'] for y in response_data['results']]]) == 2
    assert response_data['count'] == 2


@pytest.mark.django_db
def test_get_favorites_no_recipes_match(api_client):
    response = api_client.get("/api/recipe/home/favorites/", format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_favorites_no_secret_header(api_client):
    api_client.credentials()
    response = api_client.get("/api/recipe/home/favorites/", format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_get_trending_recipes(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    second_recipe, second_recipe_data = create_recipe(api_client)

    remove_access_token_header_and_add_header_secret(api_client)

    response = api_client.get("/api/recipe/trending", format="json")
    assert response.status_code == 200

    response_data = json.loads(response.content)
    assert len([x for x in response_data if x['name'] == recipe.name or x['name'] == second_recipe_data['name']]) == 2
    assert response_data[0]['name'] != response_data[1]['name']


@pytest.mark.django_db
def test_get_trending_recipes_without_auth_header(api_client):
    api_client.credentials()

    response = api_client.get("/api/recipe/trending", format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_recipe_by_name(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    create_recipe(api_client)

    remove_access_token_header_and_add_header_secret(api_client)

    response = api_client.get(f"/api/recipe/home/?search={recipe.name}", format="json")
    assert response.status_code == 200

    response_data = json.loads(response.content)
    assert response_data['count'] == 1
    assert response_data['results'][0]['name'] == recipe.name


@pytest.mark.django_db
def test_get_recipe_by_name_without_secret_header(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    api_client.credentials()

    response = api_client.get(f"/api/recipe/home/?search={recipe.name}", format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_recipe_without_query_parameter(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    second_recipe, second_recipe_data = create_recipe(api_client)

    remove_access_token_header_and_add_header_secret(api_client)

    response = api_client.get(f"/api/recipe/home/", format="json")
    assert response.status_code == 200

    response_data = json.loads(response.content)
    assert response_data['count'] == 2
    assert len(
        [x for x in response_data['results'] if x['name'] == recipe.name or x['name'] == second_recipe.name]) == 2


@pytest.mark.django_db
def test_get_recipe_return_recipe_main_info(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)

    remove_access_token_header_and_add_header_secret(api_client)
    response = api_client.get(f"/api/recipe/home/", format="json")

    assert response.status_code == 200

    response_data = json.loads(response.content)
    assert recipe.name == response_data['results'][0]['name']
    assert recipe.servings == response_data['results'][0]['servings']
    assert recipe.prep_time == response_data['results'][0]['prep_time']
    assert recipe.video is not None
    assert recipe.image is not None
    assert recipe.is_favorite == response_data['results'][0]['is_favorite']
    assert recipe.category.pk == response_data['results'][0]['category']
    assert recipe.tag.pk == response_data['results'][0]['tag']


@pytest.mark.django_db
def test_get_recipe_return_full_info(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    ingredients, ingredients_data = create_ingredients_for_recipe(recipe, api_client)
    steps, steps_data = create_steps_for_recipe(recipe, api_client)

    remove_access_token_header_and_add_header_secret(api_client)
    response = api_client.get(f"/api/recipe/home/", format="json")
    assert response.status_code == 200

    response_data = json.loads(response.content)

    assert recipe.name == response_data['results'][0]['name']
    assert recipe.servings == response_data['results'][0]['servings']
    assert recipe.prep_time == response_data['results'][0]['prep_time']
    assert recipe.video is not None
    assert recipe.image is not None
    assert recipe.is_favorite == response_data['results'][0]['is_favorite']
    assert recipe.category.pk == response_data['results'][0]['category']
    assert recipe.tag.pk == response_data['results'][0]['tag']

    assert len(ingredients) == len([x for x in response_data['results'][0]['ingredients']])
    assert len(steps) == len([x for x in response_data['results'][0]['steps']])


@pytest.mark.django_db
def test_delete_recipe(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)

    response = api_client.delete(f"/api/recipe/{recipe.pk}/", format="json")
    assert response.status_code == 204

    with pytest.raises(Recipe.DoesNotExist):
        Recipe.objects.get(pk=recipe.pk)


@pytest.mark.django_db
def test_delete_recipe_without_access_token_header(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)

    remove_access_token_header_and_add_header_secret(api_client)
    response = api_client.delete(f"/api/recipe/{recipe.pk}/", format="json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_ingredients_second_time_rewrite_existing(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    ingredients, ingredients_data = create_ingredients_for_recipe(recipe, api_client)
    second_ingredients, second_ingredients_data = create_ingredients_for_recipe(recipe, api_client)
    print(ingredients)
    print(second_ingredients)
    assert len(second_ingredients) == len(second_ingredients_data)
    assert len([x for x in ingredients if x.name not in [y.name for y in second_ingredients]]) == 0


@pytest.mark.django_db
def test_create_steps_second_time_rewrite_existing(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    steps, steps_data = create_steps_for_recipe(recipe, api_client)
    second_steps, second_steps_data = create_steps_for_recipe(recipe, api_client)

    assert len(second_steps) == len(second_steps_data)
    assert len([x for x in steps if x.text not in [y.text for y in second_steps]]) == 0


@pytest.mark.django_db
def test_delete_user_account(api_client):
    token, admin_user, admin_user_data = get_token_and_admin_user(api_client)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    response = api_client.delete("/api/auth/delete-account")
    assert response.status_code == 204

    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=admin_user.pk)


@pytest.mark.django_db
def test_delete_user_non_existing_token(api_client):
    get_token_and_admin_user(api_client)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token f6ecfd953ab8b1f2e0c6ab866ab4c62e24c24c9d")

    response = api_client.delete("/api/auth/delete-account")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_user_password(api_client):
    admin_user, new_user_data, password_data = request_password_reset_for_user(api_client)
    remove_access_token_header_and_add_header_secret(api_client)

    response = api_client.post("/api/auth/token", new_user_data, format="json")
    assert response.status_code == 200

    token = Token.objects.get(user=admin_user)
    assert token is not None


@pytest.mark.django_db
def test_update_password_user_cant_login_with_old_password(api_client):
    admin_user, new_user_data, password_data = request_password_reset_for_user(api_client)
    remove_access_token_header_and_add_header_secret(api_client)

    old_password_data = {
        "email": admin_user.email,
        "password": password_data['old_password']
    }

    response = api_client.post("/api/auth/token", old_password_data, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_user_username_and_email(api_client):
    user_data, admin_user = request_user_patch_request(api_client, UserUpdateDetailsEnum.BOTH)

    user_by_username = User.objects.get(username=user_data['username'])
    user_by_email = User.objects.get(email=user_data['email'])

    assert user_by_username == user_by_email


@pytest.mark.django_db
def test_old_username_is_not_available_when_change_it(api_client):
    user_data, admin_user = request_user_patch_request(api_client, UserUpdateDetailsEnum.USERNAME)

    with pytest.raises(User.DoesNotExist):
        User.objects.get(username=admin_user.username)


@pytest.mark.django_db
def test_old_email_is_not_available_when_change_it(api_client):
    user_data, admin_user = request_user_patch_request(api_client, UserUpdateDetailsEnum.EMAIL)

    with pytest.raises(User.DoesNotExist):
        User.objects.get(username=admin_user.email)


@pytest.mark.django_db
def test_request_change_password_token(api_client):
    response_data, data = request_password_reset_token(api_client)
    token = PasswordResetToken.objects.get(email=data['email'])

    assert token.email == data['email']
    assert token.token == response_data['token']
    assert token.created_at is not None


@pytest.mark.django_db
def test_request_change_password_invalid_email(api_client):
    data = {
        "email": f"email-{uuid.uuid4()}@email.com"
    }

    response = api_client.post("/api/auth/password_reset", data=data, format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_change_password_with_token(api_client):
    response_data, data = request_password_reset_token(api_client)
    api_client.credentials()

    new_password = f"password-{uuid.uuid4()}"

    change_password_data = {
        "password": new_password,
        "confirm_password": new_password
    }

    response = api_client.post(f"/api/auth/password_reset/reset?token={response_data['token']}",
                               data=change_password_data, format="json")
    assert response.status_code == 204


@pytest.mark.django_db
def test_change_password_with_token_passwords_does_not_match(api_client):
    response_data, data = request_password_reset_token(api_client)
    api_client.credentials()

    change_password_data = {
        "password": f"password-{uuid.uuid4()}",
        "confirm_password": f"password-{uuid.uuid4()}"
    }

    response = api_client.post(f"/api/auth/password_reset/reset?token={response_data['token']}",
                               data=change_password_data, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_change_password_invalid_token(api_client):
    request_password_reset_token(api_client)
    api_client.credentials()
    new_password = f"password-{uuid.uuid4()}"

    change_password_data = {
        "password": new_password,
        "confirm_password": new_password
    }

    response = api_client.post(f"/api/auth/password_reset/reset?token={uuid.uuid4()}", data=change_password_data,
                               format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_change_password_password_validation_logged_user(api_client):
    response, response_data = password_change_for_validation(api_client, PasswordResetChoice.SHORT_ENTRY)

    assert response.status_code == 400
    assert LENGTH_PASSWORD_ERROR_MESSAGE in response_data['errors']
    assert PASSWORD_TO_COMMON_ERROR_MESSAGE in response_data['errors']
    assert len(response_data['errors']) == 2


@pytest.mark.django_db
def test_change_password_password_validation_old_password_does_not_match_logged_user(api_client):
    response, response_data = password_change_for_validation(api_client, PasswordResetChoice.NON_MATCHING)

    assert response.status_code == 400
    assert OLD_PASSWORD_DOES_NOT_MATCH_ERROR_MESSAGE in response_data['errors']
    assert len(response_data['errors']) == 1


@pytest.mark.django_db
def test_change_password_password_validation_number_only_logged_user(api_client):
    response, response_data = password_change_for_validation(api_client, PasswordResetChoice.NUMERIC)

    assert response.status_code == 400
    assert NUMERIC_PASSWORD_ERROR_MESSAGE in response_data['errors']
    assert len(response_data['errors']) == 1


@pytest.mark.django_db
def test_change_password_numeric_validation_request_reset(api_client):
    response, response_data = request_change_password_validation(api_client, PasswordResetChoice.NUMERIC)

    assert response.status_code == 400
    assert NUMERIC_PASSWORD_ERROR_MESSAGE in response_data['errors']
    assert len(response_data['errors']) == 1


@pytest.mark.django_db
def test_change_password_on_reset_validations_length(api_client):
    response, response_data = request_change_password_validation(api_client, PasswordResetChoice.SHORT_ENTRY)

    assert LENGTH_PASSWORD_ERROR_MESSAGE in response_data['errors']
    assert PASSWORD_TO_COMMON_ERROR_MESSAGE in response_data['errors']
    assert len(response_data['errors']) == 2


@pytest.mark.django_db
def test_change_password_on_reset_passwords_does_not_match(api_client):
    response, response_data = request_change_password_validation(api_client, PasswordResetChoice.NON_MATCHING)

    assert response.status_code == 400
    assert CONFIRM_AND_NEW_PASSWORD_DOES_NOT_MATCH_ERROR_MESSAGE in response_data['errors']
    assert len(response_data['errors']) == 1

@pytest.mark.django_db
def test_translate_recipe_return_none_for_default_user_settings_none_on_post(api_client):
    add_access_token_header(api_client)
    response = api_client.post("/api/recipe/translate", format="json")

    assert response.status_code == 400
    response_json_content = json.loads(response.content)
    assert "Default language for translation should be set" in response_json_content['errors']


@pytest.mark.django_db
def test_translate_recipe_without_request_data_language_and_the_recipe_is_original_false(api_client):
    add_access_token_header(api_client)
    recipe, recipe_data = create_recipe(api_client)
    recipe, recipe_data = create_recipe(api_client, original_recipe_pk=recipe.pk)
    os.environ["DEFAULT_RECIPE_DISPLAY_LANGUAGE"] = "Bulgarian"

    json_data = {
        "pk": recipe.pk
    }

    response = api_client.post("/api/recipe/translate", json_data, format="json")
    assert response.status_code == 400
    response_json_content = json.loads(response.content)

    assert "Translation must be performed only on original recipes" in response_json_content['errors']

@pytest.mark.django_db
def test_translate_translated_recipe_same_language(api_client):
    add_access_token_header(api_client)
    original_recipe, recipe_data = create_recipe(api_client)
    create_recipe(api_client, original_recipe_pk=original_recipe.pk)
    os.environ["DEFAULT_RECIPE_DISPLAY_LANGUAGE"] = "Bulgarian"

    json_data = {
        "pk": original_recipe.pk,
        "language": "Bulgarian"
    }

    response = api_client.post("/api/recipe/translate", json_data, format="json")
    assert response.status_code == 400
    response_json_content = json.loads(response.content)

    assert "Translation language is already used and there a recipe translated with that language." in response_json_content['errors']

@pytest.mark.django_db
def test_get_recipe_variations(api_client):
    add_access_token_header(api_client)
    original_recipe, recipe_data = create_recipe(api_client)
    second_recipe, recipe_data = create_recipe(api_client, original_recipe_pk=original_recipe.pk)
    third_recipe, recipe_data = create_recipe(api_client, original_recipe_pk=original_recipe.pk)
    remove_access_token_header_and_add_header_secret(api_client)

    response = api_client.get(f"/api/recipe/{original_recipe.pk}/variations", format="json")
    assert response.status_code == 200

    response_content = json.loads(response.content)
    assert (second_recipe.pk and third_recipe.pk and original_recipe.pk) in [x['pk'] for x in response_content]
