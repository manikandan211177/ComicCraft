from .models import ComicPanel


def build_comic_layout(
    outline,
    stories,
    image_urls,
) -> list[ComicPanel]:
    """
    Combines:

        Gemini outline
        +
        Gemini story
        +
        generated images

    into the final comic-panel structure.
    """

    if len(outline) != 5:

        raise ValueError(
            "Comic outline must contain "
            "exactly 5 panels."
        )

    if len(stories) != 5:

        raise ValueError(
            "Comic story must contain "
            "exactly 5 panels."
        )

    if len(image_urls) != 5:

        raise ValueError(
            "Comic image list must contain "
            "exactly 5 images."
        )

    # -----------------------------------------------------
    # Create story lookup
    # -----------------------------------------------------

    story_by_panel = {
        story.panel: story
        for story in stories
    }

    result = []

    # -----------------------------------------------------
    # Combine all data
    # -----------------------------------------------------

    for index, outline_panel in enumerate(
        outline
    ):

        story_panel = story_by_panel.get(
            outline_panel.panel
        )

        if story_panel is None:

            raise ValueError(
                "Story missing for panel "
                f"{outline_panel.panel}"
            )

        result.append(
            ComicPanel(
                panel=outline_panel.panel,

                title=outline_panel.title,

                image_url=image_urls[index],

                image_prompt=(
                    outline_panel.image_prompt
                ),

                scene_description=(
                    outline_panel.scene_description
                ),

                caption=story_panel.caption,

                narration=story_panel.narration,

                dialogue=story_panel.dialogue,
            )
        )

    return result