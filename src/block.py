import enum
# If you have a linter/pylint, it will show these as errors but it works and I don't know how to remove the error
from .block_sounds import BlockSounds
from .constants import FORMAT_VERSION_BLOCK
from .creative_category import CreativeCategory
from .recipes import CraftingRecipeShapeless, CraftingRecipeShaped

# https://wiki.bedrock.dev/blocks/blocks-stable.html#minecraft-material-instances
# https://wiki.bedrock.dev/blocks/blocks-stable.html#additional-notes
class RenderMethod(enum.Enum):
    BLEND = "blend"
    OPAQUE = "opaque"
    TRANSPARENT = "alpha_test"

# https://wiki.bedrock.dev/blocks/blocks-stable.html
class Block:
    """
    A minecraft bedrock block
    """

    id: str
    display_name: str
    texture_path: str | None
    category: CreativeCategory
    sound: BlockSounds

    hardness: int | float
    resistance: int
    render_method: RenderMethod
    has_gravity: bool

    recipe: CraftingRecipeShaped | CraftingRecipeShapeless | None

    def __init__(self) -> None:
        self.id = "placeholder"
        self.display_name = "Placeholder"
        self.texture_path = (
            None  # If None, it will use the default path that uses id as file name
        )
        self.category = CreativeCategory.CONSTRUCTION
        self.sound = BlockSounds.STONE
        self.hardness = 1
        self.resistance = 1
        self.render_method = RenderMethod.BLEND
        self.has_gravity = False
        self.recipe = None

    def set_id(self, block_id: str):
        """
        Sets the blocks id
        """
        self.id = block_id
        return self

    def set_display_name(self, display_name: str):
        """
        Sets the blocks display name
        """
        self.display_name = display_name
        return self

    def set_texture_path(self, texture_path: str):
        """
        Sets the blocks texture path (if not provided, it will use default that uses id for file name in textures/blocks/id)
        """
        self.texture_path = texture_path
        return self

    def set_category(self, category: CreativeCategory):
        """
        Sets the blocks creative tab/category
        """
        self.category = category
        return self

    def set_sound(self, sound: BlockSounds):
        """
        Sets the blocks sound when walked on or used
        """
        self.sound = sound
        return self

    def set_hardness(self, hardness: int | float):
        """
        Sets the blocks hardness (how long it takes to break in seconds)
        """
        self.hardness = hardness
        return self

    def set_resistance(self, resistance: int):
        """
        Sets the blocks resistance (how much of a chance it will break from a explosion)
        """
        self.resistance = resistance
        return self

    def set_render_method(self, render_method: RenderMethod):
        """
        Sets the blocks rendering method (how it looks ingame, like if its transparent or opaque, etc..)
        """
        self.render_method = render_method
        return self

    def set_has_gravity(self, has_gravity: bool = True):
        self.has_gravity = has_gravity
        return self

    def set_recipe(self, recipe: CraftingRecipeShaped | CraftingRecipeShapeless):
        """
        Sets the recipe for the block
        """
        self.recipe = recipe
        self.recipe.item_id = self.id
        self.recipe.result_item_id = self.id
        return self

    def construct(self, namespace: str) -> dict:
        """
        Returns the block json used inside a behaviour pack
        """
        return {
            "format_version": FORMAT_VERSION_BLOCK,
            "minecraft:block": {
                "description": {
                    "identifier": f"{namespace}:{self.id}",
                    "register_to_creative_menu": True,
                    "menu_category": {
                        "category": self.category.value,
                    },
                },
                "components": {
                    "minecraft:display_name": self.display_name,
                    "minecraft:material_instances": {
                        "*": {
                            "texture": f"{namespace}:{self.id}",
                            "render_method": self.render_method.value,
                        }
                    },
                    "minecraft:destructible_by_mining": {
                        "seconds_to_destroy": self.hardness
                    },
                    "minecraft:destructible_by_explosion": {
                        "explosion_resistance": self.resistance
                    },
                },
            },
        }