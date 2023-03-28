import os

from rembg import remove

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(ROOT_DIR, 'assets')
RESOURCE_CARDS_DIR = os.path.join(ASSET_DIR, 'resource')
DEVELOPMENT_CARDS_DIR = os.path.join(ASSET_DIR, 'development')
TILE_CARDS_DIR = os.path.join(ASSET_DIR, 'tiles')
FILE_EXTENSIONS = [".jpg", ".png", ".gif", ".jpeg"]


def prepare_assets(directory):
    files = os.listdir(directory)
    print()

    for file in files:
        if any([file.endswith(extension) for extension in FILE_EXTENSIONS]):
            input_path = os.path.join(directory, file)

            print(input_path)

            output_path = os.path.join(directory, f'new_{file}')

            with open(input_path, 'rb') as i:
                with open(output_path, 'wb') as o:
                    input = i.read()
                    output = remove(input)
                    o.write(output)

            os.remove(input_path)
            os.rename(output_path, input_path)

        else:
            print(f"Error: {file} has an unsupported file extension")
            continue
