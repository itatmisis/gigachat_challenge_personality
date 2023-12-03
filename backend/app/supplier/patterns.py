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
    Pattern(
        title="pencil",
        description="Наброски карандашом прямиком из тетради!",
        themes=["doodle sketch"],
        color_styles=["monochrome, black and white, paper texture"],
        draw_styles=["pencil sketch"],
    ),
    Pattern(
        title="fluffy",
        description="Пушистики!",
        themes=["fluffy animal"],
        moods=["Cute"],
        color_styles=[
            "Pastel",
            "Vibrant colours",
            "Flamboyant picturesque",
            "Vivid",
        ],
        draw_styles=["Chibi"],
    ),
    Pattern(
        title="snowwhite",
        description="Белоснежка и 7 гномов",
        themes=["Snow White girl", "hand mirror", "red apple", "evil queen"],
        moods=["Content", "Fairy", "Lovely", "Picturesque", "Mysterious"],
        color_styles=["Calm Colors", "Soft Colors", "Muted Color"],
        draw_styles=["mural art style", "book illustration", "Disney Pixar"],
    ),
    Pattern(
        title="owl",
        description="Люблю сов и всё что с ними связано",
        themes=["Owl"],
        moods=["Cute", "Funny", "Serious"],
        draw_styles=["realism", "disney pixar", "pokemon card"],
    ),
    Pattern(
        title="wizard",
        description="Ощути себя волшебником!",
        themes=["wizard", "spellcasting", "potion brewing", "whimsical entity"],
        moods=["Magical", "Heartwarming", "devious", "Mystical"],
    ),
    Pattern(
        title="anime",
        description="Анимешный подход!",
        themes=["anime", "anime girl", "kawai", "anime hero"],
        moods=[
            "Content",
            "Adorable",
            "Lovely",
            "Blissful",
            "Peaceful",
            "Undisturbed",
            "Cute",
            "Picturesque",
        ],
        color_styles=[
            "Soft Colors",
            "Sparkly Colors",
        ],
        draw_styles=[
            "Pixel Art",
            "Pokemon Card",
            "Anime Art",
            "Clip Studio Art",
            "Chibi",
        ],
    ),
    Pattern(title="random", description="Полностью случайный паттерн"),
]

name_to_pattern: dict[str, Pattern] = {pattern.title: pattern for pattern in _patterns}
