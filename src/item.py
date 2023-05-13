# If you have a linter/pylint, it will show these as errors but it works and I don't know how to remove the error
from .constants import FORMAT_VERSION_ITEM
from .creative_category import CreativeCategory
from .recipe import CraftingRecipeShapeless, CraftingRecipeShaped

# https://wiki.bedrock.dev/items/items-16.html
# Requires Holiday Features Enabled (as of May 12th, 2023)
class Item:
    """
    A minecraft bedrock item
    """

    id: str
    display_name: str
    texture_path: str | None
    category: CreativeCategory
    max_stack_size: int
    will_despawn: bool

    is_food: bool
    food_bars: int
    use_duration: int | float

    enchanted: bool
    allow_off_hand: bool

    recipe: CraftingRecipeShaped | CraftingRecipeShapeless | None

    def __init__(self) -> None:
        self.id = "placeholder"
        self.display_name = "Placeholder"
        self.texture_path = (
            None  # If None, it will use the default path that uses id as file name
        )
        self.category = CreativeCategory.CONSTRUCTION
        self.max_stack_size = 64
        self.will_despawn = True

        self.is_food = False
        self.food_bars = 0
        self.use_duration = 5

        self.enchanted = False
        self.allow_off_hand = False

        self.recipe = None

    def set_id(self, item_id: str):
        """
        Sets the items id
        """
        self.id = item_id
        return self

    def set_display_name(self, display_name: str):
        """
        Sets the items display name
        """
        self.display_name = display_name
        return self

    def set_texture_path(self, texture_path: str):
        """
        Sets the items texture path (if not provided, it will use default that uses id for file name in textures/items/id)
        """
        self.texture_path = texture_path
        return self

    def set_category(self, category: CreativeCategory):
        """
        Sets the items creative tab/category
        """
        self.category = category
        return self

    def set_max_stack_size(self, max_stack_size: int):
        """
        Set the max number the item can stack to
        """
        self.max_stack_size = max_stack_size
        return self

    def set_will_despawn(self, should_despawn: bool):
        """
        Set if the item should/will despawn
        """
        self.will_despawn = should_despawn
        return self

    def set_food(self, bars: int):
        """
        Sets is_food on the item and sets the value for the food consumption (food_bars)
        """
        self.is_food = True
        self.food_bars = bars
        return self

    def set_use_duration(self, seconds: int | float):
        """
        Sets how many seconds it takes to eat the food (Only applies if item is a food)
        """
        self.use_duration = seconds
        return self

    def set_enchanted(self):
        """
        Makes the item look enchanted
        """
        self.enchanted = True
        return self

    def set_allow_off_hand(self):
        """
        Allow using the item in the offhand slot (False by default)
        """
        self.allow_off_hand = True
        return self

    def set_recipe(self, recipe: CraftingRecipeShaped | CraftingRecipeShapeless):
        """
        Sets the recipe for the item
        """
        self.recipe = recipe
        self.recipe.item_id = self.id
        self.recipe.result_item_id = self.id
        return self

    def construct(self, namespace: str) -> dict:
        """
        Returns the item json used inside a behaviour pack
        """
        data = {
            "format_version": FORMAT_VERSION_ITEM,
            "minecraft:item": {
                "description": {
                    "identifier": f"{namespace}:{self.id}",
                    "category": self.category.value,
                },
                "components": {
                    "minecraft:display_name": {"value": self.display_name},
                    "minecraft:icon": {"texture": f"{namespace}:{self.id}"},
                    "minecraft:max_stack_size": self.max_stack_size,
                    "minecraft:foil": self.enchanted,
                    "minecraft:hand_equipped": True,
                    "minecraft:should_despawn": self.will_despawn,
                },
            },
        }

        if self.is_food:
            data["minecraft:item"]["components"][
                "minecraft:use_duration"
            ] = self.use_duration
            data["minecraft:item"]["components"]["minecraft:food"] = {
                "nutrition": self.food_bars
            }
            # TODO: allow using animation: drink
            data["minecraft:item"]["components"]["minecraft:use_animation"] = "eat"
            # TODO: figure out how to use this/make it look like an apple as base?
            data["minecraft:item"]["components"]["minecraft:render_offsets"] = {
                "main_hand": {
                    "position": [1, 1, 1],
                    "rotation": [1, 1, 1],
                    "scale": [1, 1, 1],
                }
            }

        return data