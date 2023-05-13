# If you have a linter/pylint, it will show these as errors but it works and I don't know how to remove the error
from .constants import FORMAT_VERSION_RECIPE

class CraftingRecipeShaped:
    """
    A minecraft bedrock shaped crafting recipe
    """

    item_id: str
    pattern: list[str]
    result_item_id: str

    def __init__(self) -> None:
        self.item_id = ""
        self.pattern = []
        self.result_item_id = ""

    def set_item_id(self, item_id: str):
        """
        Set the item the recipe is being used for
        """
        self.item_id = item_id
        return self

    def set_pattern(self, pattern: list[str]):
        """
        Set the shape of the recipe
        """
        self.pattern = pattern
        return self

    def set_result_item_id(self, result_item_id: str):
        """
        Set the result item of the recipe
        """
        self.result_item_id = result_item_id
        return self

    def construct(self, namespace: str) -> dict:
        """
        Returns the shaped recipe json used inside a behaviour pack
        """
        return {
            "format_version": FORMAT_VERSION_RECIPE,
            "minecraft:recipe_shaped": {
                "description": {"identifier": f"{namespace}:{self.item_id}"},
                "tags": ["crafting_table"],
                "pattern": self.pattern,
                "key": {
                    # TODO: work this out
                },
                "result": f"{namespace}:{self.item_id}",
            },
        }

class RecipeIngredient:
    """
    A minecraft bedrock shapeless recipe ingredient
    """

    item_id: str
    count: int

    def __init__(self, item_id: str, count: int = 1) -> None:
        self.item_id = item_id
        if count <= 0:
            raise Exception(
                "RecipeIngredients must have a greater or equal to 1 count."
            )
        self.count = count

    def construct(self) -> dict:
        return {"item": self.item_id, "count": self.count}


class CraftingRecipeShapeless:
    """
    A minecraft bedrock shapeless crafting recipe
    """

    item_id: str
    ingredients: list[RecipeIngredient]
    result_item_id: str

    def __init__(self) -> None:
        self.item_id = ""
        self.ingredients = []
        self.result_item_id = ""

    def set_item_id(self, item_id: str):
        self.item_id = item_id
        return self

    def set_ingredients(self, ingredients: list[RecipeIngredient]):
        self.ingredients = ingredients
        return self

    def set_result_item_id(self, result_item_id: str):
        self.result_item_id = result_item_id
        return self

    def construct(self, namespace: str) -> dict:
        """
        Returns the shaped recipe json used inside a behaviour pack
        """
        return {
            "format_version": FORMAT_VERSION_RECIPE,
            "minecraft:recipe_shapeless": {
                "description": {"identifier": f"{namespace}:{self.item_id}"},
                "tags": ["crafting_table"],
                "ingredients": [
                    ingredient.construct() for ingredient in self.ingredients
                ],
                "result": {"item": f"{namespace}:{self.result_item_id}"},
            },
        }
