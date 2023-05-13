import json
from src.addon_manager import (
    AddonManager,
    Item,
    Block,
    CreativeCategory,
    CraftingRecipeShapeless,
    RecipeIngredient,
)
from src.util import error, OUT_DIRECTORY, DEFAULTS_PATH


def main():
    if not OUT_DIRECTORY.exists():
        print("'./out' doesn't exist, creating it...")
        OUT_DIRECTORY.mkdir()

    if not OUT_DIRECTORY.is_dir():
        error("'./out' must be a directory!")

    input(
        "WARNING: If you continue, any files in './out' will be erased! (Enter to continue)"
    )

    name = "Template Addon"
    description = "A bedrock addon created using sammwi's AddonManager!"
    namespace = "template_addon"

    if not DEFAULTS_PATH.exists() and not DEFAULTS_PATH.suffix == ".json":
        print(
            "Couldn't find defaults in current folder, proceeding with hardcoded defaults..."
        )
    else:
        print("Found defaults in current folder, proceeding...")
        parsed = dict(json.loads(s=DEFAULTS_PATH.read_text(encoding="utf-8")))
        name = parsed.get("name", name)
        description = parsed.get("description", description)
        namespace = parsed.get("namespace", namespace)

    manager = AddonManager(name, description, namespace)

    manager.add_item(
        item=Item()
        .set_id("pie")
        .set_display_name("Pie")
        .set_category(CreativeCategory.NATURE)
        .set_max_stack_size(5)
        .set_food(10)
    )

    manager.add_item(
        item=Item()
        .set_id("pizza")
        .set_display_name("Pizza")
        .set_category(CreativeCategory.NATURE)
        .set_max_stack_size(4)
        .set_food(4)
    )

    manager.add_item(
        item=Item()
        .set_id("ice_cream")
        .set_display_name("Ice Cream")
        .set_category(CreativeCategory.NATURE)
        .set_max_stack_size(2)
        .set_food(1)
    )

    manager.add_item(
        item=Item()
        .set_id("fanta")
        .set_display_name("Fanta")
        .set_category(CreativeCategory.NATURE)
        .set_max_stack_size(1)
        .set_food(3)
    )

    manager.add_block(
        block=Block()
        .set_id("leather_block")
        .set_display_name("Leather Block")
        .set_category(CreativeCategory.NATURE)
        .set_hardness(1.5)
        .set_texture_path("textures/blocks/stone")
        .set_recipe(
            recipe=CraftingRecipeShapeless().set_ingredients(
                [RecipeIngredient(item_id="minecraft:leather", count=9)]
            )
        )
    )

    manager.generate()
    print("\nFinished!")


if __name__ == "__main__":
    main()
