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


# pink_pattern = Pattern(description='Цвет настроения - розовый!',
#                        theme_list=[],
#                        mood_list=['Adorable','Excited','Lovely','Cute','Happy'],
#                        color_style_list=['Bright Pink Colors', 'Colorful Pink Colors', 'Flashy Pink Colors'],
#                        draw_style_list='')

# random_pattern = Pattern(description='Полностью случайный паттерн.',
#                        theme_list=[],
#                        mood_list=[],
#                        color_style_list=[],
#                        draw_style_list=[])

# toys_pattern = Pattern(description='Самое время вернуться в детство!',
#                        theme_list=['toy', 'lego body', 'toy car'],
#                        mood_list=['Ecstatic', 'Joyful', 'Energetic', 'Content'],
#                        color_style_list=[],
#                        draw_style_list=['art toy style', 'lego', 'minecraft', 'roblox', 'pixel art'])

# dota_pattern = Pattern(description='Этот паттерн как кость в горле',
#                        theme_list=['skull in spacesuit', 'skull', 'skeleton'],
#                        mood_list=['Creepy', 'Angry', 'Rude', 'Agressive'],
#                        color_style_list=[],
#                        draw_style_list=[])

# christmas_pattern = Pattern(description='Бубенцы, бубенцы - радостно галдят',
#                        theme_list=['christmas tree', 'Santa Claus', 'snow', 'Christmas decorations', 'winter'],
#                        mood_list=['Excited', 'Hopefull', 'Blissful', 'Enthusiastic'],
#                        color_style_list=[],
#                        draw_style_list=[])
_patterns = [
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
    Pattern(title="empty", description="Полностью случайный паттерн"),
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
]

name_to_pattern: dict[str, Pattern] = {pattern.title: pattern for pattern in _patterns}
