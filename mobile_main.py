from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from bazi_calculator import generate_fortune_report

# 设置窗口背景颜色
Window.clearcolor = get_color_from_hex('#1a1a1a')

class BaziApp(App):
    def build(self):
        self.title = "八字性格运势分析"
        
        # 主布局
        root = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # 标志与标题
        header = Label(
            text="八字性格运势分析", 
            font_size='28sp', 
            bold=True, 
            size_hint_y=None, 
            height=120,
            color=get_color_from_hex('#ffd700')
        )
        root.add_widget(header)
        
        # 输入表单区域
        form = BoxLayout(orientation='vertical', spacing=12, size_hint_y=None, height=450)
        
        def create_input_row(label_text, widget):
            row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
            row.add_widget(Label(text=label_text, size_hint_x=0.3, halign='right'))
            row.add_widget(widget)
            return row

        self.year_input = TextInput(text='1990', multiline=False, input_filter='int', font_size='18sp')
        self.month_spinner = Spinner(text='1', values=[str(i) for i in range(1, 13)], font_size='18sp')
        self.day_spinner = Spinner(text='1', values=[str(i) for i in range(1, 32)], font_size='18sp')
        self.hour_spinner = Spinner(text='12', values=[str(i) for i in range(24)], font_size='18sp')
        self.gender_spinner = Spinner(text='男', values=['男', '女'], font_size='18sp')

        form.add_widget(create_input_row("年份:", self.year_input))
        form.add_widget(create_input_row("月份:", self.month_spinner))
        form.add_widget(create_input_row("日期:", self.day_spinner))
        form.add_widget(create_input_row("时辰:", self.hour_spinner))
        form.add_widget(create_input_row("性别:", self.gender_spinner))
        
        root.add_widget(form)
        
        # 计算按钮
        calc_btn = Button(
            text="开始精批命局", 
            size_hint_y=None, 
            height=120, 
            background_color=get_color_from_hex('#d4af37'),
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True
        )
        calc_btn.bind(on_release=self.calculate)
        root.add_widget(calc_btn)
        
        # 结果展示区 (滚动)
        result_container = BoxLayout(padding=[0, 20, 0, 0])
        self.scroll = ScrollView(do_scroll_x=False)
        self.result_label = Label(
            text="请输入生辰八字，点击按钮获取分析内容。",
            size_hint_y=None,
            halign='left',
            valign='top',
            markup=True,
            font_size='16sp',
            line_height=1.4
        )
        self.result_label.bind(width=lambda s, w: s.setter('text_size')(s, (w, None)))
        self.result_label.bind(texture_size=lambda s, z: s.setter('height')(s, z[1]))
        self.scroll.add_widget(self.result_label)
        result_container.add_widget(self.scroll)
        root.add_widget(result_container)
        
        return root

    def calculate(self, instance):
        try:
            y = int(self.year_input.text)
            m = int(self.month_spinner.text)
            d = int(self.day_spinner.text)
            h = int(self.hour_spinner.text)
            g = self.gender_spinner.text
            
            report = generate_fortune_report(y, m, d, h, g)
            ana = report['命理分析']
            stages = ana.get('人生命程', {})
            
            # 使用 Kivy 的 Markup 语法美化内容
            res = [
                f"[b][size=22sp][color=ffd700]—— 精批报告 ——[/color][/size][/b]\n",
                f"[b][color=ff8888]● 核心分析[/color][/b]",
                f"【日元属性】: {ana['日元']}命人",
                f"【能量状态】: {ana['日主强弱']}",
                f"【性格精解】: {ana['性格分析']}\n",
                f"[b][color=ffcc66]● 人生命程 (年月日时)[/color][/b]",
                f"[size=14sp]{stages.get('早年(1-16岁)', '')}[/size]",
                f"[size=14sp]{stages.get('青年(17-32岁)', '')}[/size]",
                f"[size=14sp]{stages.get('中年(33-48岁)', '')}[/size]",
                f"[size=14sp]{stages.get('晚年(49岁后)', '')}[/size]\n",
                f"[b][color=88ff88]● 事业展望[/color][/b]",
                f"{ana['事业分析']}\n",
                f"[b][color=8888ff]● 大师建议[/color][/b]",
                f"{report['建议']}\n",
                f"[i][size=14sp](注：命理供参考，努力方能成事)[/size][/i]"
            ]
            
            self.result_label.text = "\n".join(res)
            # 自动滚动到顶部
            self.scroll.scroll_y = 1
        except Exception as e:
            self.result_label.text = f"[color=ff0000]计算出错：{str(e)}[/color]"

if __name__ == '__main__':
    BaziApp().run()
