import os
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

@dataclass
class ParameterConfig:
    """パラメータの設定を保持するデータクラス"""
    unit: str
    step: float
    max: float = 200.0

@dataclass
class MenuConfig:
    """メニューの設定を保持するデータクラス"""
    target: str
    param_a: ParameterConfig
    param_b: ParameterConfig

class MenuManager:
    """メニュー管理クラス"""
    FILE_PATH = "menu.txt"

    def __init__(self):
        """メニュー管理クラスの初期化"""
        self.menus: Dict[str, MenuConfig] = self._load_menus()

    def _load_menus(self) -> Dict[str, MenuConfig]:
        """menu.txtからメニューを読み込む"""
        menus: Dict[str, MenuConfig] = {}
        
        if not os.path.exists(self.FILE_PATH):
            print(f"[警告] {self.FILE_PATH} が存在しません。")
            return menus

        try:
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        parts = line.strip().split(",")
                        if len(parts) not in [6, 8]:
                            print(f"[警告] {line_num}行目: 不正なフォーマットです。")
                            continue

                        name = parts[0]
                        target = parts[1]
                        param_a = ParameterConfig(
                            unit=parts[2],
                            step=float(parts[3])
                        )
                        param_b = ParameterConfig(
                            unit=parts[4],
                            step=float(parts[5])
                        )

                        # 最大値が指定されている場合
                        if len(parts) == 8:
                            param_a.max = float(parts[6])
                            param_b.max = float(parts[7])
                        else:
                            param_a.max = 200
                            param_b.max = 200
                            
                        menus[name] = MenuConfig(
                            target=target,
                            param_a=param_a,
                            param_b=param_b
                        )

                    except (ValueError, IndexError) as e:
                        print(f"[警告] {line_num}行目: データの解析に失敗しました - {e}")
                        continue

        except Exception as e:
            print(f"[エラー] ファイルの読み込みに失敗しました - {e}")

        return menus

    def get_menu(self, menu_input: str) -> Optional[MenuConfig]:
        """指定したメニューの情報を取得"""
        name = self.find_menu_by_tag_or_name(menu_input)
        return self.menus.get(name)

    def get_all_menus(self) -> Dict[str, MenuConfig]:
        """全メニューを取得"""
        return self.menus

    def get_menu_names(self) -> List[str]:
        """全メニュー名を取得"""
        return list(self.menus.keys())

    def get_menu_tagandnames(self) -> List[str]:
        """全メニュー名とタグを取得"""
        return [f"({menu.target}) {name}" for name, menu in self.menus.items()]

    def find_menu_by_tag_or_name(self, input_str: str) -> Optional[str]:
        """タグまたは名前でメニューを検索し、名前を返す"""
        if not input_str:
            return None

        # 直接の名前での検索
        if input_str in self.menus:
            return input_str

        # タグ付きの名前での検索
        if input_str.startswith("(") and ")" in input_str:
            try:
                _, name = input_str[1:].split(") ", 1)
                if name in self.menus:
                    return name
            except ValueError:
                pass

        return None

    @staticmethod
    def check_menu_file() -> Tuple[bool, str]:
        """menu.txtの存在確認"""
        if not os.path.exists(MenuManager.FILE_PATH):
            return False, f"{MenuManager.FILE_PATH} が存在しません。"
        return True, f"{MenuManager.FILE_PATH} が存在します。"


if __name__ == "__main__":
    # メニューファイルの確認
    exists, message = MenuManager.check_menu_file()
    print(message)

    # メニューマネージャーのテスト
    mm = MenuManager()
    print("\n利用可能なメニュー:")
    for name in mm.get_menu_names():
        print(f"- {name}")

    # 特定のメニューの情報を表示
    test_menu = "アブドミナル"
    menu_info = mm.get_menu(test_menu)
    if menu_info:
        print(f"\n{test_menu}の情報:")
        print(f"ターゲット: {menu_info.target}")
        print(f"パラメータA: {menu_info.param_a.unit} (ステップ: {menu_info.param_a.step}, 最大: {menu_info.param_a.max})")
        print(f"パラメータB: {menu_info.param_b.unit} (ステップ: {menu_info.param_b.step}, 最大: {menu_info.param_b.max})")
    else:
        print(f"\n{test_menu}は見つかりませんでした。")
