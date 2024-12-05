# test_reminder.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import shutil
from pathlib import Path
from user_management.reminder import ReminderSystem

class TestReminder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nSetting up TestReminder class...")
        cls.base_dir = Path("./test_data")
        cls.base_dir.mkdir(exist_ok=True)
        cls.data_dir = cls.base_dir / "data"
        cls.data_dir.mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        print("\nCleaning up TestReminder class...")
        try:
            if cls.base_dir.exists():
                shutil.rmtree(cls.base_dir)
        except Exception as e:
            print(f"Warning: Could not clean up test directory: {e}")

    def setUp(self):
        self.reminder_system = ReminderSystem(self.base_dir)
        # 添加一些测试提醒
        self.reminder_system.set_reminder("TestUser", 1, "Test reminder 1")
        self.reminder_system.set_reminder("TestUser", 2, "Test reminder 2")

    def tearDown(self):
        self.reminder_system = None

    def test_set_and_get_reminder(self):
        """Test setting and retrieving reminders"""
        self.reminder_system.set_reminder("TestUser", 3, "Test reminder 3")
        self.assertIn("TestUser", self.reminder_system.reminders)
        self.assertIn(3, self.reminder_system.reminders["TestUser"])
        self.assertEqual(
            self.reminder_system.reminders["TestUser"][3],
            "Test reminder 3"
        )
        
        self.reminder_system.set_reminder("TestUser", 3, "Updated reminder")
        self.assertEqual(
            self.reminder_system.reminders["TestUser"][3],
            "Updated reminder"
        )

    def test_clear_reminder(self):
        """Test clearing specific reminders"""
        self.reminder_system.clear_reminder("TestUser", 1)
        self.assertNotIn(1, self.reminder_system.reminders["TestUser"])
        self.assertIn(2, self.reminder_system.reminders["TestUser"])
        
        # 测试清除不存在的提醒
        self.reminder_system.clear_reminder("TestUser", 999)
        self.reminder_system.clear_reminder("NonexistentUser", 1)

    def test_check_alerts(self):
        """Test low stock alerts"""
        low_stock_warnings = [
            (4, "Med1", 2),
            (5, "Med2", 1)
        ]
        self.reminder_system.check_alerts("TestUser", low_stock_warnings)
        
        self.assertIn(4, self.reminder_system.reminders["TestUser"])
        self.assertIn(5, self.reminder_system.reminders["TestUser"])
        self.assertIn("Med1", self.reminder_system.reminders["TestUser"][4])
        self.assertIn("Med2", self.reminder_system.reminders["TestUser"][5])

    def test_clear_all_reminders(self):
        """Test clearing all reminders for a user"""
        self.reminder_system.clear_all_reminders("TestUser")
        self.assertEqual(len(self.reminder_system.reminders["TestUser"]), 0)
        
        # 测试清除不存在用户的提醒
        self.reminder_system.clear_all_reminders("NonexistentUser")

    def test_persistence(self):
        """Test reminder data persistence"""
        # 创建新的提醒系统实例（会从文件加载数据）
        new_reminder_system = ReminderSystem(self.base_dir)
        
        # 验证数据是否正确保存和加载
        self.assertIn("TestUser", new_reminder_system.reminders)
        self.assertIn(1, new_reminder_system.reminders["TestUser"])
        self.assertIn(2, new_reminder_system.reminders["TestUser"])
        self.assertEqual(
            new_reminder_system.reminders["TestUser"][1],
            "Test reminder 1"
        )

if __name__ == '__main__':
    unittest.main()