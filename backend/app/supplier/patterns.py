from dataclasses import dataclass


@dataclass
class Pattern:
    title: str

    themes: list[str] | None = None
    moods: list[str] | None = None
    styles: list[str] | None = None
    color_styles: list[str] | None = None
    draw_styles: list[str] | None = None


_patterns = [
    Pattern(
        title="pink",
        styles=["Adorable", "Excited", "Lovely", "Cute", "Happy"],
        color_styles=[
            "Bright Pink Colors",
            "Colorful Pink Colors",
            "Flashy Pink Colors",
        ],
    ),
    Pattern(title="empty"),
    Pattern(
        title="toy",
        themes=["toy", "lego body", "toy car"],
        moods=["Ecstatic", "Joyful", "Energetic", "Content"],
        color_styles=[],
        draw_styles=["art toy style", "lego", "minecraft", "roblox", "pixel art"],
    ),
]

name_to_pattern: dict[str, Pattern] = {pattern.title: pattern for pattern in _patterns}
