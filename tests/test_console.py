#!/usr/bin/python3
"""Defines unittests for console.py.
Unittest classes:
    TestHBNBCommand_prompting
    TestHBNBCommand_help
    TestHBNBCommand_exit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_all
    TestHBNBCommand_destroy
    TestHBNBCommand_update
"""
import unittest
from unittest.mock import patch, MagicMock
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from io import StringIO
import sys
import os


class TestConsole(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        self.stdout = StringIO()
        sys.stdout = self.stdout
        # Clear the storage for a clean state
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Tear down test environment"""
        self.stdout = None
        sys.stdout = sys.__stdout__
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def _run_command(self, command):
        self.console.onecmd(command)
        return self.stdout.getvalue().strip()

    def _clear_stdout(self):
        self.stdout.truncate(0)
        self.stdout.seek(0)

    def test_create_BaseModel(self):
        """Test create command for BaseModel"""
        output = self._run_command("create BaseModel")
        created_id = output.strip()
        self.assertIn(f"BaseModel.{created_id}", storage.all())
        self._clear_stdout()

    def test_create_User(self):
        """Test create command for User"""
        output = self._run_command("create User")
        created_id = output.strip()
        self.assertIn(f"User.{created_id}", storage.all())
        self._clear_stdout()

    @patch('models.storage.save')
    @patch('models.storage.new')
    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_parameters(self, mock_stdout, mock_storage_new, mock_storage_save):
        """Test create command with parameters"""
        mock_storage_new.return_value = None
        mock_storage_save.return_value = None

        self.console.onecmd('create State name="California"')
        output = mock_stdout.getvalue().strip()

        # Check if the instance is created and saved
        mock_storage_new.assert_called_once()
        mock_storage_save.assert_called_once()

        # Retrieve the created instance
        created_instance = mock_storage_new.call_args[0][0]

        # Verify the output ID matches the created instance's ID
        self.assertEqual(output, created_instance.id)

        # Check the name attribute
        self.assertEqual(created_instance.name, "California")

    def test_show_BaseModel(self):
        """Test show command for BaseModel"""
        instance = BaseModel()
        instance.save()
        command = f"show BaseModel {instance.id}"
        output = self._run_command(command)
        self.assertIn(instance.id, output)
        self._clear_stdout()

    def test_show_User(self):
        """Test show command for User"""
        instance = User()
        instance.save()
        command = f"show User {instance.id}"
        output = self._run_command(command)
        self.assertIn(instance.id, output)
        self._clear_stdout()

    def test_destroy_BaseModel(self):
        """Test destroy command for BaseModel"""
        instance = BaseModel()
        instance.save()
        command = f"destroy BaseModel {instance.id}"
        self._run_command(command)
        self.assertNotIn(f"BaseModel.{instance.id}", storage.all())
        self._clear_stdout()

    def test_destroy_User(self):
        """Test destroy command for User"""
        instance = User()
        instance.save()
        command = f"destroy User {instance.id}"
        self._run_command(command)
        self.assertNotIn(f"User.{instance.id}", storage.all())
        self._clear_stdout()

    def test_all(self):
        """Test all command for all models"""
        instance1 = BaseModel()
        instance2 = User()
        instance1.save()
        instance2.save()
        command = "all"
        output = self._run_command(command)
        self.assertIn(instance1.id, output)
        self.assertIn(instance2.id, output)
        self._clear_stdout()

    def test_all_BaseModel(self):
        """Test all command for BaseModel"""
        instance = BaseModel()
        instance.save()
        command = "all BaseModel"
        output = self._run_command(command)
        self.assertIn(instance.id, output)
        self._clear_stdout()

    def test_update_BaseModel(self):
        """Test update command for BaseModel"""
        instance = BaseModel()
        instance.save()
        instance.name = "Old Name"
        instance.save()
        command = f"update BaseModel {instance.id} name \"New\""
        self._run_command(command)
        instance = storage.all()[f"BaseModel.{instance.id}"]
        self.assertEqual(instance.name, "New")
        self._clear_stdout()

    def test_update_method_BaseModel(self):
        """Test .update("id", "attribute_name", "string_value") method for BaseModel"""
        instance = BaseModel()
        instance.save()
        instance.name = "Old Name"
        instance.save()
        command = f'BaseModel.update("{instance.id}", "name", "New Name")'
        self._run_command(command)
        instance = storage.all()[f"BaseModel.{instance.id}"]
        self.assertEqual(instance.name, "New Name")
        self._clear_stdout()

    def test_count_BaseModel(self):
        """Test count command for BaseModel"""
        instance1 = BaseModel()
        instance2 = BaseModel()
        instance1.save()
        instance2.save()
        command = "BaseModel.count()"
        output = self._run_command(command)
        self.assertEqual(output, "2")
        self._clear_stdout()

    def test_count_User(self):
        """Test count command for User"""
        instance = User()
        instance.save()
        command = "User.count()"
        output = self._run_command(command)
        self.assertEqual(output, "1")
        self._clear_stdout()

    def test_all_method_BaseModel(self):
        """Test .all() method for BaseModel"""
        instance = BaseModel()
        instance.save()
        command = "BaseModel.all()"
        output = self._run_command(command)
        self.assertIn(instance.id, output)
        self._clear_stdout()

    def test_show_method_BaseModel(self):
        """Test .show("id") method for BaseModel"""
        instance = BaseModel()
        instance.save()
        command = f"BaseModel.show(\"{instance.id}\")"
        output = self._run_command(command)
        self.assertIn(instance.id, output)
        self._clear_stdout()

    def test_destroy_method_BaseModel(self):
        """Test .destroy("id") method for BaseModel"""
        instance = BaseModel()
        instance.save()
        command = f"BaseModel.destroy(\"{instance.id}\")"
        self._run_command(command)
        self.assertNotIn(f"BaseModel.{instance.id}", storage.all())
        self._clear_stdout()

    def test_update_method_BaseModel(self):
        """Test .update("id", "attribute_name", "string_value") method for BaseModel"""
        instance = BaseModel()
        instance.save()
        instance.name = "Old Name"
        instance.save()
        command = f'BaseModel.update("{instance.id}", "name", "New")'
        self._run_command(command)
        instance = storage.all()[f"BaseModel.{instance.id}"]
        self.assertEqual(instance.name, "Old Name")
        self._clear_stdout()

    def _clear_stdout(self):
        self.stdout.truncate(0)
        self.stdout.seek(0)

if __name__ == "__main__":
    unittest.main()
