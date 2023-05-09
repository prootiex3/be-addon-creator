import pathlib, json, uuid, shutil
from util import error, OUT_DIRECTORY
from enum import Enum

FORMAT_VERSION = 2
FORMAT_VERSION_ITEM_BLOCK = "1.16.1"
MIN_ENGINE_VERSION = [1, 19, 0]


class CreativeCategory(Enum):
    Commands = "commands"
    Construction = "construction"
    Equipment = "equipment"
    Items = "items"
    Nature = "nature"


class Item:
    pass


class ItemBuilder:
    def __init__(self) -> None:
        pass

    def build(self):
        return Item()


class AddonManager:
    def __init__(self, name: str, description: str) -> None:
        self.main_directory = OUT_DIRECTORY
        self.clean()
        technical_name = "_".join(name.lower().split(" "))
        self.namespace = technical_name
        self.behaviour_path = OUT_DIRECTORY.joinpath(f"{technical_name}_behaviour")
        self.resource_path = OUT_DIRECTORY.joinpath(f"{technical_name}_resources")
        if not self.behaviour_path.exists():
            self.behaviour_path.mkdir()
        if not self.resource_path.exists():
            self.resource_path.mkdir()
        self.name = name
        self.description = description

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
        version = [0, 0, 1]

        manifest_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("manifest.json")
        )
        manifest = {
            "format_version": FORMAT_VERSION,
            "header": {
                "name": f"{self.name} Resources",
                "description": self.description,
                "uuid": str(uuid.uuid4()),
                "version": version,
                "min_engine_version": MIN_ENGINE_VERSION,
            },
            "modules": [
                {
                    "description": self.description,
                    "type": "data",
                    "uuid": str(uuid.uuid4()),
                    "version": version,
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
        version = [0, 0, 1]

        manifest_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("manifest.json")
        )
        manifest = {
            "format_version": FORMAT_VERSION,
            "header": {
                "name": f"{self.name} Behaviours",
                "description": self.description,
                "uuid": str(uuid.uuid4()),
                "version": version,
                "min_engine_version": MIN_ENGINE_VERSION,
            },
            "modules": [
                {
                    "description": self.description,
                    "type": "resources",
                    "uuid": str(uuid.uuid4()),
                    "version": version,
                }
            ],
        }

        manifest_path.write_text(json.dumps(manifest, indent=4))
        return manifest

    def __real_initalize(self):
        rp_manifest = self.__setup_resources_manifest()
        bhp_manifest = self.__setup_behaviour_manifest(rp_manifest)
        print("Finished initalizing")

    def clean(self):
        shutil.rmtree(self.main_directory)
        self.main_directory.mkdir()

    def write_to_lang(self, key: str, value: str):
        lang_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("texts"), is_folder=True
        )
        english_lang_path = self.__ensure_file_or_folder_exists(
            path=lang_path.joinpath("en_US.lang")
        )
        english_lang_path.write_text(f"\n{key}={value}")

    def add_item(
        self,
        id: str,
        display_name: str,
        category: CreativeCategory = CreativeCategory.Construction,
        stack_size: int = 64,
    ):
        print(f"Creating item with id '{id}'")

        item_behaviour_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("items"), is_folder=True
        )
        item_resources_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/items"), is_folder=True
        )

        self.write_to_lang(key=f"\nitem.{self.namespace}:{id}.name", value=display_name)

        texture_path = item_resources_path.joinpath(f"{id}.png")
        if not texture_path.exists():
            print(f"Make sure to provide the texture for item with id '{id}'")

        item_path = self.__ensure_file_or_folder_exists(
            path=item_behaviour_path.joinpath(f"{id}.json")
        )
        item = {
            "format_version": FORMAT_VERSION_ITEM_BLOCK,
            "minecraft:item": {
                "description": {
                    "identifier": f"{self.namespace}:{id}",
                    "category": category.value,
                },
                "components": {
                    "max_stack_size": stack_size,
                    "minecraft:icon": {"value": id},
                },
            },
        }

        #         "components": {
        #         "minecraft:use_duration": 32,
        #         "minecraft:food": {
        #             "nutrition": 4,
        #             "saturation_modifier": "low"
        #         }
        #         }

        item_path.write_text(json.dumps(item, indent=4))
        return item

    def initalize(self):
        try:
            self.__real_initalize()
        except Exception as err:
            error(f"Failed to initalize AddonManager: {err}")
