# If you have a linter/pylint, it will show these as errors but it works and I don't know how to remove the error
from .constants import FORMAT_VERSION_ENTITY_CLIENT, FORMAT_VERSION_ENTITY, MIN_ENGINE_VERSION

# https://bedrock.dev/docs/stable/Entities
class Entity:
    """
    A minecraft bedrock entity
    """

    id: str
    name: str
    textures: dict[str, str]

    egg_should_use_texture: bool
    egg_texture_path: str | None
    egg_base_color: str
    egg_overlay_color: str

    can_wear_armor: bool

    def __init__(self) -> None:
        self.id = ""
        self.name = ""
        self.textures = {"default": "textures/entity/steve"}

        self.egg_should_use_texture = False
        self.egg_texture_path = None
        self.egg_base_color = "#000000"
        self.egg_overlay_color = "#ffff00"

        self.can_wear_armor = True

    def set_id(self, entity_id: str):
        """
        Sets the entity's id
        """
        self.id = entity_id
        return self

    def set_name(self, name: str):
        """
        Sets the entity's name
        """
        self.name = name
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

    def set_can_wear_armor(self, value: bool = True):
        self.can_wear_armor = value
        return self

    # Entity
    def construct_behaviour(self, namespace: str) -> dict:
        return {
            "format_version": FORMAT_VERSION_ENTITY,
            "minecraft:entity": {
                "description": {
                    "identifier": f"{namespace}:{self.id}",
                    "is_spawnable": True,
                    "is_summonable": True,
                },
                "components": {
                    "minecraft:type_family": {"family": ["player"]},
                    "minecraft:collision_box": {"width": 0.6, "height": 1.8},
                },
            },
        }

    # Client Entity
    def construct_resource(self, namespace: str) -> dict[str, str]:
        """
        Returns the entity json used inside a behaviour pack
        """
        return {
            "format_version": FORMAT_VERSION_ENTITY_CLIENT,
            "minecraft:client_entity": {
                "description": {
                    "identifier": f"{namespace}:{self.id}",
                    "min_engine_version": ".".join([f"{i}" for i in MIN_ENGINE_VERSION]),  # type: ignore
                    "materials": {"default": "player"},
                    # entity_alphatest = player
                    "textures": self.textures,
                    "enable_attachables": self.can_wear_armor,
                    "geometry": {"default": "geometry.pig.v1.8"},
                    "animations": {
                        "walk": "animation.quadruped.walk",
                        "look_at_target": "animation.common.look_at_target",
                    },
                    "animation_controllers": [
                        {"setup": "controller.animation.pig.setup"},
                        {"move": "controller.animation.pig.move"},
                        {"baby": "controller.animation.pig.baby"},
                    ],
                    "render_controllers": ["controller.render.default"],
                    "spawn_egg": {"texture": "spawn_egg", "texture_index": 0}
                    if self.egg_should_use_texture
                    else {
                        "base_color": self.egg_base_color,
                        "overlay_color": self.egg_overlay_color,
                    },
                }
            },
        }