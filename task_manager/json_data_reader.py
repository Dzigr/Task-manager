import json
import os


def get_json_data(file_name):
    """
    Read the data from json file.

    Parameters: file_name: name of the file with fixture.

    Returns: data from fixture.
    """
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'fixtures',
        file_name,
    )

    with open('{path}.json'.format(path=file_path), 'r') as read_file:
        return json.load(read_file)
