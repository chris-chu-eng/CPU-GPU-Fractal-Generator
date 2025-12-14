import pygame


def draw_text_wrapped(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    max_width: int,
    start_pos: tuple[int, int],
) -> None:
    """Draws text that automatically wraps to the next line.

    Args:
        surface (pygame.Surface): The surface to draw text onto.
        text (str): The text string to render.
        font (pygame.font.Font): The font to use for rendering.
        color (tuple[int, int, int]): RGB color tuple for the text.
        max_width (int): Maximum width before wrapping to next line.
        start_pos (tuple[int, int]): Starting (x, y) position for text.
    """
    words = text.split(" ")
    space_width, _ = font.size(" ")
    x, y = start_pos

    current_line = []
    current_width = 0

    for word in words:
        word_surface = font.render(word, True, color)
        word_width = word_surface.get_width()
        word_height = word_surface.get_height()

        if current_width + word_width >= max_width:
            surface.blit(font.render(" ".join(current_line), True, color), (x, y))
            current_line = [word]
            current_width = word_width
            y += word_height
        else:
            current_line.append(word)
            current_width += word_width + space_width

    if current_line:
        surface.blit(font.render(" ".join(current_line), True, color), (x, y))
