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
    def get_asset(self, directory):
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
