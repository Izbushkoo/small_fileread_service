import csv
from io import StringIO


class CSVIsEmpty(Exception):
    pass


class CSVHandler:

    __field_names = [
        "title", "header", "image_url", "rating", "description", "description_items"
    ]

    def __init__(self, contents: bytes):
        self._string_buffer = StringIO(contents.decode("utf-8-sig"))
        self._list_of_dicts = self._map_to_dicts()

    @property
    def list_of_dicts(self):
        return self._list_of_dicts

    def _map_to_dicts(self):
        new_list = []
        for item in list(csv.DictReader(self._string_buffer, fieldnames=self.__field_names)):
            new_item = {}
            for key in self.__field_names:
                if key == "description_items":
                    new_item[key] = item[key].split("; ")
                elif key == "rating":
                    new_item[key] = int(item[key])
                else:
                    new_item[key] = item[key]
            new_list.append(new_item)
        return new_list

