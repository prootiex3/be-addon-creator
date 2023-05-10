import pathlib, json, os
from addon_manager import AddonManager, Item
from util import error, OUT_DIRECTORY


def main():
    if not OUT_DIRECTORY.exists():
        print("'./out' doesn't exist, creating it...")
        OUT_DIRECTORY.mkdir()

    if not OUT_DIRECTORY.is_dir():
        error("'./out' must be a directory!")

    input(
        "WARNING: If you continue, any files in './out' will be erased! (Enter to continue)"
    )

    defaults_path = pathlib.Path("./defaults.json")
    if not defaults_path.exists():
        name = input("Name of your addon (has default): ")
        description = input("Description of your addon (has default): ")
    else:
        print("Found defaults in current folder, proceeding...")
        name = "Template Addon"
        description = "A bedrock addon created using sammwi's AddonManager!"
        try:
            parsed = dict(json.loads(defaults_path.read_text()))
            name = parsed.get("name", name)
            description = parsed.get("description", description)
        except:
            print(f"Failed to use defaults, using local defaults instead...")
    manager = AddonManager(name, description)
    manager.initalize()

    manager.add_item(
        item=Item()
        .set_id("pie")
        .set_display_name("Pie")
        .set_max_stack_size(64)
        .set_food(10)
    )

    manager.add_item(
        item=Item()
        .set_id("pizza")
        .set_display_name("Pizza")
        .set_max_stack_size(4)
        .set_food(4)
    )

    manager.add_item(
        item=Item()
        .set_id("ice_cream")
        .set_display_name("Ice Cream")
        .set_max_stack_size(2)
        .set_food(1)
    )

    manager.add_item(
        item=Item()
        .set_id("fanta")
        .set_display_name("Fanta")
        .set_max_stack_size(1)
        .set_food(3)
    )


if __name__ == "__main__":
    main()
