import pathlib, json, uuid, shutil, enum
from util import error, OUT_DIRECTORY

DEBUG = True


def debug(message: str):
    """
    DEBUG
    """
    if DEBUG:
        print(f"DEBUG: {message}")


# TODO: maybe make these editable?
FORMAT_VERSION = 2
FORMAT_VERSION_ITEM = "1.16.100"
FORMAT_VERSION_BLOCK = "1.19.80"
FORMAT_VERSION_BLOCK_SOUND = [1, 1, 0]
FORMAT_VERSION_RECIPE = "1.17.41"
FORMAT_VERSION_ENTITY = "1.8.0"
FORMAT_VERSION_BIOME = "1.13.0"
MIN_ENGINE_VERSION = [1, 19, 0]
GLOBAL_VERSION = [1, 0, 0]


# https://wiki.bedrock.dev/blocks/block-sounds.html
# Last updated for 1.19.80
class BlockSounds(enum.Enum):
    '''
    Minecraft Bedrock Block Sounds
    '''
    AMETHYST_BLOCK = "amethyst_block"
    AMETHYST_CLUSTER = "amethyst_cluster"
    ANCIENT_DEBRIS = "ancient_debris"
    ANVIL = "anvil"
    AZALEA = "azalea"
    AZALEA_LEAVES = "azalea_leaves"
    BAMBOO = "bamboo"
    BAMBOO_SAPLING = "bamboo_sapling"
    BASALT = "basalt"
    BIG_DRIPLEAF = "big_dripleaf"
    BONE_BLOCK = "bone_block"
    CALCITE = "calcite"
    CANDLE = "candle"
    CAVE_VINES = "cave_vines"
    CHAIN = "chain"
    CLOTH = "cloth"
    COMPARATOR = "comparator"
    COPPER = "copper"
    CORAL = "coral"
    DEEPSLATE = "deepslate"
    DEEPSLATE_BRICKS = "deepslate_bricks"
    DIRT_WITH_ROOTS = "dirt_with_roots"
    DRIPSTONE_BLOCK = "dripstone_block"
    FROG_SPAWN = "frog_spawn"
    FROG_LIGHT = "froglight"
    FUNGUS = "fungus"
    GLASS = "glass"
    GRASS = "grass"
    GRAVEL = "gravel"
    HANGING_ROOTS = "hanging_roots"
    HONEY_BLOCK = "honey_block"
    ITEM_FRAME = "itemframe"
    LADDER = "ladder"
    LANTERN = "lantern"
    LARGE_AMETHYST_BUD = "large_amethyst_bud"
    SMALL_AMETHYST_BUD = "small_amethyst_bud"
    LEVER = "lever"
    LODESTONE = "lodestone"
    MANGROVE_ROOTS = "mangrove_roots"
    MUDDY_MANGROVE_ROOTS = "muddy_mangrove_roots"
    MEDIUM_AMETHYST_BUD = "medium_amethyst_bud"
    METAL = "metal"
    MOSS_BLOCK = "moss_block"
    MOSS_CARPET = "moss_carpet"
    MUD = "mud"
    MUD_BRICKS = "mud_bricks"
    NETHER_BRICK = "nether_brick"
    NETHER_GOLD_ORE = "nether_gold_ore"
    NETHER_SPROUTS = "nether_sprouts"
    NETHER_WART = "nether_wart"
    NETHER_WOOD = "nether_wood"
    NETHERITE = "netherite"
    NETHERRACK = "netherrack"
    NYLIUM = "nylium"
    PACKED_MUD = "packed_mud"
    POINTED_DRIPSTONE = "pointed_dripstone"
    POWDER_SNOW = "powder_snow"
    ROOTS = "roots"
    SAND = "sand"
    SCAFFOLDING = "scaffolding"
    SCULK = "sculk"
    SCULK_CATALYST = "sculk_catalyst"
    SCULK_SENSOR = "sculk_sensor"
    SCULK_SHRIEKER = "sculk_shrieker"
    SCULK_VEIN = "sculk_vein"
    SHROOM_LIGHT = "shroomlight"
    SLIME = "slime"
    SNOW = "snow"
    SOUL_SAND = "soul_sand"
    SOUL_SOIL = "soul_soil"
    SPORE_BLOSSOM = "spore_blossom"
    STEM = "stem"
    STONE = "stone"
    SWEET_BERRY_BUSH = "sweet_berry_bush"
    TUFF = "tuff"
    VINES = "vines"
    WOOD = "wood"

# https://wiki.bedrock.dev/items/items-16.html#enchantable-slots
class EnchantableSlot(enum.Enum):
    '''
    _
    '''
    ARMOR_FEET = "armor_feet"
    ARMOR_TORSO = "armor_torso"
    ARMOR_HEAD = "armor_head"
    ARMOR_LEGS = "armor_legs"
    AXE = "axe"
    BOW = "bow"
    COSMETIC_HEAD = "cosmetic_head"
    CROSSBOW = "crossbow"
    ELYTRA = "elytra"
    FISHING_ROD = "fishing_rod"
    FLINT_AND_STEEL = "flintsteel"
    HOE = "hoe"
    PICKAXE = "pickaxe"
    SHEARS = "shears"
    SHIELD = "shield"
    SHOVEL = "shovel"
    SWORD = "sword"

# https://wiki.bedrock.dev/items/enchantments.html
class Enchantments(enum.Enum):
    '''
    Minecraft Bedrock Enchantments
    '''
    SILK_TOUCH = "silk_touch"
    FORTUNE = "fortune"
    EFFICIENCY = "efficiency"
    LUCK_OF_THE_SEA = "luck_of_the_sea"
    LURE = "lure"
    SHARPNESS = "sharpness"
    SMITE	= "smite"
    BANE_OF_ARTHROPODS = "bane_of_arthropods"
    FIRE_ASPECT = "fire_aspect"
    KNOCKBACK = "knockback"
    LOOTING = "looting"
    POWER = "power"
    FLAME = "flame"
    PUNCH = "punch"
    INFINITY = "infinity"
    MULTI_SHOT = "multishot"
    PIERCING = "piercing"
    QUICK_CHARGE = "quick_charge"
    IMPALING = "impaling"
    RIPTIDE = "riptide"
    LOYALTY = "loyalty"
    CHANNELING = "channeling"
    PROTECTION = "protection"
    PROJECTILE_PROTECTION =	"projectile_protection"
    FIRE_PROTECTION = "fire_protection"
    BLASH_PROTECTION = "blast_protection"
    FEATHER_FALLING = "feather_falling"
    THORNS = "thorns"
    FROST_WALKER = "frost_walker"
    RESPIRATION = "respiration"
    AQUA_AFFINITY = "aqua_affinity"
    CURSE_OF_BINDING = "curse_of_binding"
    DEPTH_STRIDER = "depth_strider"
    SOUL_SPEED = "soul_speed"
    UNBREAKING = "unbreaking"
    MENDING = "mending"
    CURSE_OF_VANISHING = "curse_of_vanishing"

# https://wiki.bedrock.dev/documentation/creative-categories.html
class CreativeCategory(enum.Enum):
    """
    A enum consisting of the Bedrock Edition creative tabs
    """

    CONSTRUCTION = "Construction"
    EQUIPMENT = "Equipment"
    ITEMS = "Items"
    NATURE = "Nature"


# https://wiki.bedrock.dev/commands/damage.html#damage-cause-list
class DamageSources(enum.Enum):
    ANVIL = "anvil"
    ATTACK = "attack"
    BLOCK_EXPLOSION = "block_explosion"
    CHARGING = "charging"
    CONTACT = "contact"
    DROWNING = "drowning"
    ENTITY_ATTACK = "entity_attack"
    ENTITY_EXPLOSION = "entity_explosion"
    FALL = "fall"
    FALLING_BLOCK = "falling_block"
    FATAL = "fatal"
    FIRE = "fire"
    FIRE_TICK = "fire_tick"
    FIREWORKS = "fireworks"
    FLY_INTO_WALL = "fly_into_wall"
    FREEZING = "freezing"
    LAVA = "lava"
    LIGHTING = "lightning"
    MAGIC = "magic"
    MAGMA = "magma"
    NONE = "none"
    OVERRIDE = "override"
    PISTON = "piston"
    PROJECTILE = "projectile"
    SONIC_BOOM = "sonic_boom"
    STALACITE = "stalactite"
    STALAGMITE = "stalagmite"
    STARVE = "starve"
    SUFFOCATION = "suffocation"
    SUICIDE = "suicide"
    TEMPATURE = "temperature"
    THORNS = "thorns"
    VOID = "void"
    WITHER = "wither"

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
        '''
        Set the item the recipe is being used for
        '''
        self.item_id = item_id
        return self

    def set_pattern(self, pattern: list[str]):
        '''
        Set the shape of the recipe
        '''
        self.pattern = pattern
        return self

    def set_result_item_id(self, result_item_id: str):
        '''
        Set the result item of the recipe
        '''
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

    def __init__(self, item_id: str, count: int) -> None:
        self.item_id = item_id
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

    is_food: bool
    food_bars: int
    
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
        self.is_food = False
        self.food_bars = 0
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

    def set_food(self, bars: int):
        """
        Sets is_food on the item and sets the value for the food consumption (food_bars)
        """
        self.is_food = True
        self.food_bars = bars
        return self
    
    def set_enchanted(self):
        '''
        Makes the item look enchanted
        '''
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
                    "minecraft:hand_equipped": True
                },
            },
        }

        if self.is_food:
            data["minecraft:item"]["components"]["minecraft:use_duration"] = 32
            data["minecraft:item"]["components"]["minecraft:food"] = {
                "nutrition": self.food_bars
            }
            # TODO: allow using animation: drink 
            data["minecraft:item"]["components"]["minecraft:use_animation"] = "eat"

        return data

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
        data = {
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

        return data

# https://bedrock.dev/docs/stable/Entities#Biome%20Tags
class BiomeTags(enum.Enum):
    ANIMAL = "animal"
    BEACH = "beach"
    BIRCH = "birch"
    COLD = "cold"
    DARK_OAK = "dark_oak"
    DEEP = "deep"
    DESERT = "desert"
    EGE = "edge"
    EXTREME_HILLS = "extreme_hills"
    FLOWER_FOREST = "flower_forest"
    FOREST = "forest"
    FROZEN = "frozen"
    HILLS = "hills"
    ICE = "ice"
    ICE_PLAINS = "ice_plains"
    JUNGLE = "jungle"
    LAKES = "lakes"
    LUKEWARN = "lukewarm"
    MEGA = "mega"
    MESA = "mesa"
    MONSTER = "monster"
    MOOSHROOM_ISLAND = "mooshroom_island"
    MOUNTAIN = "mountain"
    MUTATED = "mutated"
    NETHER = "nether"
    OCEAN = "ocean"
    PLAINS = "plains"
    PLATEAU = "plateau"
    RIVER = "river"
    ROOFED = "roofed"
    SAVANNA = "savanna"
    SHORE = "shore"
    STONE = "stone"
    SWAMP = "swamp"
    TAIGA = "taiga"
    THE_END = "the_end"
    WARM = "warm"

# https://bedrock.dev/docs/stable/Entities
class Entity:
    """
    A minecraft bedrock entity
    """
    
    id: str
    
    egg_should_use_texture: bool
    egg_texture_path: str | None
    egg_base_color: str
    egg_overlay_color: str
    
    can_wear_armor: bool

    def __init__(self) -> None:
        self.id = ""
        self.egg_should_use_texture = False
        self.egg_texture_path = None
        self.egg_base_color = "#"
        self.egg_overlay_color = "#"
        self.can_wear_armor = True
        
    def set_id(self, entity_id: str):
        """
        Sets the entity's id
        """
        self.id = entity_id
        return self
    
    def set_egg_use_texture(self, texture_path: str):
        self.egg_should_use_texture = True
        self.egg_texture_path = texture_path
        return self
    
    def set_egg_base_color(self, hex_color: str):
        self.egg_base_color = hex_color
        return self
    
    def set_egg_overlay_color(self, hex_color: str):
        self.egg_overlay_color = hex_color
        return self
    
    def set_can_wear_armor(self, value: bool):
        self.can_wear_armor = value
        return self

    def construct(self, namespace: str) -> dict[str, str]:
        """
        Returns the entity json used inside a behaviour pack
        """
        data = {
            "format_version": FORMAT_VERSION_ENTITY,
            "minecraft:client_entity": {
                "description": {
                    "identifier": f"{namespace}:{self.id}",
                    "min_engine_version": '.'.join(MIN_ENGINE_VERSION),
                },
                "components": {
                    "enable_attachables": self.can_wear_armor,
                    "spawn_egg": {
                        "texture": "spawn_egg",
                        "texture_index": 0
                    } if self.egg_should_use_texture else {
                        "base_color": self.egg_base_color,
                        "overlay_color": self.egg_overlay_color
                    } 
                }
            }
        }
        return data

# https://wiki.bedrock.dev/world-generation/biomes.html#climates
class BiomeClimate(enum.Enum):
    '''
    Allowed Minecraft Bedrock Climates used in the Biome class
    '''
    FROZEN = "frozen"
    COLD = "cold"
    MEDIUM = "medium"
    LUKEWARM = "lukewarm"
    WARM = "warm"

# https://wiki.bedrock.dev/world-generation/biomes.html
# According to ^, "As of 1.18, Custom Biomes are broken for Minecraft Bedrock"
class Biome:
    '''
    A minecraft bedrock biome
    '''
    
    id: str
    
    def __init__(self) -> None:
        self.id = ""
        
    def set_id(self, biome_id: str):
        """
        Sets the biomes id
        """
        self.id = biome_id
        return self
    
    def construct(self, namespace: str) -> dict:
        """
        Returns the biomes json used inside a behaviour pack
        """
        return {
            "format_version": FORMAT_VERSION_BIOME,
            "minecraft:biome": {
                "description": {
                    "identifier": f"{namespace}_{self.id}"
                },
                "components": {}
            }
        }

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

        self.items: list[Item] = []
        self.blocks: list[Block] = []
        self.recipes: list[CraftingRecipeShapeless | CraftingRecipeShaped] = []
        self.entities: list[Entity] = []

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
            parsed[name] = {"sound": block.sound.value, "textures": block.texture_path}
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

    def add_block(self, block: Block):
        """
        Add a custom block to the addon using the Block class
        """
        debug(f"Adding block with id '{block.id}'")
        index = len(self.blocks)
        self.blocks.append(block)
        return index

    def add_recipe(self, recipe: CraftingRecipeShapeless | CraftingRecipeShaped):
        """
        Add a custom block to the addon using the Block class
        """
        debug(f"Adding recipe for item/block with id '{recipe.result_item_id}'")
        index = len(self.recipes)
        self.recipes.append(recipe)
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

    def generate(self):
        """
        Generate the files for the addon like items, blocks, recipes, etc...
        """
        self.__generate_items()
        self.__generate_blocks()        
        self.__generate_recipes()
