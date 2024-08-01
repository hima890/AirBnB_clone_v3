#!/usr/bin/python3
"""
Dynamically Create classes
"""
from models.base_model import BaseModel
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def dynamicallyCreateCls(className):
    """
    Dynamically creates an instance of a class based on its name.

    Args:
        className (str): The name of the class to instantiate.

    Returns:
        None: If the class doesn't exist or an exception occurs
        during instantiation.

    Raises:
        KeyError: If the specified class name doesn't exist in
        the global scope.
        Exception: Any other unexpected exceptions that occur
        during instantiation.

    Prints:
        str: The ID of the newly created instance, if successful.

    Example:
        If className = "MyClass" and MyClass is a defined
        class with a save() method,
        this function will instantiate MyClass, save the
        instance, and print its ID.

    """
    try:
        # Dynamically get the class using globals() and getattr()
        cls = globals()[className]

        # Create a new class instance
        new_instance = cls()

        # Save the instance (assuming save() method exists in the class)
        new_instance.save()

        # Print the instance id (assuming id attribute exists in the instance)
        print(new_instance.id)

    except KeyError:
        print("** class doesn't exist **")
        return None  # Return None to indicate failure

    except Exception as e:
        print(e)  # Print any other exception that might occur
        return None  # Return None to indicate failure
