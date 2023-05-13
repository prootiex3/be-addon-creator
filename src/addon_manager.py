import pathlib
import json
import uuid
import shutil
# If you have a linter/pylint, it will show these as errors but it works and I don't know how to remove the error
from .util import error, debug, OUT_DIRECTORY 
from .constants import FORMAT_VERSION, FORMAT_VERSION_BLOCK_SOUND, MIN_ENGINE_VERSION, GLOBAL_VERSION 
from .item import Item
from .block import Block
from .entity import Entity
from .biome import Biome
from .recipe import CraftingRecipeShapeless, CraftingRecipeShaped

class AddonManager:
    """
    Create Minecraft Bedrock Edition Addons using this class!
    """

    def __init__(
        self, name: str, description: str, namespace: str | None = None
    ) -> None:
        self.main_directory = OUT_DIRECTORY
        self.clean()

        self.name = name
        self.namespace = (
            "_".join(self.name.lower().split(" ")) if namespace is None else namespace
        )
        self.description = description

        self.behaviour_path = self.__ensure_file_or_folder_exists(
            path=OUT_DIRECTORY.joinpath(f"{self.namespace}_behaviour"), is_folder=True
        )
        self.resource_path = self.__ensure_file_or_folder_exists(
            path=OUT_DIRECTORY.joinpath(f"{self.namespace}_resources"), is_folder=True
        )

        self.items_behaviour_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("items"), is_folder=True
        )
        self.items_textures_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/items"), is_folder=True
        )

        self.blocks_behaviour_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("blocks"), is_folder=True
        )

        self.blocks_textures_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/blocks"), is_folder=True
        )

        self.recipes_behaviour_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("recipes"), is_folder=True
        )

        self.entities_behaviour_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("entities"), is_folder=True
        )

        self.entities_resource_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("entity"), is_folder=True
        )

        self.items: list[Item] = []
        self.blocks: list[Block] = []
        self.recipes: list[CraftingRecipeShapeless | CraftingRecipeShaped] = []
        self.entities: list[Entity] = []
        self.biomes: list[Biome] = []

        self.initalize()

    def __ensure_file_or_folder_exists(
        self, path: pathlib.Path, is_folder: bool = False
    ):
        """
        Checks if the path exists, if not it creates it and its parents
        """
        if not path.exists():
            if is_folder:
                path.mkdir(parents=True)
            else:
                path.touch()
        return path

    def __setup_behaviour_manifest(self, resource_manifest) -> dict:
        """
        Create and put the behaviour pack manifest into the addon
        """
        debug("Setting up behaviour manifest")

        manifest_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("manifest.json")
        )
        manifest = {
            "format_version": FORMAT_VERSION,
            "header": {
                "name": f"{self.name} Behaviour",
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
        """
        Create and put the resource pack manifest into the addon
        """
        debug("Setting up resources manifest")

        manifest_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("manifest.json")
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
                    "type": "resources",
                    "uuid": str(uuid.uuid4()),
                    "version": GLOBAL_VERSION,
                }
            ],
        }

        manifest_path.write_text(json.dumps(manifest, indent=4))
        return manifest

    def clean(self):
        """
        reset/clear the contents in the out folder
        """
        shutil.rmtree(self.main_directory)
        self.main_directory.mkdir()

    def __write_to_lang(self, key: str, value: str):
        """
        Write the item (id) display name to texts/(language).json
        """
        # TODO: other languages?
        default_lang = "en_US"
        debug(f"Writing '{key}' to language {default_lang} with value '{value}'")
        lang_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("texts"), is_folder=True
        )
        lang_file_path = self.__ensure_file_or_folder_exists(
            path=lang_path.joinpath(f"{default_lang}.lang")
        )
        lang_text = lang_file_path.read_text().lstrip()
        lang_file_path.write_text(f"{lang_text}\n{key}={value}")

    def __write_item_texture(self, item: Item):
        """
        Write the item (item.id) texture to textures/item_texture.json
        """
        item_textures_json_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/item_texture.json")
        )
        name = f"{self.namespace}:{item.id}"
        try:
            parsed = json.loads(item_textures_json_path.read_text())
            parsed["texture_data"][name] = {
                "textures": f"textures/items/{item.id}"
                if item.texture_path is None
                else item.texture_path
            }
            item_textures_json_path.write_text(json.dumps(parsed, indent=4))
        except:
            item_textures_json_path.write_text(
                json.dumps(
                    {
                        "texture_name": "atlas.items",
                        "texture_data": {
                            name: {
                                "textures": f"textures/items/{item.id}"
                                if item.texture_path is None
                                else item.texture_path
                            }
                        },
                    },
                    indent=4,
                )
            )
        debug(f"Make sure to provide the texture for item with id '{item.id}'")

    def __write_block_sound(self, block: Block):
        blocks_resource_sounds_json_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("blocks.json")
        )
        name = f"{self.namespace}:{block.id}"
        try:
            parsed = json.loads(blocks_resource_sounds_json_path.read_text())
            parsed[name] = {"sound": block.sound.value, "textures": name}
            blocks_resource_sounds_json_path.write_text(json.dumps(parsed, indent=4))
        except:
            data = {
                "format_version": FORMAT_VERSION_BLOCK_SOUND,
                name: {"sound": block.sound.value, "textures": name},
            }
            blocks_resource_sounds_json_path.write_text(json.dumps(data, indent=4))

    def __write_block_texture(self, block: Block):
        """
        Write the block (block.id) texture to textures/terrain_texture.json
        """
        block_textures_json_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/terrain_texture.json")
        )
        name = f"{self.namespace}:{block.id}"
        try:
            parsed = json.loads(block_textures_json_path.read_text())
            parsed["texture_data"][name] = {
                "textures": f"textures/blocks/{block.id}"
                if block.texture_path is None
                else block.texture_path
            }
            block_textures_json_path.write_text(json.dumps(parsed, indent=4))
        except:
            block_textures_json_path.write_text(
                json.dumps(
                    {
                        "texture_name": "atlas.terrain",
                        "padding": 8,
                        "num_mip_levels": 4,
                        "texture_data": {
                            name: {
                                "textures": f"textures/blocks/{block.id}"
                                if block.texture_path is None
                                else block.texture_path
                            }
                        },
                    },
                    indent=4,
                )
            )
        debug(f"Make sure to provide the texture for block with id '{block.id}'")

    def add_item(self, item: Item):
        """
        Add a custom item to the addon using the Item class
        """
        debug(f"Adding item with id '{item.id}'")
        index = len(self.items)
        self.items.append(item)
        return index

    def add_items(self, items: list[Item]):
        """
        Add a list of custom items to the addon using an array of Item classes
        """
        for item in items:
            self.add_item(item)
        return len(self.items)

    def add_block(self, block: Block):
        """
        Add a custom block to the addon using the Block class
        """
        debug(f"Adding block with id '{block.id}'")
        index = len(self.blocks)
        self.blocks.append(block)
        return index

    def add_blocks(self, blocks: list[Block]):
        """
        Add a list of custom blocks to the addon using an array of Block classes
        """
        for block in blocks:
            self.add_block(block)
        return len(self.blocks)

    def add_recipe(self, recipe: CraftingRecipeShapeless | CraftingRecipeShaped):
        """
        Add a custom recipe to the addon using the Recipe class
        """
        debug(f"Adding recipe for item/block with id '{recipe.result_item_id}'")
        index = len(self.recipes)
        self.recipes.append(recipe)
        return index

    def add_entity(self, entity: Entity):
        """
        Add a custom entity to the addon using the Entity class
        """
        debug(f"Adding entity with id '{entity.id}'")
        index = len(self.entities)
        self.entities.append(entity)
        return index

    def __real_initalize(self):
        rp_manifest = self.__setup_resources_manifest()
        self.__setup_behaviour_manifest(rp_manifest)
        debug("Finished initalizing\n")

    def initalize(self):
        """
        Initalize Addon Manager
        """
        try:
            self.__real_initalize()
        except Exception as err:
            error(f"Failed to initalize AddonManager: {err}")

    def __generate_recipe(
        self, recipe: CraftingRecipeShaped | CraftingRecipeShapeless | None
    ):
        if recipe is None:
            return
        recipe_json_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath(f"recipes/{recipe.item_id}.json"),
        )
        recipe_json_path.write_text(
            json.dumps(recipe.construct(self.namespace), indent=4)
        )

    def __generate_items(self):
        for item in self.items:
            self.__write_to_lang(
                key=f"item.{self.namespace}:{item.id}.name", value=item.display_name
            )
            self.__write_item_texture(item)
            self.__generate_recipe(item.recipe)
            item_path = self.__ensure_file_or_folder_exists(
                path=self.items_behaviour_path.joinpath(f"{item.id}.json")
            )
            item_data = item.construct(self.namespace)
            item_path.write_text(json.dumps(item_data, indent=4))

    def __generate_blocks(self):
        for block in self.blocks:
            self.__write_to_lang(
                key=f"tile.{self.namespace}:{block.id}.name", value=block.display_name
            )
            self.__write_block_texture(block)
            self.__write_block_sound(block)
            self.__generate_recipe(block.recipe)
            block_path = self.__ensure_file_or_folder_exists(
                path=self.blocks_behaviour_path.joinpath(f"{block.id}.json")
            )
            block_data = block.construct(self.namespace)
            block_path.write_text(json.dumps(block_data, indent=4))

    def __generate_recipes(self):
        for recipe in self.recipes:
            self.__generate_recipe(recipe)

    def __generate_entities(self):
        for entity in self.entities:
            # For the resource pack
            entity_path_resource = self.__ensure_file_or_folder_exists(
                path=self.entities_resource_path.joinpath(f"{entity.id}.entity.json")
            )
            entity_data_resource = entity.construct_resource(self.namespace)
            entity_path_resource.write_text(json.dumps(entity_data_resource, indent=4))
            # For the behaviour pack
            entity_path_behaviour = self.__ensure_file_or_folder_exists(
                path=self.entities_behaviour_path.joinpath(f"{entity.id}.json")
            )
            entity_data_behaviour = entity.construct_behaviour(self.namespace)
            entity_path_behaviour.write_text(
                json.dumps(entity_data_behaviour, indent=4)
            )
            # Name the spawn egg
            self.__write_to_lang(
                key=f"item.spawn_egg.entity.{self.namespace}:{entity.id}.name",
                value=f"{entity.name} Spawn Egg",
            )

    def generate(self):
        """
        Generate the files for the addon like items, blocks, recipes, etc...
        """
        self.__generate_items()
        self.__generate_blocks()
        self.__generate_recipes()
        self.__generate_entities()
