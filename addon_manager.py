import pathlib, json, uuid, shutil, enum
from util import error, OUT_DIRECTORY

DEBUG = True
def debug(message: str):
    '''
        DEBUG
    '''
    if DEBUG:
        print(f"DEBUG: {message}")

# TODO: maybe make these editable?
FORMAT_VERSION = 2
FORMAT_VERSION_ITEM_BLOCK = "1.16.100"
MIN_ENGINE_VERSION = [1, 16, 0]
GLOBAL_VERSION = [1, 0, 0]

class CreativeCategory(enum.Enum):
    '''
        A enum consisting of the Bedrock Edition creative tabs
    '''
    CONSTRUCTION = "Construction"
    EQUIPMENT = "Equipment"
    ITEMS = "Items"
    NATURE = "Nature"

class Item:
    '''
        A minecraft bedrock item
    '''
    id: str
    display_name: str
    category: CreativeCategory
    max_stack_size: int

    is_food: bool
    food_bars: int

    def __init__(self) -> None:
        self.id = "placeholder"
        self.display_name = "Placeholder"
        self.category = CreativeCategory.CONSTRUCTION
        self.max_stack_size = 64

        self.is_food = False
        self.food_bars = 0

    def set_id(self, item_id: str):
        '''
            Sets the items id
        '''
        self.id = item_id
        return self

    def set_display_name(self, display_name: str):
        '''
            Sets the items display name
        '''
        self.display_name = display_name
        return self

    def set_category(self, category: CreativeCategory):
        '''
            Sets the items creative tab/category
        '''
        self.category = category
        return self

    def set_max_stack_size(self, max_stack_size: int):
        '''
            Set the max number the item can stack to
        '''
        self.max_stack_size = max_stack_size
        return self

    def set_food(self, bars: int):
        '''
            Sets is_food on the item and sets the value for the food consumption (food_bars)
        '''
        self.is_food = True
        self.food_bars = bars
        return self
    
    def construct(self, namespace: str) -> dict:
        '''
            Returns the item json used inside a behaviour pack
        '''
        data = {
            "format_version": FORMAT_VERSION_ITEM_BLOCK,
            "minecraft:item": {
                "description": {
                    "identifier": f"{namespace}:{self.id}",
                    "category": self.category.value,
                },
                "components": {
                    "minecraft:icon": {"texture": f"{namespace}:{self.id}"},
                    "minecraft:display_name": {"value": self.display_name},
                    "minecraft:max_stack_size": self.max_stack_size,
                },
            },
        }

        if self.is_food:
            data["minecraft:item"]["components"]["minecraft:use_duration"] = 32
            data["minecraft:item"]["components"]["minecraft:food"] = {
                "nutrition": self.food_bars
            }
            
        return data
    
class Block:
    '''
        A minecraft bedrock block
    '''
    id: str
    display_name: str
    category: CreativeCategory
    
    def __init__(self) -> None:
        self.id = "placeholder"
        self.display_name = "Placeholder"
        self.category = CreativeCategory.CONSTRUCTION
        
    def set_id(self, block_id: str):
        '''
            Sets the blocks id
        '''
        self.id = block_id
        return self

    def set_display_name(self, display_name: str):
        '''
            Sets the blocks display name
        '''
        self.display_name = display_name
        return self

    def set_category(self, category: CreativeCategory):
        '''
            Sets the blocks creative tab/category
        '''
        self.category = category
        return self
    
    def construct(self, namespace: str) -> dict:
        '''
            Returns the block json used inside a behaviour pack
        '''
        data = {
            "format_version": FORMAT_VERSION_ITEM_BLOCK,
            "minecraft:block": {
                "description": {
                    "identifier": f"{namespace}:{self.id}",
                    "category": self.category.value,
                },
                "components": {}
            }
        }
        
        return data

class Recipe:
    '''
        A minecraft bedrock recipe
    '''
    pass

class Entity:
    '''
        A minecraft bedrock entity
    '''
    pass

class AddonManager:
    '''
        Create Minecraft Bedrock Edition Addons using this class!
    '''
    def __init__(
        self, name: str, description: str, namespace: str | None = None
    ) -> None:
        self.main_directory = OUT_DIRECTORY
        self.clean()

        self.name = name
        self.description = description

        technical_name = "_".join(self.name.lower().split(" "))
        self.namespace = technical_name if namespace is None else namespace

        self.behaviour_path = self.__ensure_file_or_folder_exists(
            path=OUT_DIRECTORY.joinpath(f"{technical_name}_behaviour"), is_folder=True
        )
        self.resource_path = self.__ensure_file_or_folder_exists(
            path=OUT_DIRECTORY.joinpath(f"{technical_name}_resources"), is_folder=True
        )
        
        self.items_behaviour_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("items"), is_folder=True
        )
        self.items_resources_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/items"), is_folder=True
        )
        
        self.blocks_behaviour_path = self.__ensure_file_or_folder_exists(
            path=self.behaviour_path.joinpath("blocks"), is_folder=True
        )
        self.blocks_resources_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/blocks"), is_folder=True
        )
        
        self.items: list[Item] = []
        self.blocks: list[Block] = []
        self.recipes: list[Recipe] = []
        self.entities: list[Entity] = []
        
        self.initalize()

    def __ensure_file_or_folder_exists(
        self, path: pathlib.Path, is_folder: bool = False
    ):
        '''
            Checks if the path exists, if not it creates it and its parents
        '''
        if not path.exists():
            if is_folder:
                path.mkdir(parents=True)
            else:
                path.touch()
        return path

    def __setup_behaviour_manifest(self, resource_manifest) -> dict:
        '''
            Create and put the behaviour pack manifest into the addon
        '''
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
        '''
            Create and put the resource pack manifest into the addon
        '''
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
        '''
            reset/clear the contents in the out folder
        '''
        shutil.rmtree(self.main_directory)
        self.main_directory.mkdir()

    def __write_to_lang(self, key: str, value: str):
        '''
            Write the item (id) display name to texts/(language).json
        '''
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

    def __write_item_texture(self, item_id: str):
        '''
            Write the item (item_id) texture to textures/item_texture.json
        '''
        item_textures_json_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/item_texture.json"),
        )
        name = f"{self.namespace}:{item_id}"
        try:
            parsed = json.loads(item_textures_json_path.read_text())
            parsed["texture_data"][name] = {"textures": f"textures/items/{item_id}"}
            item_textures_json_path.write_text(json.dumps(parsed, indent=4))
        except:
            item_textures_json_path.write_text(
                json.dumps(
                    {
                        "texture_name": "atlas.items",
                        "texture_data": {name: {"textures": f"textures/items/{item_id}"}},
                    },
                    indent=4,
                )
            )
        debug(f"Make sure to provide the texture for item with id '{item_id}'")
    
    def __write_block_texture(self, block_id: str):
        '''
            Write the block (block_id) texture to textures/terrain_texture.json
        '''
        block_textures_json_path = self.__ensure_file_or_folder_exists(
            path=self.resource_path.joinpath("textures/terrain_texture.json"),
        )
        name = f"{self.namespace}:{block_id}"
        try:
            parsed = json.loads(block_textures_json_path.read_text())
            parsed["texture_data"][name] = {"textures": f"textures/blocks/{block_id}"}
            block_textures_json_path.write_text(json.dumps(parsed, indent=4))
        except:
            block_textures_json_path.write_text(
                json.dumps(
                    {
                        "texture_name": "atlas.terrain",
                        "padding": 8,
                        "num_mip_levels": 4,
                        "texture_data": {name: {"textures": f"textures/blocks/{block_id}"}},
                    },
                    indent=4,
                )
            )
        debug(f"Make sure to provide the texture for block with id '{block_id}'")

    def add_item(self, item: Item):
        '''
            Add a custom item to the addon using the Item class
        '''
        debug(f"Adding item with id '{item.id}'")
        index = len(self.items)
        self.items.append(item)
        return index
    
    def add_block(self, block: Block):
        '''
            Add a custom block to the addon using the Block class
        '''
        debug(f"Adding block with id '{block.id}'")
        index = len(self.blocks)
        self.blocks.append(block)
        return index

    def __real_initalize(self):
        rp_manifest = self.__setup_resources_manifest()
        self.__setup_behaviour_manifest(rp_manifest)
        debug("Finished initalizing\n")

    def initalize(self):
        '''
            Initalize Addon Manager
        '''
        try:
            self.__real_initalize()
        except Exception as err:
            error(f"Failed to initalize AddonManager: {err}")

    def __generate_items(self):
        for item in self.items:
            self.__write_to_lang(
                key=f"item.{self.namespace}:{item.id}.name", value=item.display_name
            )
            self.__write_item_texture(item_id=item.id)
            item_path = self.__ensure_file_or_folder_exists(
                path=self.items_behaviour_path.joinpath(f"{item.id}.json")
            )
            item_data = item.construct(namespace=self.namespace)
            item_path.write_text(json.dumps(item_data, indent=4))

    def __generate_blocks(self):
        for block in self.blocks:
            self.__write_to_lang(
                key=f"block.{self.namespace}:{block.id}.name", value=block.display_name
            )
            self.__write_block_texture(block_id=block.id)
            block_path = self.__ensure_file_or_folder_exists(
                path=self.blocks_behaviour_path.joinpath(f"{block.id}.json")
            )
            block_data = block.construct(namespace=self.namespace)
            block_path.write_text(json.dumps(block_data, indent=4))

    def generate(self):
        self.__generate_items()
        self.__generate_blocks()