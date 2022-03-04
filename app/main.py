from typing import Optional

from fastapi import FastAPI, APIRouter, Query

from app.models import RECIPES, Recipe
from app.schemas import RecipeSearchResults, RecipeCreate

app = FastAPI(
    title='Recipe API', openapi_url='/openapi.json'
)

api_router = APIRouter()


@api_router.get('/', status_code=200)
def root() -> dict:
    """
    GET: Root
    :return:
    """
    return {'msg': "Hello. World!"}


@api_router.get('/recipe/{recipe_id}/', status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int) -> dict:
    """
    GET: Recipe by ID
    :param recipe_id:
    :return:
    """
    result = None
    results = [recipe for recipe in RECIPES if recipe.id == recipe_id]
    if len(results):
        result = results[0]
    return result


@api_router.get('/search/', status_code=200, response_model=RecipeSearchResults)
def search_recipes(keyword: Optional[str] = Query(None, min_length=3, example='chicken'),
                   max_results: Optional[int] = 10) -> dict:
    """
    GET: Search recipes by keyword
    :param keyword:
    :param max_results:
    :return:
    """
    if not keyword:
        return {'results': RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), RECIPES)
    return {'results': list(results)[:max_results]}


@api_router.post('/recipe/', status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate) -> dict:
    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url
    )
    RECIPES.append(recipe_entry.dict())
    return recipe_entry.dict()


app.include_router(api_router)
