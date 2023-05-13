import enum
# If you have a linter/pylint, it will show these as errors but it works and I don't know how to remove the error
from .constants import FORMAT_VERSION_BIOME

# https://wiki.bedrock.dev/world-generation/biomes.html#climates
class BiomeClimate(enum.Enum):
    """
    Allowed Minecraft Bedrock Climates used in the Biome class
    """

    FROZEN = "frozen"
    COLD = "cold"
    MEDIUM = "medium"
    LUKEWARM = "lukewarm"
    WARM = "warm"


# https://wiki.bedrock.dev/world-generation/biomes.html
# According to ^, "As of 1.18, Custom Biomes are broken for Minecraft Bedrock"
class Biome:
    """
    A minecraft bedrock biome
    """

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
                "description": {"identifier": f"{namespace}_{self.id}"},
                "components": {},
            },
        }