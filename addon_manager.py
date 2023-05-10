import pathlib, json, uuid, shutil
from util import error, OUT_DIRECTORY
from enum import Enum

# TODO: maybe make these editable?
FORMAT_VERSION = 2
FORMAT_VERSION_ITEM_BLOCK = "1.16.1"
MIN_ENGINE_VERSION = [1, 19, 0]
GLOBAL_VERSION = [1, 0, 0]


class CreativeCategory(Enum):
    Commands = "commands"
    Construction = "construction"
    Equipment = "equipment"
    Items = "items"
    Nature = "nature"


class Item:
    id: str
    display_name: str
    category: CreativeCategory
    max_stack_size: int

    is_food: bool
    food_bars: int

    def __init__(self) -> None:
        self.id = "placeholder"
        self.display_name = "Placeholder"
        self.category = CreativeCategory.Construction
        self.max_stack_size = 64

        self.is_food = False
        self.food_bars = 0

    def set_id(self, id: str):
        self.id = id
        return self

    def set_display_name(self, display_name: str):
        self.display_name = display_name
        return self

    def set_category(self, category: CreativeCategory):
        self.category = category
        return self

    def set_max_stack_size(self, max_stack_size: int):
        self.max_stack_size = max_stack_size
        return self

    def set_food(self, bars: int):
        self.is_food = True
        self.food_bars = bars
        return self


class AddonManager:
    def __init__(self, name: str, description: str) -> None:
        self.main_directory = OUT_DIRECTORY
        self.clean()

        self.name = name
        self.description = description

        technical_name = "_".join(self.name.lower().split(" "))
        self.namespace = technical_name

        self.behaviour_path = self.__ensure_file_or_folder_exists(
            path=OUT_DIRECTORY.joinpath(f"{technical_name}_behaviour"), is_folder=True
        )
        self.resource_path = self.__ensure_file_or_folder_exists(
            path=OUT_DIRECTORY.joinpath(f"{technical_name}_resources"), is_folder=True
        )

    def __ensure_file_or_folder_exists(
        self, path: pathlib.Path, is_folder: bool = False
    ):
        if not path.exists():
            if is_folder:
                path.mkdir(parents=True)
            else:
                path.touch()
        return path

    def __setup_behaviour_manifest(self, resource_manifest) -> dict:
        print("Setting up behaviour manifest")

        manifest_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("manifest.json")
        )
        manifest = {
            "format_version": FORMAT_VERSION,
            "header": {
                "name": f"{self.name} Resources",
                "description": self.description,
                "uuid": str(uuid.uuid4()),
                "version": GLOBAL_VERSION,
                "min_engine_version": MIN_ENGINE_VERSION,
            },
            "modules": [
                {
                    "description": self.description,
                    "type": "data",
                    "uuid": str(uuid.uuid4()),
                    "version": GLOBAL_VERSION,
                }
            ],
            "dependencies": [
                {
                    "uuid": resource_manifest["header"]["uuid"],
                    "version": resource_manifest["header"]["version"],
                }
            ],
        }

        manifest_path.write_text(json.dumps(manifest, indent=4))
        return manifest

    def __setup_resources_manifest(self) -> dict:
        print("Setting up resources manifest")

        manifest_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("manifest.json")
        )
        manifest = {
            "format_version": FORMAT_VERSION,
            "header": {
                "name": f"{self.name} Behaviours",
                "description": self.description,
                "uuid": str(uuid.uuid4()),
                "version": GLOBAL_VERSION,
                "min_engine_version": MIN_ENGINE_VERSION,
            },
            "modules": [
                {
                    "description": self.description,
                    "type": "resources",
                    "uuid": str(uuid.uuid4()),
                    "version": GLOBAL_VERSION,
                }
            ],
        }

        manifest_path.write_text(json.dumps(manifest, indent=4))
        return manifest

    def __real_initalize(self):
        rp_manifest = self.__setup_resources_manifest()
        bhp_manifest = self.__setup_behaviour_manifest(rp_manifest)
        print("Finished initalizing\n")

    def clean(self):
        shutil.rmtree(self.main_directory)
        self.main_directory.mkdir()

    def write_to_lang(self, key: str, value: str):
        # TODO: other languages?
        default_lang = "en_US"
        print(f"Writing '{key}' to language {default_lang} with value '{value}'")
        lang_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("texts"), is_folder=True
        )
        lang_file_path = self.__ensure_file_or_folder_exists(
            path=lang_path.joinpath(f"{default_lang}.lang")
        )
        lang_text = lang_file_path.read_text().lstrip()
        lang_file_path.write_text(f"{lang_text}\n{key}={value}")

    def add_item(self, item: Item):
        print(f"Creating item with id '{item.id}'")

        item_behaviour_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("items"), is_folder=True
        )
        item_resources_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/items"), is_folder=True
        )

        self.write_to_lang(
            key=f"item.{self.namespace}:{item.id}.name", value=item.display_name
        )

        print(f"Make sure to provide the texture for item with id '{item.id}'\n")
        item_path = self.__ensure_file_or_folder_exists(
            path=item_behaviour_path.joinpath(f"{item.id}.json")
        )

        item_data = {
            "format_version": FORMAT_VERSION_ITEM_BLOCK,
            "minecraft:item": {
                "description": {
                    "identifier": f"{self.namespace}:{item.id}",
                    "category": item.category.value,
                },
                "components": {
                    "max_stack_size": item.max_stack_size,
                    "minecraft:icon": {"texture": item.id},
                },
            },
        }

        if item.is_food:
            item_data["minecraft:item"]["components"]["minecraft:use_duration"] = 32
            item_data["minecraft:item"]["components"]["minecraft:food"] = {
                "nutrition": item.food_bars
            }

        item_path.write_text(json.dumps(item_data, indent=4))
        return item_data

    def initalize(self):
        try:
            self.__real_initalize()
        except Exception as err:
            error(f"Failed to initalize AddonManager: {err}")
