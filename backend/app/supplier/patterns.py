from dataclasses import dataclass


@dataclass
class Pattern:
    title: str
    description: str | None = None

    themes: list[str] | None = None
    moods: list[str] | None = None
    styles: list[str] | None = None
    color_styles: list[str] | None = None
    draw_styles: list[str] | None = None


RANDOM = "random"
_patterns = [
    Pattern(
        title="xmas",
        description="Бубенцы, бубенцы - радостно галдят",
        themes=[
            "christmas tree",
            "Santa Claus",
            "snow",
            "Christmas decorations",
            "winter",
        ],
        moods=["Excited", "Hopefull", "Blissful", "Enthusiastic"],
    ),
    Pattern(
        title="skihorise",
        description="Новый вид КОНЬкобежного спорта!",
        themes=["horse skating on ice"],
        moods=["Funny", "Whimsical", "Cute"],
        draw_styles=["Photorealism"],
    ),
    Pattern(
        title="crippy",
        description="Новое измерение в формате стикера!",
        themes=[
            "galactic voyage",
            "interdimensional travel",
            "hyperdimensional entity",
            "hippy in space",
        ],
        moods=[],
        color_styles=[
            "Acid",
            "Trippy",
            "Bright colours",
            "Flashing lights",
            "Vivid",
            "Rich-coloured",
            "Flamboyant",
        ],
        draw_styles=["Fractal", "Tattoo"],
    ),
    Pattern(
        title="pink",
        description="Цвет настроения - розовый!",
        styles=["Adorable", "Excited", "Lovely", "Cute", "Happy"],
        color_styles=[
            "Bright Pink Colors",
            "Colorful Pink Colors",
            "Flashy Pink Colors",
        ],
    ),
    Pattern(
        title="toy",
        description="Самое время вернуться в детство!",
        themes=["toy", "lego body", "toy car"],
        moods=["Ecstatic", "Joyful", "Energetic", "Content"],
        color_styles=[],
        draw_styles=["art toy style", "lego", "minecraft", "roblox", "pixel art"],
    ),
    Pattern(
        title="skelleton",
        description="Этот паттерн как кость в горле",
        themes=["skull in spacesuit", "skull", "skeleton"],
        moods=["Creepy", "Angry", "Rude", "Agressive"],
    ),
    Pattern(
        title="frogs",
        description="Лягушачье запрудье",
        themes=["water lily", "frog", "pond", "forest", "reed"],
        moods=[
            "Content",
            "Adorable",
            "Lovely",
            "Blissful",
            "Peaceful",
            "Undisturbed",
            "Picturesque",
        ],
        color_styles=["Calm Green Colors", "Soft Colors", "Muted Color"],
        draw_styles=["mural art style", "outsider art style", "Digital Art"],
    ),
    Pattern(title="random", description="Полностью случайный паттерн"),
]

name_to_pattern: dict[str, Pattern] = {pattern.title: pattern for pattern in _patterns}
