#!/usr/bin/python3
"""
This module contains the entry point of the command interpreter.
"""

import cmd
import os
import json
import re
from models import storage
from utility.dynamically_create_cls import dynamicallyCreateCls
from utility.parse_value import parse_value
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
""""
console.py
    This class represents the command interpreter, and the control center
    of this project. It defines function handlers for all commands inputted
    in the console and calls the appropriate storage engine APIs to manipulate
    application data / models.
"""


class HBNBCommand(cmd.Cmd):

    prompt = "(hbnb) "
    __supported_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    # All the supported classes that globals function used
    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id. Also supports setting attributes using
        <key>=<value> syntax.
        Usage: create <class name> <param 1> <param 2> <param 3>...
        """
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in HBNBCommand.__supported_classes:
            print("** class doesn't exist **")
            return

        new_instance = eval(class_name)()

        # Process additional arguments for attributes
        for param in args[1:]:
            match = re.match(r'^(\w+)=(".*?"|\d+\.\d+|\d+)$', param)
            if match:
                key, value = match.groups()
                value = parse_value(value)
                if value is not None:
                    setattr(new_instance, key, value)

        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on the
        class name and id.
        Usage: show <class name> <id>
        """
        args = arg.split()

        if not args:
            print("** class name missing **")
            return None

        className = args[0]
        if className not in HBNBCommand.__supported_classes:
            print("** class doesn't exist **")
            return None

        if len(args) != 2:
            print("** instance id missing **")
            return None

        classId = args[1]
        key = "{}.{}".format(className, classId)
        if key not in storage.all().keys():
            print("** no instance found **")
            return None

        instance = storage.all()[key]
        print("{}".format(instance))

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id.
        Usage: destroy <class name> <id>
        """
        args = arg.split()

        if not args:
            print("** class name missing **")
            return None

        className = args[0]
        if className not in HBNBCommand.__supported_classes:
            print("** class doesn't exist **")
            return None

        if len(args) != 2:
            print("** instance id missing **")
            return None

        classId = args[1]
        key = "{}.{}".format(className, classId)
        if key not in storage.all().keys():
            print("** no instance found **")
            return None

        storage.delete(key)

    def do_all(self, arg):
        """Prints all string representation of all instances based
        or not on the class name."""
        args = arg.split()
        all_objs = storage.all()
        result = []

        if not args:
            # No class name provided, print all instances
            for obj in all_objs.values():
                result.append(str(obj))
        else:
            class_name = args[0]
            if class_name not in self.__supported_classes:
                print("** class doesn't exist **")
                return None
            # Print all instances of the specified class
            for key, obj in all_objs.items():
                if key.startswith(class_name + "."):
                    result.append(str(obj))

        print(result)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by
        adding or updating attribute."""
        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.__supported_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        attr_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return
        attr_value = args[3].strip('"')

        # Cast attribute value to the correct type
        instance = all_objs[key]
        # Default to str if attribute doesn't exist
        attr_type = type(getattr(instance, attr_name, str))
        try:
            if attr_type == int:
                attr_value = int(attr_value)
            elif attr_type == float:
                attr_value = float(attr_value)
            else:
                attr_value = str(attr_value)
        except ValueError:
            print("** value type error **")
            return

        setattr(instance, attr_name, attr_value)
        instance.save()

    def do_all(self, line):
        """
        Prints all string representations of all instances of a class.
        Usage: <class name>.all() or all <class name>
        """
        if line:
            if line not in self.__supported_classes:
                print("** class doesn't exist **")
                return
            class_name = line
            objects = [str(obj) for obj in storage.all(
                eval(class_name)).values()]
        else:
            objects = [str(obj) for obj in storage.all().values()]
        print(objects)

    def onecmd(self, line):
        """Override the default behavior to handle <class name>.all()"""
        if line.endswith('.all()'):
            class_name = line.split('.')[0]
            return self.do_all(class_name)
        return super().onecmd(line)

    def do_count(self, class_name):
        if class_name in self.__supported_classes:
            count = len(storage.all(eval(class_name)))
            print(count)
        else:
            print("** class doesn't exist **")

    def do_show2(self, className, classId):
        """Retrieve an instance based on its ID"""
        key = className + '.' + classId
        if key in storage.all(eval(className)):
            print(storage.all(eval(className))[key])
        else:
            print("** no instance found **")

    def do_destroy2(self, className, classId):
        key = "{}.{}".format(className, classId)
        if key not in storage.all().keys():
            print("** no instance found **")
            return None

        storage.delete(key)

    def do_update_cmd(self, class_name, instance_id, update_data):
        """Updates an instance based on the class name and id"""
        key = "{}.{}".format(class_name, instance_id)
        objects = storage.all()
        if key not in objects:
            print("** no instance found **")
            return

        # Check if update_data is a dictionary representation
        if update_data.startswith("{") and update_data.endswith("}"):
            try:
                update_dict = json.loads(update_data.replace("'", "\""))
                if isinstance(update_dict, dict):
                    for attribute_name, attribute_value in update_dict.items():
                        setattr(objects[key], attribute_name, attribute_value)
                    objects[key].save()
                else:
                    print("** value is not a dictionary **")
            except json.JSONDecodeError:
                print("** value is not a valid dictionary **")
        else:
            update_parts = update_data.split(", ")
            if len(update_parts) == 2:
                attribute_name = update_parts[0].strip('"')
                attribute_value = update_parts[1].strip('"')
                setattr(objects[key], attribute_name, attribute_value)
                objects[key].save()
            else:
                print("** Incorrect number of parameters **")

    def default(self, line):
        """Default behavior when command prefix is a class name"""
        parts = line.split('.')
        if len(parts) == 2:
            class_name = parts[0]
            command = parts[1]
            if class_name in self.__supported_classes:
                if command == "count()":
                    self.do_count(class_name)
                elif command.startswith("show(") and command.endswith(")"):
                    instance_id = command[5:-1].strip('"')
                    self.do_show2(class_name, instance_id)
                elif command.startswith("destroy(") and command.endswith(")"):
                    instance_id = command[9:-1].strip('"')
                    self.do_destroy2(class_name, instance_id)
                elif command.startswith("update(") and command.endswith(")"):
                    params = command[7:-1].split(", ", 2)
                    if len(params) == 3:
                        instance_id = params[0].strip('"')
                        attribute_name = params[1].strip('"')
                        attribute_value = params[2].strip('"')
                        self.do_update_cmd(
                            class_name, instance_id,
                            f"{attribute_name} {attribute_value}")
                    elif len(params) == 2:
                        instance_id = params[0].strip('"')
                        update_data = params[1]
                        self.do_update_cmd(
                            class_name, instance_id, update_data)
                else:
                    print(f"** Unknown command: {command} **")
            else:
                print("** class doesn't exist **")
        else:
            super().default(line)

    def do_help(self, arg):

        """To get help on a command, type help <topic>.
        """
        return super().do_help(arg)

    def do_EOF(self, line):
        """Inbuilt EOF command to gracefully catch errors.
        """
        print("")
        return True

    def emptyline(self):
        """Override default `empty line + return` behaviour.
        """
        pass

    def do_clear(self, arg):
        """
        Clears the console screen.
        Usage: clear
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def do_quit(self, arg):
        """Quit command to exit the program.
        """
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
