import os, uuid, random, pytest, json

from authentication.models import User
from recipe.models import Category, Tag, Recipe, Ingredient
from rest_framework.authtoken.models import Token
from dotenv import load_dotenv
from rest_framework.test import APIClient

load_dotenv()


@pytest.fixture(scope="function")
def api_client():
    client = APIClient()
    client.credentials(HTTP_X_AUTH_HEADER=os.getenv('X_AUTH_HEADER'))

    return client


@pytest.mark.django_db
def create_user(api_client):
    admin_user_data = {
        "username": f"admin-{random.uniform(0, 10000)}",
        "password": "test123",
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
def create_recipe(api_client):
    tag, tag_data = create_tag(api_client)
    category, category_data = create_category(api_client)

    recipe_data = {
        "name": f"Recipe-{uuid.uuid4()}",
        "serves": int(random.uniform(0, 20)),
        "category": category.pk,
        "tag": tag.pk,
        "prep_time": int(random.uniform(1, 60)),
        "image": open("tests/uploads/upload-image.png", 'rb'),
        "video": open("tests/uploads/upload-video.mp4", 'rb')
    }

    response = api_client.post("/api/recipe/", recipe_data, format="multipart")
    assert response.status_code == 201
    recipe = Recipe.objects.get(name=recipe_data['name'])

    return recipe, recipe_data

@pytest.mark.django_db
def create_ingredients_for_recipe(recipe: Recipe, api_client):

    ingredients = [
        {"name": f"ingredient-{uuid.uuid4()}", "quantity": str(random.uniform(1, 100)), "metric": "pcs"},
        {"name": f"ingredient-{uuid.uuid4()}", "quantity": str(random.uniform(1, 100)), "metric": "tbsp"},
        {"name": f"ingredient-{uuid.uuid4()}", "quantity": str(random.uniform(1, 100)), "metric": "tbsp"}
    ]

    response = api_client.post(f"/api/recipe/{recipe.pk}/ingredients", json=ingredients, format="json")
    print(response.content)
    assert response.status_code == 201
    ingredients = Ingredient.objects.select_related(recipe=recipe).all()
    print(ingredients)
    return ingredients, ingredients



@pytest.mark.django_db
def test_create_admin_user(api_client):
    admin_user, admin_user_data = create_user(api_client)

    assert admin_user.username == admin_user_data['username']
    assert admin_user.is_superuser == True


@pytest.mark.django_db
def test_login_with_non_existing_user(api_client):
    login_data = {
        "username": "non_existing_user",
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

    assert recipe.name == recipe_data['name']
    assert recipe.serves == recipe_data['serves']
    assert recipe.is_favorite == False
    assert recipe.tag.pk == recipe_data['tag']
    assert recipe.category.pk == recipe_data['category']
    assert recipe.created_at is not None
    assert recipe.image is not None
    assert recipe.video is not None
    assert recipe.prep_time == recipe_data['prep_time']


@pytest.mark.django_db
def test_create_recipe_with_wrong_access_token(api_client):
    add_access_token_header(api_client)
    tag, tag_data = create_tag(api_client)
    category, category_data = create_category(api_client)

    recipe_data = {
        "name": f"Recipe-{uuid.uuid4()}",
        "serves": int(random.uniform(0, 20)),
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
        "serves": int(random.uniform(0, 20)),
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
        "serves": int(random.uniform(0, 20)),
        "category": category.pk,
        "tag": tag.pk,
        "prep_time": int(random.uniform(1, 60)),
        "image": open("tests/uploads/upload-image.png", 'rb'),
        "video": open("tests/uploads/upload-video.mp4", 'rb')
    }

    response = api_client.put(f"/api/recipe/{recipe.pk}", update_recipe_data, format="multipart")
    assert response.status_code == 200

    updated_recipe = Recipe.objects.get(name=update_recipe_data['name'])
    assert updated_recipe.serves == update_recipe_data['serves']
    assert updated_recipe.tag.pk == tag.pk
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
        "serves": int(random.uniform(0, 20)),
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

    assert ingredients.recipe == recipe
    assert ingredients