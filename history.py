# 過去のトレーニングデータを管理
# 過去の重量・回数を保存，更新
# 過去のトレーニングデータを表示
# データはJSON形式で保存

import os
import json
from dataclasses import dataclass
from typing import Dict, Optional
from menu_manager import MenuManager

@dataclass
class TrainingRecord:
    """トレーニング記録を保持するデータクラス"""
    last_a: float
    last_b: float
    best_a: float
    best_b: float

class TrainingHistory:
    """トレーニング履歴を管理するクラス"""
    FILE_PATH = "history_data.json"

    def __init__(self):
        """トレーニング履歴をロード"""
        self.history: Dict[str, TrainingRecord] = self._load_history()
        self.menu_manager = MenuManager()

    def _load_history(self) -> Dict[str, TrainingRecord]:
        """過去のトレーニングデータを読み込む"""
        if not os.path.exists(self.FILE_PATH):
            return {}

        try:
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    menu_name: TrainingRecord(
                        last_a=record["last_a"],
                        last_b=record["last_b"],
                        best_a=record["best_a"],
                        best_b=record["best_b"]
                    )
                    for menu_name, record in data.items()
                }
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[警告] 履歴データの読み込みに失敗しました: {e}")
            return {}

    def save_history(self) -> None:
        """トレーニングデータを保存"""
        try:
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        menu_name: {
                            "last_a": record.last_a,
                            "last_b": record.last_b,
                            "best_a": record.best_a,
                            "best_b": record.best_b
                        }
                        for menu_name, record in self.history.items()
                    },
                    f,
                    ensure_ascii=False,
                    indent=2
                )
        except Exception as e:
            print(f"[エラー] 履歴データの保存に失敗しました: {e}")

    def update_history(self, menu_name: str, last_a: float, last_b: float) -> None:
        """トレーニングデータを更新"""
        if not self._check_menu(menu_name):
            return

        menu_name = self.menu_manager.find_menu_by_tag_or_name(menu_name)
        if not menu_name:
            return

        # 現在の記録を取得
        current_record = self.history.get(menu_name, TrainingRecord(0, 0, 0, 0))
        
        # 最高記録を更新
        best_a = max(current_record.best_a, last_a)
        best_b = max(current_record.best_b, last_b)
        
        # 記録を更新
        self.history[menu_name] = TrainingRecord(
            last_a=last_a,
            last_b=last_b,
            best_a=best_a,
            best_b=best_b
        )
        
        self.save_history()
        print(f"[更新] {menu_name}: ({last_a}, {last_b}) を保存しました。最高記録: ({best_a}, {best_b})")

    def get_last_training(self, menu_name: str) -> Optional[Dict[str, float]]:
        """最後のトレーニングデータを取得"""
        menu_name = self.menu_manager.find_menu_by_tag_or_name(menu_name)
        if not menu_name:
            return None

        record = self.history.get(menu_name)
        if not record:
            return {"last_a": 0, "last_b": 0}

        return {
            "last_a": record.last_a,
            "last_b": record.last_b,
            "best_a": record.best_a,
            "best_b": record.best_b
        }

    def remove_history(self, menu_name: str) -> None:
        """指定したメニューの履歴を削除"""
        menu_name = self.menu_manager.find_menu_by_tag_or_name(menu_name)
        if not menu_name:
            return

        if menu_name in self.history:
            del self.history[menu_name]
            self.save_history()
            print(f"[削除] {menu_name} の履歴を削除しました。")
        else:
            print(f"[エラー] {menu_name} の履歴は存在しません。")

    def clear_history(self) -> None:
        """全トレーニング履歴を削除"""
        self.history.clear()
        self.save_history()
        print("[リセット] 全トレーニング履歴を削除しました。")

    def _check_menu(self, menu_name: str) -> bool:
        """メニューが存在するか確認"""
        if not self.menu_manager.get_menu(menu_name):
            print(f"[エラー] {menu_name} は存在しません。")
            return False
        return True


if __name__ == "__main__":
    th = TrainingHistory()
    menu_name = "ランニング"
    lt = th.get_last_training(menu_name)
    print(f"{menu_name} の最後のトレーニングデータ: {lt}")