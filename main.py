import pathlib, json, os
from addon_manager import AddonManager, ItemBuilder
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
    manager.add_item(id="pie", display_name="Pie", stack_size=64)
    manager.add_item(id="pizza", display_name="Pizza", stack_size=4)
    manager.add_item(id="ice_cream", display_name="Ice Cream", stack_size=2)
    manager.add_item(id="fanta", display_name="Fanta", stack_size=1)
    # manager.add_item(ItemBuilder()


if __name__ == "__main__":
    main()
