import os
import constants as ct
import pathlib
from PIL import ImageTk, Image


class SpriteManager(object):
    """
    The SpriteManager manages game sprites.
    """

    # Initialize empty sprite container to hold our sprites
    # as to prevent tkinter from garbage collecting them
    __sprites = {}

    # Determine root path (the parent folder of this class)
    __root_path = pathlib.Path(os.path.abspath(os.getcwd())).parent

    @staticmethod
    def load_sprites() -> None:
        """
        Loads sprites from sprites folder.
        :return: None
        """
        # Reset sprites
        SpriteManager.__sprites = {}

        for file_name in os.listdir(SpriteManager.__root_path.joinpath(ct.SPRITE_PATH)):
            # Break up file name & extension (if it exists)
            file_name_tokens = os.path.splitext(file_name)

            # Validate file type if there is one
            if file_name_tokens[1] != f'.{ct.SPRITE_FORMAT}':
                continue

            # Add to sprite collection
            SpriteManager.__add_sprite(file_name_tokens[0])

    @staticmethod
    def __add_sprite(sprite_name: str) -> None:
        """
        Adds the PhotoImage object of the given sprite to the
        sprites collection.
        :param sprite_name: sprite to add
        :return: None
        """
        image = ImageTk.PhotoImage(Image.open(SpriteManager.__root_path.joinpath(
            f'{ct.SPRITE_PATH}/{sprite_name}.{ct.SPRITE_FORMAT}')))

        SpriteManager.__sprites.update({sprite_name: image})

    @staticmethod
    def get_sprite(sprite_name: str) -> ImageTk.PhotoImage:
        """
        Retrieves the PhotoImage object of the given sprite.
        :param sprite_name: sprite to retrieve
        :return: resulting PhotoImage object
        """
        return SpriteManager.__sprites.get(sprite_name)
