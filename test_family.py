# test_family.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import shutil
from pathlib import Path
from user_management.family import FamilyManagement
from user_management.reminder import ReminderSystem

class TestFamily(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nSetting up TestFamily class...")
        cls.base_dir = Path("./test_data")
        cls.base_dir.mkdir(exist_ok=True)
        cls.data_dir = cls.base_dir / "data"
        cls.data_dir.mkdir(exist_ok=True)
        cls.reminder_system = ReminderSystem(cls.base_dir)

    @classmethod
    def tearDownClass(cls):
        print("\nCleaning up TestFamily class...")
        try:
            if cls.base_dir.exists():
                shutil.rmtree(cls.base_dir)
        except Exception as e:
            print(f"Warning: Could not clean up test directory: {e}")

    def setUp(self):
        self.family_manager = FamilyManagement(
            self.base_dir,
            self.reminder_system
        )
        # 清除所有现有成员
        for member in list(self.family_manager.members.keys()):
            self.family_manager.delete_member(member)

    def tearDown(self):
        self.family_manager = None

    def test_add_member(self):
        """Test adding family members"""
        # 首先确保测试的成员不存在
        if "John" in self.family_manager.members:
            self.family_manager.delete_member("John")
        if "Jane" in self.family_manager.members:
            self.family_manager.delete_member("Jane")
            
        self.assertTrue(self.family_manager.add_member("John"))
        self.assertTrue(self.family_manager.add_member("Jane"))
        self.assertIn("John", self.family_manager.members)
        self.assertIn("Jane", self.family_manager.members)
        self.assertFalse(self.family_manager.add_member("John"))  # 测试重复添加

    def test_member_switching(self):
        """Test switching between family members"""
        # 确保成员不存在
        if "John" in self.family_manager.members:
            self.family_manager.delete_member("John")
        if "Jane" in self.family_manager.members:
            self.family_manager.delete_member("Jane")
            
        self.family_manager.add_member("John")
        self.family_manager.add_member("Jane")
        
        self.assertTrue(self.family_manager.switch_member("John"))
        self.assertEqual(self.family_manager.current_member, "John")
        self.assertTrue(self.family_manager.switch_member("Jane"))
        self.assertEqual(self.family_manager.current_member, "Jane")
        self.assertFalse(self.family_manager.switch_member("NonExistent"))

    def test_member_deletion(self):
        """Test deleting family members"""
        # 准备测试数据
        self.family_manager.add_member("John")
        
        # 测试删除存在的成员
        self.assertTrue(self.family_manager.delete_member("John"))
        self.assertNotIn("John", self.family_manager.members)
        
        # 测试删除不存在的成员
        self.assertFalse(self.family_manager.delete_member("NonExistent"))

if __name__ == '__main__':
    unittest.main()