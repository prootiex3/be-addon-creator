import enum

# https://wiki.bedrock.dev/documentation/creative-categories.html
class CreativeCategory(enum.Enum):
    """
    A enum consisting of the Bedrock Edition creative tabs
    """

    CONSTRUCTION = "Construction"
    EQUIPMENT = "Equipment"
    ITEMS = "Items"
    NATURE = "Nature"