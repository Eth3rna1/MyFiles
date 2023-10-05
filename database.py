import json
import os
from typing import Any


def _correct_file_name(name: str, file_type: str) -> str:
    """
    Get the correct file type

    (name).(file_type)
    """
    count = name.count(".")
    if count == 1 or count == 0:
        if "." in name:
            TYPE = name.split(".")[1]
            if TYPE == file_type:
                return name
            else:
                raise Exception(f'"{name}" must be a ".{file_type}" file')
        else:
            return f"{name}.{file_type}"
    else:
        raise Exception(f'"{name}" must be contain 1 or 0 "."')


class JsonDatabase:
    def __init__(self, file_name: str = "ToolDatabase.json") -> None:
        file_name = _correct_file_name(file_name, "json")
        self.file = str(file_name)
        self.key = None
        self.value = None
        self.db = {}
        self.indentation = 4
        self.dict = {}

    def create(self) -> None:
        """
        Create the database.
        
        It is advised to use the .exist() method instead of this one.
        """
        with open(self.file, "w") as file:
            file.write("")

    def exist(self) -> bool:
        """
        Returns True if the database file exists in the working directory.
        If not, it will create it and return None
        """
        if os.path.exists(self.file):
            return True
        JsonDatabase(self.file).create()

    def read(self, return_string: bool = False, indentation: int = 4) -> dict | str:
        """
        return a dictionary instance of the database. if return_string, it
        will return a prettified string instance of the database. Else, it
        will return the normal dictionary.
        
        :param bool return_string: True = string instance, False = dictionary instance
        :param int indentation: the amount of spaces used if a str instance is returned
        """
        JsonDatabase(self.file).exist()
        try:
            with open(self.file, "r") as file:
                self.db = json.loads(file.read())
        except Exception:
            self.db = {}
        if return_string:
            return str(json.dumps(self.db, indent=indentation, sort_keys=True))
        return self.db

    def __call__(self, *args: Any, **kwds: Any) -> dict:
        """
        Return the database
        """
        return JsonDatabase(self.file).read()

    def add(self, payload: dict):
        """
        Appends the dictionary to the database dictionary. Just like a dictionary, if the regarded
        payload already exists, the existing dict will be overrided in the database
        
        :param dict payload: The dictionary instance you want to add
        """
        data = JsonDatabase(self.file).read()
        data.update(payload)
        with open(self.file, "w") as file:
            file.write(json.dumps(data, indent=4))

    def remove(self, key: str) -> dict:
        """
        Remove the key along with its value.
        After doing so, it will re-write the database with
        the exception of the key removed
        
        :param str key: The key you want to remove from the database
        """
        d = JsonDatabase(self.file)
        data = d.read()
        dictionary = d.get_key(key).dict
        del data[key]
        with open(self.file, "w") as file:
            file.write(json.dumps(data, indent=self.indentation))
        return dict

    def drop_database(self, ask: bool = True) -> dict:
        """
        Delete the database
        
        ==================================================
            THERE IS NO GOING BACK AFTER IT IS DELETED
        ==================================================
        
        :param bool ask: Ask for confirmation before deleting the database
        """
        if ask:
            confirmation = input(
                'Are you sure you want to {} the database, "{}"? [y/n] '.title().format(
                    "ERASE", self.file
                )
            ).lower()
        else:
            confirmation = "y"
        if confirmation == "y":
            os.remove(self.file)
            print(f'Database "{self.file}" Has Been Deleted!')
            return self.db

    def get_key(self, key: str):
        """
        Just like the .get() method from the dict class. This method, 
        will return itself but with updated variables like key and value.
        If it cannot be found, it will return None
        
        :param str key: The key you want to retrieve along with its value
        
        .key = retrieve the key
        .value = retrieve the value
        .dict = retrieve the key and value in this format: {key : value}
        """
        db = JsonDatabase(self.file).read()
        if db.get(key, None):
            self.key = key
            self.value = db[key]
            self.dict = {self.key: self.value}
        return self
