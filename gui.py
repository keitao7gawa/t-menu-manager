import ui
import console
import keyboard
from menu_manager import MenuManager
from history import TrainingHistory

class TrainingApp(ui.View):
    def __init__(self):
        self.menu_manager = MenuManager()
        self.history = TrainingHistory()
        
        # カラー設定
        self.background_color = '#E8F5E9'
        self.record_breaking_color = '#F44336'
        self.record_button_active_color = '#7B1FA2'
        self.record_button_inactive_color = '#BDBDBD'
        
        # メニュー選択部分の初期化
        self._init_menu_selection()
        
        # パラメータ入力部分の初期化
        self._init_parameter_inputs()
        
        # 出力ボタンの初期化
        self._init_output_buttons()
        
        # 初期選択の設定
        self._select_first_menu()
        
        # ビューの基本設定
        self.flex = 'WH'
        self.is_keyboard = keyboard.is_keyboard()
        
        # テーブルビューの設定
        self._configure_table_view()

    def _init_menu_selection(self):
        """メニュー選択部分のUI要素を初期化"""
        self.menu_label = ui.Label(text="📋 トレーニングメニュー", frame=(10, 10, 300, 30))
        self.menu_label.font = ('Helvetica-Bold', 13)
        self.menu_label.text_color = '#1E88E5'
        self.add_subview(self.menu_label)
        
        self.menu_table = ui.TableView(frame=(10, 40, 350, 150))
        self.menu_table.data_source = ui.ListDataSource(self.menu_manager.get_menu_tagandnames())
        self.menu_table.delegate = self
        self.add_subview(self.menu_table)

    def _init_parameter_inputs(self):
        """パラメータ入力部分のUI要素を初期化"""
        # パラメータAの初期化
        self._init_parameter_a()
        
        # パラメータBの初期化
        self._init_parameter_b()

    def _init_parameter_a(self):
        """パラメータAのUI要素を初期化"""
        self.param_a_name = "パラメータA"
        self.param_a_label = ui.Label(text=f"0.0 {self.param_a_name}", frame=(10, 200, 200, 30))
        self.param_a_label.alignment = ui.ALIGN_CENTER
        self.param_a_label.font = ('Helvetica-Bold', 20)
        self.param_a_label.text_color = '#1A237E'
        self.add_subview(self.param_a_label)
        
        self._create_parameter_controls('a')

    def _init_parameter_b(self):
        """パラメータBのUI要素を初期化"""
        self.param_b_name = "パラメータB"
        self.param_b_label = ui.Label(text=f"0 {self.param_b_name}", frame=(10, 280, 200, 30))
        self.param_b_label.alignment = ui.ALIGN_CENTER
        self.param_b_label.font = ('Helvetica-Bold', 20)
        self.param_b_label.text_color = '#1A237E'
        self.add_subview(self.param_b_label)
        
        self._create_parameter_controls('b')

    def _create_parameter_controls(self, param_type):
        """パラメータのコントロール（スライダー、ボタン）を作成"""
        y_position = 240 if param_type == 'a' else 320
        
        # マイナスボタン
        minus_button = ui.Button(title="-", frame=(10, y_position, 30, 30))
        minus_button.action = getattr(self, f"decrease_param_{param_type}")
        minus_button.font = ('Helvetica-Bold', 20)
        minus_button.background_color = '#FF5252'
        minus_button.tint_color = 'white'
        minus_button.corner_radius = 20
        self.add_subview(minus_button)
        setattr(self, f"param_{param_type}_minus_button", minus_button)
        
        # スライダー
        slider = ui.Slider(frame=(50, y_position, 200, 30))
        slider.continuous = False
        slider.action = getattr(self, f"update_param_{param_type}")
        slider.value = 0.0
        slider.tint_color = '#42A5F5'
        self.add_subview(slider)
        setattr(self, f"param_{param_type}_slider", slider)
        
        # プラスボタン
        plus_button = ui.Button(title="+", frame=(260, y_position, 30, 30))
        plus_button.action = getattr(self, f"increase_param_{param_type}")
        plus_button.font = ('Helvetica-Bold', 20)
        plus_button.background_color = '#4CAF50'
        plus_button.tint_color = 'white'
        plus_button.corner_radius = 20
        self.add_subview(plus_button)
        setattr(self, f"param_{param_type}_plus_button", plus_button)

    def _init_output_buttons(self):
        """出力ボタンのUI要素を初期化"""
        # 種目名出力ボタン
        self.menu_output_button = ui.Button(title="📝 種目名", frame=(10, 400, 100, 40))
        self.menu_output_button.action = self.output_menu_name
        self.menu_output_button.font = ('Helvetica-Bold', 15)
        self.menu_output_button.background_color = '#1976D2'
        self.menu_output_button.tint_color = 'white'
        self.menu_output_button.corner_radius = 15
        self.add_subview(self.menu_output_button)
        
        # 記録ボタン
        self.record_output_button = ui.Button(title="💪 記録", frame=(120, 400, 100, 40))
        self.record_output_button.action = self.output_record
        self.record_output_button.font = ('Helvetica-Bold', 15)
        self.record_output_button.background_color = self.record_button_inactive_color
        self.record_output_button.tint_color = 'white'
        self.record_output_button.corner_radius = 15
        self.add_subview(self.record_output_button)

    def _select_first_menu(self):
        """最初のメニューを選択"""
        if self.menu_table.data_source.items:
            self.menu_table.selected_row = (0, 0)
            self.tableview_did_select(self.menu_table, 0, 0)

    def _configure_table_view(self):
        """テーブルビューの設定を行う"""
        self.menu_table.row_height = 50
        self.menu_table.data_source.font = ('Helvetica', 10.5)
        self.menu_table.background_color = '#FFFFFF'
        self.menu_table.border_width = 1
        self.menu_table.border_color = '#81C784'
        self.menu_table.corner_radius = 10

    def _calculate_parameter_value(self, slider_value, param_min=0, param_max=200, param_step=1):
        """スライダーの値をパラメータ値に変換"""
        param_value = param_min + slider_value * (param_max - param_min)
        if param_step.is_integer():
            return int(round(param_value))
        return round(param_value, len(str(param_step).split('.')[1]))

    def _calculate_slider_value(self, param_value, param_min=0, param_max=200):
        """パラメータ値をスライダー値に変換"""
        return (param_value - param_min) / (param_max - param_min)

    def _update_parameter_label(self, param_type):
        """パラメータのラベルを更新"""
        param_value = self._calculate_parameter_value(
            getattr(self, f"param_{param_type}_slider").value,
            0,
            getattr(self, f"param_{param_type}_max"),
            getattr(self, f"param_{param_type}_step")
        )
        
        # stepの値に基づいて表示形式を決定
        step = getattr(self, f"param_{param_type}_step")
        if isinstance(step, int):
            display_value = int(param_value)
        else:
            display_value = round(param_value, len(str(step).split('.')[1]))
        
        label = getattr(self, f"param_{param_type}_label")
        label.text = f"{display_value} {getattr(self, f'param_{param_type}_name')}"
        
        # 最高記録を超えているかチェック
        if param_value > getattr(self, f"best_{param_type}"):
            label.text_color = self.record_breaking_color
        else:
            label.text_color = '#1A237E'
        
        self._update_record_button_state()

    def _update_record_button_state(self):
        """記録ボタンの状態を更新"""
        param_a_value = self._calculate_parameter_value(
            self.param_a_slider.value,
            0,
            self.param_a_max,
            self.param_a_step
        )
        param_b_value = self._calculate_parameter_value(
            self.param_b_slider.value,
            0,
            self.param_b_max,
            self.param_b_step
        )
        
        can_record = not ((param_a_value == 0 and self.param_a_step != 0) or 
                         (param_b_value == 0 and self.param_b_step != 0))
        
        self.record_output_button.background_color = (
            self.record_button_active_color if can_record 
            else self.record_button_inactive_color
        )
        self.record_output_button.enabled = can_record

    def _handle_record_output(self, menu_name, param_a, param_b):
        """記録出力の処理を行う"""
        # 最高記録の更新
        is_record_a = param_a > self.best_a
        is_record_b = param_b > self.best_b
        
        if is_record_a:
            self.best_a = param_a
        if is_record_b:
            self.best_b = param_b
        
        # 履歴の更新
        self.history.update_history(menu_name, param_a, param_b)
        
        # 出力テキストの生成と挿入
        output_text = f"  - {param_a} {self.param_a_name}, {param_b} {self.param_b_name}\n"
        if keyboard.is_keyboard():
            keyboard.insert_text(output_text)
        
        # 結果メッセージの表示
        if is_record_a or is_record_b:
            console.hud_alert("🏆 新記録達成！おめでとう！", 'success')
        else:
            console.hud_alert("🔥 素晴らしい！記録しました！", 'success')

    def layout(self):
        """ レイアウトを動的に調整 """
        margin = 10
        label_height = 30
        button_size = 35  # 増減ボタンを少し小さく
        slider_height = 30
        button_width = 100
        vertical_spacing = 15  # 垂直方向の間隔を少し縮小

        if self.is_keyboard:
            scale_factor = 1
        else:
            scale_factor = 1.0

        left_width = self.width * 0.4 * scale_factor
        right_width = self.width * 0.6 * scale_factor

        self.menu_label.frame = (margin, margin, left_width - 2 * margin, label_height)
        self.menu_table.frame = (margin, margin + label_height, left_width - 2 * margin, self.height - 2 * margin - label_height)
        
        # パラメータAの位置を上に移動
        param_x = left_width + margin
        param_a_y = margin
        self.param_a_label.frame = (param_x + (right_width - 2 * margin - self.param_a_slider.width) / 2, param_a_y, self.param_a_slider.width, label_height * 0.8)
        self.param_a_minus_button.frame = (param_x, param_a_y + label_height, button_size * scale_factor, button_size * scale_factor)
        self.param_a_slider.frame = (param_x + button_size * scale_factor + margin, param_a_y + label_height, right_width - 4 * margin - 2 * button_size * scale_factor, slider_height * scale_factor)
        self.param_a_plus_button.frame = (param_x + right_width - 2 * margin - button_size * scale_factor, param_a_y + label_height, button_size * scale_factor, button_size * scale_factor)
        
        # パラメータBの位置も上に移動
        param_b_y = param_a_y + label_height + button_size * scale_factor + margin
        self.param_b_label.frame = (param_x + (right_width - 2 * margin - self.param_b_slider.width) / 2, param_b_y, self.param_b_slider.width, label_height * 0.8)
        self.param_b_minus_button.frame = (param_x, param_b_y + label_height, button_size * scale_factor, button_size * scale_factor)
        self.param_b_slider.frame = (param_x + button_size * scale_factor + margin, param_b_y + label_height, right_width - 4 * margin - 2 * button_size * scale_factor, slider_height * scale_factor)
        self.param_b_plus_button.frame = (param_x + right_width - 2 * margin - button_size * scale_factor, param_b_y + label_height, button_size * scale_factor, button_size * scale_factor)
        
        # 出力ボタンの位置を調整
        output_y = param_b_y + label_height + button_size * scale_factor + vertical_spacing
        output_button_height = button_size * 0.8 * scale_factor
        self.menu_output_button.frame = (param_x, output_y, button_width * scale_factor, output_button_height)
        self.record_output_button.frame = (param_x + button_width * scale_factor + margin, output_y, button_width * scale_factor, output_button_height)

    def tableview_did_select(self, tableview, section, row):
        """ メニューが選択された時の処理 """
        menu_name = self.menu_table.data_source.items[row]
        menu = self.menu_manager.get_menu(menu_name)
        self.param_a_name = menu.param_a.unit
        self.param_b_name = menu.param_b.unit
        self.param_a_step = menu.param_a.step
        self.param_b_step = menu.param_b.step
        self.param_a_max = menu.param_a.max
        self.param_b_max = menu.param_b.max

        last_training = self.history.get_last_training(menu_name)
        if last_training:
            self.param_a_slider.value = self._calculate_slider_value(last_training.get("last_a", 0.0), 0, self.param_a_max)
            self.param_b_slider.value = self._calculate_slider_value(last_training.get("last_b", 0.0), 0, self.param_b_max)
            
            # 最高記録を保存
            self.best_a = last_training.get("best_a", 0.0)
            self.best_b = last_training.get("best_b", 0.0)
        else:
            self.param_a_slider.value = 0.0
            self.param_b_slider.value = 0.0
            self.best_a = 0.0
            self.best_b = 0.0
        
        self._update_parameter_label('a')
        self._update_parameter_label('b')
    
    def update_param_a(self, sender):
        """ スライダーでパラメータAを更新 """
        param_a_value = round(sender.value * self.param_a_max / self.param_a_step) * self.param_a_step
        self.param_a_slider.value = self._calculate_slider_value(param_a_value, 0, self.param_a_max)
        self._update_parameter_label('a')
    
    def increase_param_a(self, sender):
        """ パラメータAを増加 """
        param_a_value = min(self._calculate_parameter_value(self.param_a_slider.value, 0, self.param_a_max, self.param_a_step) + self.param_a_step, self.param_a_max)  # 200を最大値と仮定
        self.param_a_slider.value = self._calculate_slider_value(param_a_value, 0, self.param_a_max)
        self._update_parameter_label('a')
        
    def decrease_param_a(self, sender):
        """ パラメータAを減少 """
        param_a_value = max(self._calculate_parameter_value(self.param_a_slider.value, 0, self.param_a_max, self.param_a_step) - self.param_a_step, 0)  # 0を最小値と仮定
        self.param_a_slider.value = self._calculate_slider_value(param_a_value, 0, self.param_a_max)
        self._update_parameter_label('a')
    
    def update_param_b(self, sender):
        """ スライダーでパラメータBを更新 """
        param_b_value = round(sender.value * self.param_b_max / self.param_b_step) * self.param_b_step
        self.param_b_slider.value = self._calculate_slider_value(param_b_value, 0, self.param_b_max)
        self._update_parameter_label('b')
    
    def increase_param_b(self, sender):
        """ パラメータBを増加 """
        param_b_value = min(self._calculate_parameter_value(self.param_b_slider.value, 0, self.param_b_max, self.param_b_step) + self.param_b_step, self.param_b_max)  # 200を最大値と仮定
        self.param_b_slider.value = self._calculate_slider_value(param_b_value, 0, self.param_b_max)
        self._update_parameter_label('b')
    
    def decrease_param_b(self, sender):
        """ パラメータBを減少 """
        param_b_value = max(self._calculate_parameter_value(self.param_b_slider.value, 0, self.param_b_max, self.param_b_step) - self.param_b_step, 0)  # 0を最小値と仮定
        self.param_b_slider.value = self._calculate_slider_value(param_b_value, 0, self.param_b_max)
        self._update_parameter_label('b')
    
    def output_menu_name(self, sender):
        """ 種目名出力ボタンが押された時の処理 """
        selected_row = self.menu_table.selected_row
        if selected_row is None:
            console.hud_alert("🔍 メニューを選択してください", 'error')
            return
        
        menu_name = self.menu_table.data_source.items[selected_row[1]]
        output_text = f"- {menu_name}\n"
        
        if keyboard.is_keyboard():
            keyboard.insert_text(output_text)
        console.hud_alert("✅ トレーニング種目を設定しました", 'success')

    def output_record(self, sender):
        """ 記録ボタンが押された時の処理 """
        selected_row = self.menu_table.selected_row
        if selected_row is None:
            console.hud_alert("🔍 メニューを選択してください", 'error')
            return
        
        menu_name = self.menu_table.data_source.items[selected_row[1]]
        param_a = self._calculate_parameter_value(self.param_a_slider.value, 0, self.param_a_max, self.param_a_step)
        param_b = self._calculate_parameter_value(self.param_b_slider.value, 0, self.param_b_max, self.param_b_step)
        
        # パラメータが0で、かつステップが0でない場合は記録できない
        if (param_a == 0 and self.param_a_step != 0) or (param_b == 0 and self.param_b_step != 0):
            console.hud_alert("⚠️ パラメータが0の場合は記録できません", 'error')
            return
        
        # 最高記録を更新
        is_record_a = param_a > self.best_a
        is_record_b = param_b > self.best_b
        
        if is_record_a:
            self.best_a = param_a
        if is_record_b:
            self.best_b = param_b
        
        self._handle_record_output(menu_name, param_a, param_b)

    
def main():
    view = TrainingApp()
    if keyboard.is_keyboard():
        keyboard.set_view(view, 'expanded')
        # キーボード表示後にテーブルの一番下を選択してから元に戻す
        # キーボード表示時にテーブルビューの高さが変わるため、一度一番下までスクロールして
        # テーブルの表示範囲を更新する必要がある。その後、選択を元に戻すことで、
        # テーブルビューが正しく表示される。
        if view.menu_table.data_source.items:
            last_row = len(view.menu_table.data_source.items) - 1
            view.menu_table.selected_row = (0, last_row)
            view.tableview_did_select(view.menu_table, 0, last_row)
            # 少し遅延を入れてから元の選択に戻す
            def restore_selection():
                view.menu_table.selected_row = (0, 0)
                view.tableview_did_select(view.menu_table, 0, 0)
            ui.delay(restore_selection, 0.1)
    else:
        view.present("sheet")
if __name__ == "__main__":
    main()
