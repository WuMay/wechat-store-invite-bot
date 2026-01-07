import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class RecordManager:
    """邀约记录管理器"""

    def __init__(self, record_file: str):
        self.record_file = record_file
        self.records: Dict[str, List[Dict]] = {}
        self._load_records()

    def _load_records(self):
        """加载记录文件"""
        if os.path.exists(self.record_file):
            try:
                with open(self.record_file, 'r', encoding='utf-8') as f:
                    self.records = json.load(f)
            except Exception as e:
                print(f"加载记录文件失败: {e}")
                self.records = {}
        else:
            self.records = {}

    def _save_records(self):
        """保存记录到文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.record_file), exist_ok=True)
            with open(self.record_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存记录文件失败: {e}")

    def is_invited(self, talent_id: str) -> bool:
        """检查达人是否已邀约"""
        return talent_id in self.records

    def add_record(self, talent_id: str, talent_name: str, status: str = "success"):
        """添加邀约记录"""
        if talent_id not in self.records:
            self.records[talent_id] = []

        record = {
            "name": talent_name,
            "status": status,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.records[talent_id].append(record)
        self._save_records()

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        total = len(self.records)
        success = sum(1 for records in self.records.values()
                     if any(r["status"] == "success" for r in records))
        failed = total - success

        return {
            "total": total,
            "success": success,
            "failed": failed
        }

    def get_all_records(self) -> Dict:
        """获取所有记录"""
        return self.records

    def print_statistics(self):
        """打印统计信息"""
        stats = self.get_statistics()
        print("\n" + "="*50)
        print("邀约统计")
        print("="*50)
        print(f"总计邀约: {stats['total']} 人")
        print(f"成功: {stats['success']} 人")
        print(f"失败: {stats['failed']} 人")
        print("="*50)
