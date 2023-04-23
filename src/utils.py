# pylint: disable=missing-module-docstring
import os
import abc
from rembg import remove

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(ROOT_DIR, 'assets')
RESOURCE_CARDS_DIR = os.path.join(ASSET_DIR, 'resource')
DEVELOPMENT_CARDS_DIR = os.path.join(ASSET_DIR, 'development')
TILE_CARDS_DIR = os.path.join(ASSET_DIR, 'tiles')
BUILDINGS_DIR = os.path.join(ASSET_DIR, 'buildings')
FILE_EXTENSIONS = [".jpg", ".png", ".gif", ".jpeg"]


def prepare_assets(directory):
    """
    Prepare all asset files in the given directory.

    :param directory: A string representing the directory where assets can be found.
    :type directory: str
    :raises: ValueError if the directory does not exist.

    This method prepares all asset files in the given directory by applying the `remove` function
    to their contents and writing the results to new 
    files with the prefix "new_". The original files
    are deleted, and the new files are renamed to match the names of the original files.
    """
    files = os.listdir(directory)
    print()

    for file in files:
        if any(file.endswith(extension) for extension in FILE_EXTENSIONS):
            input_path = os.path.join(directory, file)

            print(input_path)

            output_path = os.path.join(directory, f'new_{file}')

            with open(input_path, 'rb') as input_file:
                with open(output_path, 'wb') as output_file:
                    fileinput = input_file.read()
                    output = remove(fileinput)
                    output_file.write(output)

            os.remove(input_path)
            os.rename(output_path, input_path)

        else:
            print(f"Error: {file} has an unsupported file extension")
            continue


class Abstract(abc.ABC):  # pylint: disable=too-few-public-methods
    """
    A base class for implementing abstract methods and retrieving assets.

    :param directory: A string representing the directory where assets can be found.
    :type directory: str

    This class provides a base for implementing abstract methods and retrieving assets.
    The `get_asset` method searches the given directory for asset files that match the name
    of the current class. If a match is found, the full path to the asset file is returned.
    If no matches are found, a NotImplementedError is raised.
    """
    def get_asset(self, directory):
        """
        Retrieve the asset file for the current class.

        :param directory: A string representing the directory where assets can be found.
        :type directory: str
        :return: The full path to the asset file for the current class.
        :rtype: str
        :raises: NotImplementedError if no asset files are found for the current class.
        """
        found_files = [file for file in os.listdir(
            directory) if self.__class__.__name__.lower() in file]
        if found_files:
            for file in found_files:
                extension = f".{file.split('.')[1]}"
                if extension in FILE_EXTENSIONS:
                    return os.path.join(directory, file)

        act_class = self.__class__.__name__.lower()
        base_class = self.__class__.__bases__[0].__name__.lower()
        raise NotImplementedError(f"no asset files found for "
                                  f"'{act_class}' {base_class}")
