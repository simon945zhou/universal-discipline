import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QDateEdit, QTimeEdit,
    QGroupBox, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QFileDialog, QSplitter
)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QFont, QIcon, QColor

from knowledge_base import KnowledgeBase
from bazi_calculator import calculate_bazi, analyze_bazi, generate_fortune_report, match_bazi, calculate_10_year_luck
from ziwei_calculator import generate_ziwei_report

class SuanMingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.knowledge_base = KnowledgeBase()
        self.init_ui()
    
    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle('八字性格运势分析系统')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建主标签页
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # 创建各个功能标签页
        self.fortune_tab = self.create_fortune_tab()
        self.compatibility_tab = self.create_compatibility_tab()
        self.knowledge_tab = self.create_knowledge_tab()
        
        # 添加标签页到主窗口
        self.tabs.addTab(self.fortune_tab, '个人算命')
        self.tabs.addTab(self.compatibility_tab, '配对分析')
        self.tabs.addTab(self.knowledge_tab, '知识库管理')
        
        # 显示窗口
        self.show()
    
    def create_fortune_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建输入区域
        input_group = QGroupBox('个人信息输入')
        input_layout = QGridLayout()
        
        # 日期输入
        input_layout.addWidget(QLabel('出生日期:'), 0, 0)
        self.birth_date = QDateEdit()
        self.birth_date.setDate(QDate.currentDate().addYears(-20))  # 默认20年前
        self.birth_date.setCalendarPopup(True)
        input_layout.addWidget(self.birth_date, 0, 1)
        
        # 时间输入
        input_layout.addWidget(QLabel('出生时间:'), 0, 2)
        self.birth_time = QTimeEdit()
        self.birth_time.setTime(QTime(12, 0))  # 默认中午12点
        input_layout.addWidget(self.birth_time, 0, 3)
        
        # 性别选择
        input_layout.addWidget(QLabel('性别:'), 1, 0)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(['男', '女'])
        input_layout.addWidget(self.gender_combo, 1, 1)
        
        # 计算按钮
        self.calculate_btn = QPushButton('开始算命')
        self.calculate_btn.clicked.connect(self.calculate_fortune)
        input_layout.addWidget(self.calculate_btn, 1, 2, 1, 2)
        
        input_group.setLayout(input_layout)
        
        # 创建结果显示区域
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("background-color: #f0f0f0;")
        
        # 添加到主布局
        layout.addWidget(input_group)
        layout.addWidget(self.result_text)
        
        return tab
    
    def create_compatibility_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        
        # 男性信息输入
        male_group = QGroupBox('男性出生信息')
        male_group.setStyleSheet("background-color: #e6f2ff;")
        male_layout = QGridLayout()
        
        male_layout.addWidget(QLabel('性别:'), 0, 0)
        self.male_gender = QComboBox()
        self.male_gender.addItems(['男'])
        self.male_gender.setCurrentText('男')
        self.male_gender.setEnabled(False)
        male_layout.addWidget(self.male_gender, 0, 1)
        
        male_layout.addWidget(QLabel('出生年份:'), 1, 0)
        self.male_year = QComboBox()
        for year in range(1920, datetime.now().year + 1):
            self.male_year.addItem(str(year))
        self.male_year.setCurrentText('1980')
        male_layout.addWidget(self.male_year, 1, 1)
        
        male_layout.addWidget(QLabel('出生月份:'), 2, 0)
        self.male_month = QComboBox()
        for month in range(1, 13):
            self.male_month.addItem(str(month))
        self.male_month.setCurrentText('2')
        male_layout.addWidget(self.male_month, 2, 1)
        
        male_layout.addWidget(QLabel('出生日期:'), 3, 0)
        self.male_day = QComboBox()
        for day in range(1, 32):
            self.male_day.addItem(str(day))
        self.male_day.setCurrentText('1')
        male_layout.addWidget(self.male_day, 3, 1)
        
        male_layout.addWidget(QLabel('出生时间:'), 4, 0)
        self.male_time = QComboBox()
        time_options = ['子时(23:00-01:00)', '丑时(01:00-03:00)', '寅时(03:00-05:00)', 
                        '卯时(05:00-07:00)', '辰时(07:00-09:00)', '巳时(09:00-11:00)',
                        '午时(11:00-13:00)', '未时(13:00-15:00)', '申时(15:00-17:00)',
                        '酉时(17:00-19:00)', '戌时(19:00-21:00)', '亥时(21:00-23:00)']
        self.male_time.addItems(time_options)
        self.male_time.setCurrentText('子时(23:00-01:00)')
        male_layout.addWidget(self.male_time, 4, 1)
        
        male_group.setLayout(male_layout)
        
        # 女性信息输入
        female_group = QGroupBox('女性出生信息')
        female_group.setStyleSheet("background-color: #ffe6f2;")
        female_layout = QGridLayout()
        
        female_layout.addWidget(QLabel('性别:'), 0, 0)
        self.female_gender = QComboBox()
        self.female_gender.addItems(['女'])
        self.female_gender.setCurrentText('女')
        self.female_gender.setEnabled(False)
        female_layout.addWidget(self.female_gender, 0, 1)
        
        female_layout.addWidget(QLabel('出生年份:'), 1, 0)
        self.female_year = QComboBox()
        for year in range(1920, datetime.now().year + 1):
            self.female_year.addItem(str(year))
        self.female_year.setCurrentText('1982')
        female_layout.addWidget(self.female_year, 1, 1)
        
        female_layout.addWidget(QLabel('出生月份:'), 2, 0)
        self.female_month = QComboBox()
        for month in range(1, 13):
            self.female_month.addItem(str(month))
        self.female_month.setCurrentText('5')
        female_layout.addWidget(self.female_month, 2, 1)
        
        female_layout.addWidget(QLabel('出生日期:'), 3, 0)
        self.female_day = QComboBox()
        for day in range(1, 32):
            self.female_day.addItem(str(day))
        self.female_day.setCurrentText('15')
        female_layout.addWidget(self.female_day, 3, 1)
        
        female_layout.addWidget(QLabel('出生时间:'), 4, 0)
        self.female_time = QComboBox()
        self.female_time.addItems(time_options)
        self.female_time.setCurrentText('巳时(09:00-11:00)')
        female_layout.addWidget(self.female_time, 4, 1)
        
        female_group.setLayout(female_layout)
        
        input_layout.addWidget(male_group)
        input_layout.addWidget(female_group)
        
        # 创建结果显示区域
        result_layout = QHBoxLayout()
        
        self.male_analysis_text = QTextEdit()
        self.male_analysis_text.setReadOnly(True)
        self.male_analysis_text.setStyleSheet("background-color: #f0f0f0;")
        self.male_analysis_text.setPlaceholderText("男性命盘分析结果将显示在这里...")
        
        self.compatibility_text = QTextEdit()
        self.compatibility_text.setReadOnly(True)
        self.compatibility_text.setStyleSheet("background-color: #f0f0f0;")
        self.compatibility_text.setPlaceholderText("男女配对分析结果将显示在这里...")
        
        self.female_analysis_text = QTextEdit()
        self.female_analysis_text.setReadOnly(True)
        self.female_analysis_text.setStyleSheet("background-color: #f0f0f0;")
        self.female_analysis_text.setPlaceholderText("女性命盘分析结果将显示在这里...")
        
        result_layout.addWidget(self.male_analysis_text)
        result_layout.addWidget(self.compatibility_text)
        result_layout.addWidget(self.female_analysis_text)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        
        self.male_fortune_btn = QPushButton('男性算命')
        self.male_fortune_btn.clicked.connect(self.calculate_male_fortune)
        
        self.male_solution_btn = QPushButton('男性化解建议')
        self.male_solution_btn.clicked.connect(self.generate_male_solution)
        
        self.couple_analysis_btn = QPushButton('男女配对分析')
        self.couple_analysis_btn.clicked.connect(self.analyze_couple_compatibility)
        
        self.couple_solution_btn = QPushButton('配对化解建议')
        self.couple_solution_btn.clicked.connect(self.generate_couple_solution)
        
        self.female_fortune_btn = QPushButton('女性算命')
        self.female_fortune_btn.clicked.connect(self.calculate_female_fortune)
        
        self.female_solution_btn = QPushButton('女性化解建议')
        self.female_solution_btn.clicked.connect(self.generate_female_solution)
        
        button_layout.addWidget(self.male_fortune_btn)
        button_layout.addWidget(self.male_solution_btn)
        button_layout.addWidget(self.couple_analysis_btn)
        button_layout.addWidget(self.couple_solution_btn)
        button_layout.addWidget(self.female_fortune_btn)
        button_layout.addWidget(self.female_solution_btn)
        
        # 添加到主布局
        layout.addLayout(input_layout)
        layout.addLayout(result_layout)
        layout.addLayout(button_layout)
        
        return tab
    
    def create_knowledge_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建操作按钮区域
        btn_layout = QHBoxLayout()
        
        self.add_knowledge_btn = QPushButton('添加知识')
        self.add_knowledge_btn.clicked.connect(self.add_knowledge_dialog)
        
        self.delete_knowledge_btn = QPushButton('删除知识')
        self.delete_knowledge_btn.clicked.connect(self.delete_knowledge)
        
        self.refresh_knowledge_btn = QPushButton('刷新列表')
        self.refresh_knowledge_btn.clicked.connect(self.refresh_knowledge_table)
        
        btn_layout.addWidget(self.add_knowledge_btn)
        btn_layout.addWidget(self.delete_knowledge_btn)
        btn_layout.addWidget(self.refresh_knowledge_btn)
        
        # 创建分类选择
        cat_layout = QHBoxLayout()
        cat_layout.addWidget(QLabel('选择分类:'))
        self.category_combo = QComboBox()
        self.category_combo.addItem('所有分类')
        self.category_combo.addItems(self.knowledge_base.get_all_categories())
        self.category_combo.currentIndexChanged.connect(self.refresh_knowledge_table)
        cat_layout.addWidget(self.category_combo)
        
        # 创建知识列表表格
        self.knowledge_table = QTableWidget()
        self.knowledge_table.setColumnCount(2)
        self.knowledge_table.setHorizontalHeaderLabels(['文件名', '上传时间'])
        self.knowledge_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.knowledge_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # 创建知识详情显示
        self.knowledge_detail = QTextEdit()
        self.knowledge_detail.setReadOnly(True)
        self.knowledge_detail.setStyleSheet("background-color: #f0f0f0;")
        
        # 连接表格选择事件
        self.knowledge_table.cellClicked.connect(self.show_knowledge_detail)
        
        # 添加到主布局
        layout.addLayout(btn_layout)
        layout.addLayout(cat_layout)
        layout.addWidget(self.knowledge_table)
        layout.addWidget(QLabel('知识详情:'))
        layout.addWidget(self.knowledge_detail)
        
        # 刷新知识表格
        self.refresh_knowledge_table()
        
        return tab
    
    def calculate_fortune(self):
        # 获取输入数据
        birth_date = self.birth_date.date()
        birth_time = self.birth_time.time()
        gender = self.gender_combo.currentText()
        
        # 提取年月日时
        year = birth_date.year()
        month = birth_date.month()
        day = birth_date.day()
        hour = birth_time.hour()
        
        try:
            # 生成命理报告
            report = generate_fortune_report(year, month, day, hour, gender)
            
            # 获取八字信息进行五行分析
            bazi_info = calculate_bazi(year, month, day, hour, gender)
            bazi_analysis = analyze_bazi(bazi_info)
            
            # 生成紫微斗数分析报告
            ziwei_report = generate_ziwei_report(year, month, day, hour, gender)
            
            # 格式化结果显示
            result_text = "个人命理分析报告\n"
            result_text += "=" * 50 + "\n"
            
            # 基本信息
            result_text += "【基本信息】\n"
            for key, value in report['基本信息'].items():
                result_text += f"{key}: {value}\n"
            result_text += "\n"
            
            # 八字五行分析
            result_text += "【八字五行分析】\n"
            result_text += f"日元: {bazi_analysis['日元']}\n"
            result_text += f"日元五行: {bazi_analysis['日元五行']}\n"
            result_text += "五行分布: "
            for elem, count in bazi_analysis['五行分布'].items():
                result_text += f"{elem}: {count}个, "
            result_text = result_text.rstrip(', ') + "\n"
            result_text += f"强弱势分析: {bazi_analysis['强弱势分析']}\n"
            result_text += f"性格分析: {bazi_analysis['性格分析']}\n"
            result_text += f"事业分析: {bazi_analysis['事业分析']}\n"
            result_text += f"运势概要: {bazi_analysis['运势概要']}\n"
            result_text += "\n"
            
            # 紫微斗数分析
            result_text += ziwei_report + "\n"
            
            # 命理建议
            result_text += "【综合建议】\n"
            result_text += f"{report['建议']}\n"
            
            # 显示结果
            self.result_text.setPlainText(result_text)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'计算过程中出现错误: {str(e)}')
    
    def analyze_compatibility(self):
        # 这个方法保持兼容原有功能，实际使用的是新的analyze_couple_compatibility方法
        pass
    
    def calculate_male_fortune(self):
        # 获取男性信息
        try:
            year = int(self.male_year.currentText())
            month = int(self.male_month.currentText())
            day = int(self.male_day.currentText())
            time_text = self.male_time.currentText()
            
            # 从时辰文本中提取对应的小时
            hour_map = {
                '子时': 0, '丑时': 2, '寅时': 4, '卯时': 6, 
                '辰时': 8, '巳时': 10, '午时': 12, '未时': 14, 
                '申时': 16, '酉时': 18, '戌时': 20, '亥时': 22
            }
            for key in hour_map:
                if key in time_text:
                    hour = hour_map[key]
                    break
            
            # 生成八字命理报告
            bazi_info = calculate_bazi(year, month, day, hour, '男')
            bazi_analysis = analyze_bazi(bazi_info)
            
            # 计算10年大运
            luck_periods = calculate_10_year_luck(bazi_info)
            
            # 生成紫微斗数报告
            ziwei_report = generate_ziwei_report(year, month, day, hour, '男')
            
            # 格式化结果显示
            result_text = "男性命理分析报告\n"
            result_text += "=" * 50 + "\n"
            
            # 基本信息
            result_text += "【基本信息】\n"
            result_text += f"出生日期: {year}年{month}月{day}日{hour}时\n"
            result_text += f"性别: 男\n"
            result_text += f"八字: {bazi_info['four_pillars']}\n\n"
            
            # 八字五行分析
            result_text += "【八字五行分析】\n"
            result_text += f"日元: {bazi_analysis['日元']}\n"
            result_text += f"日元五行: {bazi_analysis['日元五行']}\n"
            result_text += "五行分布: "
            for element, count in bazi_analysis['五行分布'].items():
                result_text += f"{element}{count} "
            result_text += "\n"
            result_text += f"强弱势分析: {bazi_analysis['强弱势分析']}\n"
            result_text += f"性格分析: {bazi_analysis['性格分析']}\n"
            result_text += f"运势概要: {bazi_analysis['运势概要']}\n"
            result_text += f"事业分析: {bazi_analysis['事业分析']}\n\n"
            
            # 紫微斗数分析
            result_text += "【紫微斗数分析】\n"
            result_text += f"命宫位置: {ziwei_report['命宫位置']}\n"
            result_text += f"命宫主星: {'、'.join(ziwei_report['命宫主星']) if ziwei_report['命宫主星'] else '无主星'}\n"
            result_text += f"身宫位置: {ziwei_report['身宫位置']}\n"
            result_text += f"总体评断: {ziwei_report['总体评断']}\n"
            result_text += "\n"
            
            # 添加10年大运分析
            result_text += "【10年大运分析】\n"
            for i, period in enumerate(luck_periods):
                result_text += f"第{i+1}步大运: {period['大运']}\n"
                result_text += f"年龄范围: {period['年龄']}\n"
                result_text += f"运势简析: {period['简析']}\n"
                result_text += "-" * 40 + "\n"
            
            # 显示结果
            self.male_analysis_text.setPlainText(result_text)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'计算过程中出现错误: {str(e)}')
    
    def calculate_female_fortune(self):
        # 获取女性信息
        try:
            year = int(self.female_year.currentText())
            month = int(self.female_month.currentText())
            day = int(self.female_day.currentText())
            time_text = self.female_time.currentText()
            
            # 从时辰文本中提取对应的小时
            hour_map = {
                '子时': 0, '丑时': 2, '寅时': 4, '卯时': 6, 
                '辰时': 8, '巳时': 10, '午时': 12, '未时': 14, 
                '申时': 16, '酉时': 18, '戌时': 20, '亥时': 22
            }
            for key in hour_map:
                if key in time_text:
                    hour = hour_map[key]
                    break
            
            # 生成八字命理报告
            bazi_info = calculate_bazi(year, month, day, hour, '女')
            bazi_analysis = analyze_bazi(bazi_info)
            
            # 计算10年大运
            luck_periods = calculate_10_year_luck(bazi_info)
            
            # 生成紫微斗数报告
            ziwei_report = generate_ziwei_report(year, month, day, hour, '女')
            
            # 格式化结果显示
            result_text = "女性命理分析报告\n"
            result_text += "=" * 50 + "\n"
            
            # 基本信息
            result_text += "【基本信息】\n"
            result_text += f"出生日期: {year}年{month}月{day}日{hour}时\n"
            result_text += f"性别: 女\n"
            result_text += f"八字: {bazi_info['four_pillars']}\n\n"
            
            # 八字五行分析
            result_text += "【八字五行分析】\n"
            result_text += f"日元: {bazi_analysis['日元']}\n"
            result_text += f"日元五行: {bazi_analysis['日元五行']}\n"
            result_text += "五行分布: "
            for element, count in bazi_analysis['五行分布'].items():
                result_text += f"{element}{count} "
            result_text += "\n"
            result_text += f"强弱势分析: {bazi_analysis['强弱势分析']}\n"
            result_text += f"性格分析: {bazi_analysis['性格分析']}\n"
            result_text += f"运势概要: {bazi_analysis['运势概要']}\n"
            result_text += f"事业分析: {bazi_analysis['事业分析']}\n\n"
            
            # 紫微斗数分析
            result_text += "【紫微斗数分析】\n"
            result_text += f"命宫位置: {ziwei_report['命宫位置']}\n"
            result_text += f"命宫主星: {'、'.join(ziwei_report['命宫主星']) if ziwei_report['命宫主星'] else '无主星'}\n"
            result_text += f"身宫位置: {ziwei_report['身宫位置']}\n"
            result_text += f"总体评断: {ziwei_report['总体评断']}\n"
            result_text += "\n"
            
            # 添加10年大运分析
            result_text += "【10年大运分析】\n"
            for i, period in enumerate(luck_periods):
                result_text += f"第{i+1}步大运: {period['大运']}\n"
                result_text += f"年龄范围: {period['年龄']}\n"
                result_text += f"运势简析: {period['简析']}\n"
                result_text += "-" * 40 + "\n"
            
            # 显示结果
            self.female_analysis_text.setPlainText(result_text)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'计算过程中出现错误: {str(e)}')
    
    def analyze_couple_compatibility(self):
        # 获取男性信息
        try:
            male_year = int(self.male_year.currentText())
            male_month = int(self.male_month.currentText())
            male_day = int(self.male_day.currentText())
            male_time_text = self.male_time.currentText()
            
            # 获取女性信息
            female_year = int(self.female_year.currentText())
            female_month = int(self.female_month.currentText())
            female_day = int(self.female_day.currentText())
            female_time_text = self.female_time.currentText()
            
            # 从时辰文本中提取对应的小时
            hour_map = {
                '子时': 0, '丑时': 2, '寅时': 4, '卯时': 6, 
                '辰时': 8, '巳时': 10, '午时': 12, '未时': 14, 
                '申时': 16, '酉时': 18, '戌时': 20, '亥时': 22
            }
            
            for key in hour_map:
                if key in male_time_text:
                    male_hour = hour_map[key]
                    break
            
            for key in hour_map:
                if key in female_time_text:
                    female_hour = hour_map[key]
                    break
            
            # 计算两人八字
            male_bazi = calculate_bazi(male_year, male_month, male_day, male_hour, '男')
            female_bazi = calculate_bazi(female_year, female_month, female_day, female_hour, '女')
            
            # 计算双方10年大运
            male_luck_periods = calculate_10_year_luck(male_bazi)
            female_luck_periods = calculate_10_year_luck(female_bazi)
            
            # 计算配对结果
            compatibility = calculate_compatibility(male_bazi, female_bazi)
            
            # 计算双方八字五行分析
            male_bazi_analysis = analyze_bazi(male_bazi)
            female_bazi_analysis = analyze_bazi(female_bazi)
            
            # 生成紫微斗数报告
            male_ziwei = generate_ziwei_report(male_year, male_month, male_day, male_hour, '男')
            female_ziwei = generate_ziwei_report(female_year, female_month, female_day, female_hour, '女')
            
            # 格式化结果显示
            result_text = "男女配对分析报告\n"
            result_text += "=" * 50 + "\n"
            
            # 双方信息
            result_text += "【双方信息】\n"
            result_text += f"男性: {male_year}年{male_month}月{male_day}日{male_time_text}\n"
            result_text += f"八字: {male_bazi['four_pillars']}\n"
            result_text += f"日元: {male_bazi_analysis['日元']}({male_bazi_analysis['日元五行']})\n\n"
            result_text += f"女性: {female_year}年{female_month}月{female_day}日{female_time_text}\n"
            result_text += f"八字: {female_bazi['four_pillars']}\n"
            result_text += f"日元: {female_bazi_analysis['日元']}({female_bazi_analysis['日元五行']})\n\n"
            
            # 八字配对分析
            result_text += "【八字配对分析】\n"
            for key, value in compatibility.items():
                result_text += f"{key}: {value}\n"            
            result_text += "\n"
            
            # 紫微斗数配对分析
            result_text += "【紫微斗数配对分析】\n"
            result_text += f"男方命宫主星: {'、'.join(male_ziwei['命宫主星']) if male_ziwei['命宫主星'] else '无主星'}\n"
            result_text += f"女方命宫主星: {'、'.join(female_ziwei['命宫主星']) if female_ziwei['命宫主星'] else '无主星'}\n"
            
            # 根据主星关系给出分析
            male_main_star = male_ziwei.get('命宫主星', '')
            female_main_star = female_ziwei.get('命宫主星', '')
            
            if '紫微' in male_main_star and '天府' in female_main_star:
                result_text += "主星配对评价: 紫微天府，帝王搭配，相辅相成，贵气十足。\n"
            elif '贪狼' in male_main_star and '七杀' in female_main_star:
                result_text += "主星配对评价: 贪狼七杀，个性强烈，需要相互包容理解。\n"
            elif '天机' in male_main_star and '太阴' in female_main_star:
                result_text += "主星配对评价: 天机太阴，聪明睿智，情感细腻，心灵相通。\n"
            else:
                result_text += "主星配对评价: 两人主星各具特色，需要相互欣赏对方的优点。\n"
            
            # 添加双方大运分析
            result_text += "【双方大运分析】\n"
            result_text += "男方大运:\n"
            for i, period in enumerate(male_luck_periods):
                result_text += f"第{i+1}步大运: {period['大运']}\n"
                result_text += f"年龄范围: {period['年龄']}\n"
                result_text += f"运势简析: {period['简析'][:20]}...\n"
                result_text += "-" * 20 + "\n"
            
            result_text += "\n女方大运:\n"
            for i, period in enumerate(female_luck_periods):
                result_text += f"第{i+1}步大运: {period['大运']}\n"
                result_text += f"年龄范围: {period['年龄']}\n"
                result_text += f"运势简析: {period['简析'][:20]}...\n"
                result_text += "-" * 20 + "\n"
            
            # 大运配对建议
            result_text += "\n【大运配对建议】\n"
            # 这里是简化的大运配对建议逻辑
            # 在实际应用中，可以根据双方大运的五行生克关系给出更详细的建议
            result_text += "根据双方大运走势，建议关注以下几点：\n"
            result_text += "1. 在对方大运波动较大的时期，给予更多理解和支持\n"
            result_text += "2. 利用双方大运互补的阶段，共同规划重要人生决策\n"
            result_text += "3. 注意双方大运可能产生冲突的时期，保持沟通和包容\n"
            
            # 显示结果
            self.compatibility_text.setPlainText(result_text)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'分析过程中出现错误: {str(e)}')
    
    def generate_male_solution(self):
        # 获取男性信息
        try:
            year = int(self.male_year.currentText())
            month = int(self.male_month.currentText())
            day = int(self.male_day.currentText())
            time_text = self.male_time.currentText()
            
            # 从时辰文本中提取对应的小时
            hour_map = {
                '子时': 0, '丑时': 2, '寅时': 4, '卯时': 6, 
                '辰时': 8, '巳时': 10, '午时': 12, '未时': 14, 
                '申时': 16, '酉时': 18, '戌时': 20, '亥时': 22
            }
            for key in hour_map:
                if key in time_text:
                    hour = hour_map[key]
                    break
            
            # 计算八字
            bazi = calculate_bazi(year, month, day, hour, '男')
            
            # 计算八字命理分析
            bazi_analysis = analyze_bazi(bazi)
            
            # 生成紫微斗数报告
            ziwei_report = generate_ziwei_report(year, month, day, hour, '男')
            
            # 生成化解建议
            solution_text = "男性命理化解建议\n"
            solution_text += "=" * 50 + "\n\n"
            
            # 八字五行要点
            solution_text += "【八字五行要点】\n"
            solution_text += f"日元: {bazi_analysis['日元']}({bazi_analysis['日元五行']})\n"
            solution_text += "五行分布: "
            for element, count in bazi_analysis['五行分布'].items():
                solution_text += f"{element}{count} "
            solution_text += "\n"
            solution_text += f"强弱势分析: {bazi_analysis['强弱势分析']}\n\n"
            
            # 紫微斗数要点
            solution_text += "【紫微斗数要点】\n"
            solution_text += f"命宫位置: {ziwei_report['命宫位置']}\n"
            solution_text += f"命宫主星: {'、'.join(ziwei_report['命宫主星']) if ziwei_report['命宫主星'] else '无主星'}\n"
            solution_text += f"身宫位置: {ziwei_report['身宫位置']}\n\n"
            
            # 针对性化解建议
            solution_text += "【五行化解建议】\n"
            
            # 根据五行强弱给出具体建议
            strong_element = max(bazi_analysis['五行分布'].items(), key=lambda x: x[1])[0]
            weak_element = min(bazi_analysis['五行分布'].items(), key=lambda x: x[1])[0]
            
            solution_text += f"1. 您的八字中{strong_element}元素较强，建议适当平衡，可通过以下方式：\n"
            if strong_element == '木':
                solution_text += "   - 穿着上可多选择白色、金色系衣物（金克木）\n"
                solution_text += "   - 居住环境中可增加金属类装饰物品\n"
            elif strong_element == '火':
                solution_text += "   - 穿着上可多选择黑色、蓝色系衣物（水克火）\n"
                solution_text += "   - 居住环境中可增加水元素装饰\n"
            elif strong_element == '土':
                solution_text += "   - 穿着上可多选择绿色、青色系衣物（木克土）\n"
                solution_text += "   - 居住环境中可增加植物\n"
            elif strong_element == '金':
                solution_text += "   - 穿着上可多选择红色、紫色系衣物（火克金）\n"
                solution_text += "   - 居住环境中可增加暖色调装饰\n"
            elif strong_element == '水':
                solution_text += "   - 穿着上可多选择黄色、棕色系衣物（土克水）\n"
                solution_text += "   - 居住环境中可增加陶瓷、石材装饰\n"
            
            solution_text += f"2. 您的八字中{weak_element}元素较弱，建议适当补充：\n"
            if weak_element == '木':
                solution_text += "   - 穿着上可多选择绿色、青色系衣物\n"
                solution_text += "   - 多接触大自然，种植绿色植物\n"
            elif weak_element == '火':
                solution_text += "   - 穿着上可多选择红色、紫色系衣物\n"
                solution_text += "   - 适当增加室内光线，使用暖色灯光\n"
            elif weak_element == '土':
                solution_text += "   - 穿着上可多选择黄色、棕色系衣物\n"
                solution_text += "   - 可佩戴玉石、玛瑙等土属性饰品\n"
            elif weak_element == '金':
                solution_text += "   - 穿着上可多选择白色、金色系衣物\n"
                solution_text += "   - 可佩戴金银饰品增强金气\n"
            elif weak_element == '水':
                solution_text += "   - 穿着上可多选择黑色、蓝色系衣物\n"
                solution_text += "   - 可在家中放置鱼缸或水培植物\n"
            
            solution_text += "\n【紫微斗数化解建议】\n"
            # 根据紫微斗数给出建议
            life_palace_stars = ziwei_report.get('命宫主星', '')
            if '紫微' in life_palace_stars:
                solution_text += "1. 紫微坐命者，宜保持谦逊，避免过于自我，多倾听他人意见。\n"
            elif '贪狼' in life_palace_stars:
                solution_text += "1. 贪狼坐命者，宜控制欲望，专注于目标，避免三心二意。\n"
            elif '七杀' in life_palace_stars:
                solution_text += "1. 七杀坐命者，宜培养耐心，避免冲动行事，学会冷静思考。\n"
            elif '破军' in life_palace_stars:
                solution_text += "1. 破军坐命者，宜稳定情绪，避免变化过大，培养持之以恒的精神。\n"
            elif '廉贞' in life_palace_stars:
                solution_text += "1. 廉贞坐命者，宜保持正直，避免虚荣，培养务实作风。\n"
            elif '天府' in life_palace_stars:
                solution_text += "1. 天府坐命者，宜发挥领导才能，同时保持节俭，避免铺张浪费。\n"
            else:
                solution_text += "1. 根据您的命宫主星特点，建议保持积极心态，发挥自身优势。\n"
            
            solution_text += "2. 定期关注自己的运势变化，在不利年份采取保守策略。\n"
            solution_text += "3. 保持良好的心态和健康的生活习惯，是最根本的化解方法。\n"
            
            # 显示结果
            self.male_analysis_text.setPlainText(solution_text)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成建议过程中出现错误: {str(e)}')
    
    def generate_female_solution(self):
        # 获取女性信息
        try:
            year = int(self.female_year.currentText())
            month = int(self.female_month.currentText())
            day = int(self.female_day.currentText())
            time_text = self.female_time.currentText()
            
            # 从时辰文本中提取对应的小时
            hour_map = {
                '子时': 0, '丑时': 2, '寅时': 4, '卯时': 6, 
                '辰时': 8, '巳时': 10, '午时': 12, '未时': 14, 
                '申时': 16, '酉时': 18, '戌时': 20, '亥时': 22
            }
            for key in hour_map:
                if key in time_text:
                    hour = hour_map[key]
                    break
            
            # 计算八字
            bazi = calculate_bazi(year, month, day, hour, '女')
            
            # 计算八字命理分析
            bazi_analysis = analyze_bazi(bazi)
            
            # 生成紫微斗数报告
            ziwei_report = generate_ziwei_report(year, month, day, hour, '女')
            
            # 生成化解建议
            solution_text = "女性命理化解建议\n"
            solution_text += "=" * 50 + "\n\n"
            
            # 八字五行要点
            solution_text += "【八字五行要点】\n"
            solution_text += f"日元: {bazi_analysis['日元']}({bazi_analysis['日元五行']})\n"
            solution_text += "五行分布: "
            for element, count in bazi_analysis['五行分布'].items():
                solution_text += f"{element}{count} "
            solution_text += "\n"
            solution_text += f"强弱势分析: {bazi_analysis['强弱势分析']}\n\n"
            
            # 紫微斗数要点
            solution_text += "【紫微斗数要点】\n"
            solution_text += f"命宫位置: {ziwei_report['命宫位置']}\n"
            solution_text += f"命宫主星: {'、'.join(ziwei_report['命宫主星']) if ziwei_report['命宫主星'] else '无主星'}\n"
            solution_text += f"身宫位置: {ziwei_report['身宫位置']}\n\n"
            
            # 针对性化解建议
            solution_text += "【五行化解建议】\n"
            
            # 根据五行强弱给出具体建议
            strong_element = max(bazi_analysis['五行分布'].items(), key=lambda x: x[1])[0]
            weak_element = min(bazi_analysis['五行分布'].items(), key=lambda x: x[1])[0]
            
            solution_text += f"1. 您的八字中{strong_element}元素较强，建议适当平衡，可通过以下方式：\n"
            if strong_element == '木':
                solution_text += "   - 穿着上可多选择白色、金色系衣物（金克木）\n"
                solution_text += "   - 居住环境中可增加金属类装饰物品\n"
            elif strong_element == '火':
                solution_text += "   - 穿着上可多选择黑色、蓝色系衣物（水克火）\n"
                solution_text += "   - 居住环境中可增加水元素装饰\n"
            elif strong_element == '土':
                solution_text += "   - 穿着上可多选择绿色、青色系衣物（木克土）\n"
                solution_text += "   - 居住环境中可增加植物\n"
            elif strong_element == '金':
                solution_text += "   - 穿着上可多选择红色、紫色系衣物（火克金）\n"
                solution_text += "   - 居住环境中可增加暖色调装饰\n"
            elif strong_element == '水':
                solution_text += "   - 穿着上可多选择黄色、棕色系衣物（土克水）\n"
                solution_text += "   - 居住环境中可增加陶瓷、石材装饰\n"
            
            solution_text += f"2. 您的八字中{weak_element}元素较弱，建议适当补充：\n"
            if weak_element == '木':
                solution_text += "   - 穿着上可多选择绿色、青色系衣物\n"
                solution_text += "   - 多接触大自然，种植绿色植物\n"
            elif weak_element == '火':
                solution_text += "   - 穿着上可多选择红色、紫色系衣物\n"
                solution_text += "   - 适当增加室内光线，使用暖色灯光\n"
            elif weak_element == '土':
                solution_text += "   - 穿着上可多选择黄色、棕色系衣物\n"
                solution_text += "   - 可佩戴玉石、玛瑙等土属性饰品\n"
            elif weak_element == '金':
                solution_text += "   - 穿着上可多选择白色、金色系衣物\n"
                solution_text += "   - 可佩戴金银饰品增强金气\n"
            elif weak_element == '水':
                solution_text += "   - 穿着上可多选择黑色、蓝色系衣物\n"
                solution_text += "   - 可在家中放置鱼缸或水培植物\n"
            
            solution_text += "\n【紫微斗数化解建议】\n"
            # 根据紫微斗数给出建议
            life_palace_stars = ziwei_report.get('命宫主星', '')
            if '紫微' in life_palace_stars:
                solution_text += "1. 紫微坐命者，宜保持谦逊，避免过于自我，多倾听他人意见。\n"
            elif '贪狼' in life_palace_stars:
                solution_text += "1. 贪狼坐命者，宜控制欲望，专注于目标，避免三心二意。\n"
            elif '七杀' in life_palace_stars:
                solution_text += "1. 七杀坐命者，宜培养耐心，避免冲动行事，学会冷静思考。\n"
            elif '破军' in life_palace_stars:
                solution_text += "1. 破军坐命者，宜稳定情绪，避免变化过大，培养持之以恒的精神。\n"
            elif '廉贞' in life_palace_stars:
                solution_text += "1. 廉贞坐命者，宜保持正直，避免虚荣，培养务实作风。\n"
            elif '天府' in life_palace_stars:
                solution_text += "1. 天府坐命者，宜发挥领导才能，同时保持节俭，避免铺张浪费。\n"
            elif '太阴' in life_palace_stars:
                solution_text += "1. 太阴坐命者，宜保持乐观，避免多愁善感，培养积极心态。\n"
            elif '天同' in life_palace_stars:
                solution_text += "1. 天同坐命者，宜积极进取，避免懒散，培养上进心。\n"
            else:
                solution_text += "1. 根据您的命宫主星特点，建议保持积极心态，发挥自身优势。\n"
            
            solution_text += "2. 定期关注自己的运势变化，在不利年份采取保守策略。\n"
            solution_text += "3. 保持良好的心态和健康的生活习惯，是最根本的化解方法。\n"
            
            # 显示结果
            self.female_analysis_text.setPlainText(solution_text)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成建议过程中出现错误: {str(e)}')
    
    def generate_couple_solution(self):
        # 获取男性信息
        try:
            male_year = int(self.male_year.currentText())
            male_month = int(self.male_month.currentText())
            male_day = int(self.male_day.currentText())
            male_time_text = self.male_time.currentText()
            
            # 获取女性信息
            female_year = int(self.female_year.currentText())
            female_month = int(self.female_month.currentText())
            female_day = int(self.female_day.currentText())
            female_time_text = self.female_time.currentText()
            
            # 从时辰文本中提取对应的小时
            hour_map = {
                '子时': 0, '丑时': 2, '寅时': 4, '卯时': 6, 
                '辰时': 8, '巳时': 10, '午时': 12, '未时': 14, 
                '申时': 16, '酉时': 18, '戌时': 20, '亥时': 22
            }
            
            for key in hour_map:
                if key in male_time_text:
                    male_hour = hour_map[key]
                    break
            
            for key in hour_map:
                if key in female_time_text:
                    female_hour = hour_map[key]
                    break
            
            # 计算两人八字
            male_bazi = calculate_bazi(male_year, male_month, male_day, male_hour, '男')
            female_bazi = calculate_bazi(female_year, female_month, female_day, female_hour, '女')
            
            # 计算配对结果
            compatibility = calculate_compatibility(male_bazi, female_bazi)
            
            # 计算双方八字五行分析
            male_bazi_analysis = analyze_bazi(male_bazi)
            female_bazi_analysis = analyze_bazi(female_bazi)
            
            # 生成紫微斗数报告
            male_ziwei = generate_ziwei_report(male_year, male_month, male_day, male_hour, '男')
            female_ziwei = generate_ziwei_report(female_year, female_month, female_day, female_hour, '女')
            
            # 生成配对化解建议
            solution_text = "配对关系化解建议\n"
            solution_text += "=" * 50 + "\n\n"
            
            # 配对要点
            solution_text += "【配对要点】\n"
            solution_text += f"配对指数: {compatibility.get('配对指数', '未知')}\n"
            solution_text += f"八字合婚关系: {compatibility.get('合婚关系', '未知')}\n"
            solution_text += f"男方日元: {male_bazi_analysis['日元']}({male_bazi_analysis['日元五行']})\n"
            solution_text += f"女方日元: {female_bazi_analysis['日元']}({female_bazi_analysis['日元五行']})\n"
            solution_text += f"男方命宫主星: {'、'.join(male_ziwei['命宫主星']) if male_ziwei['命宫主星'] else '无主星'}\n"
            solution_text += f"女方命宫主星: {'、'.join(female_ziwei['命宫主星']) if female_ziwei['命宫主星'] else '无主星'}\n"

            # 八字五行化解建议
            solution_text += "【八字五行化解建议】\n"
            
            # 根据五行关系给出建议
            element_relation = compatibility.get('合婚关系', '')
            if element_relation in ['相生', '被相生']:
                solution_text += "1. 两人五行相生，关系融洽，建议：\n"
                solution_text += "   - 保持现有的相处模式，相互支持鼓励\n"
                solution_text += "   - 在重要决策时，多听取对方意见\n"
            elif element_relation in ['相克', '被相克']:
                solution_text += "1. 两人五行相克，需要注意：\n"
                solution_text += "   - 在沟通中保持耐心，避免正面冲突\n"
                solution_text += "   - 可通过中间五行来调和关系（如木克土，可用火来调和）\n"
                solution_text += "   - 在居住环境中，可放置两人都适合的风水物品\n"
            else:
                solution_text += "1. 两人五行无特殊关系，建议：\n"
                solution_text += "   - 培养共同兴趣爱好，增进彼此了解\n"
                solution_text += "   - 尊重对方的生活习惯和个人空间\n"
            
            # 紫微斗数化解建议
            solution_text += "\n【紫微斗数化解建议】\n"
            male_main_star = male_ziwei.get('命宫主星', '')
            female_main_star = female_ziwei.get('命宫主星', '')
            
            # 根据主星组合给出建议
            if ('紫微' in male_main_star and '天府' in female_main_star) or ('天府' in male_main_star and '紫微' in female_main_star):
                solution_text += "1. 紫微天府组合，贵气十足，但需注意：\n"
                solution_text += "   - 避免过于强势，学会相互包容\n"
                solution_text += "   - 合理分工，发挥各自优势\n"
            elif ('贪狼' in male_main_star and '七杀' in female_main_star) or ('七杀' in male_main_star and '贪狼' in female_main_star):
                solution_text += "1. 贪狼七杀组合，个性强烈，建议：\n"
                solution_text += "   - 培养沟通技巧，避免冲动争吵\n"
                solution_text += "   - 寻找共同目标，增强协作精神\n"
            elif ('天机' in male_main_star and '太阴' in female_main_star) or ('太阴' in male_main_star and '天机' in female_main_star):
                solution_text += "1. 天机太阴组合，聪明睿智，建议：\n"
                solution_text += "   - 多交流思想，分享心得\n"
                solution_text += "   - 共同学习成长，提升自我\n"
            else:
                solution_text += "1. 根据两人主星特点，建议：\n"
                solution_text += "   - 相互欣赏对方的优点，包容缺点\n"
                solution_text += "   - 建立良好的沟通机制，及时解决问题\n"
            
            # 通用建议
            solution_text += "\n【关系改善建议】\n"
            solution_text += "1. 定期进行情感交流，分享生活点滴\n"
            solution_text += "2. 共同参与一些有益身心健康的活动，增进感情\n"
            solution_text += "3. 尊重彼此的家族文化和生活习惯\n"
            solution_text += "4. 在重要节日或纪念日，用心准备小礼物或惊喜\n"
            solution_text += "5. 如有需要，可咨询专业命理师进行更详细的合婚调理\n"
            
            # 显示结果
            self.compatibility_text.setPlainText(solution_text)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成建议过程中出现错误: {str(e)}')
    
    def refresh_knowledge_table(self):
        # 清空表格
        self.knowledge_table.setRowCount(0)
        
        # 获取选择的分类
        selected_category = self.category_combo.currentText()
        
        # 获取知识数据
        if selected_category == '所有分类':
            all_knowledge = []
            for category in self.knowledge_base.get_all_categories():
                for item in self.knowledge_base.get_knowledge_by_category(category):
                    item['category'] = category
                    all_knowledge.append(item)
        else:
            all_knowledge = self.knowledge_base.get_knowledge_by_category(selected_category)
            for item in all_knowledge:
                item['category'] = selected_category
        
        # 填充表格 - 只显示文件名和上传时间
        for i, item in enumerate(all_knowledge):
            self.knowledge_table.insertRow(i)
            # 文件名（从标题获取）
            self.knowledge_table.setItem(i, 0, QTableWidgetItem(item['title']))
            # 上传时间
            self.knowledge_table.setItem(i, 1, QTableWidgetItem(item['added_at']))
    
    def show_knowledge_detail(self, row, column):
        # 获取选中的知识项
        item_id = self.knowledge_table.item(row, 0).text()
        category = self.knowledge_table.item(row, 1).text()
        
        # 查找知识详情
        for item in self.knowledge_base.get_knowledge_by_category(category):
            if item['id'] == item_id:
                # 显示详情
                detail_text = f"标题: {item['title']}\n"
                detail_text += f"分类: {category}\n"
                detail_text += f"添加时间: {item['added_at']}\n"
                if item.get('source'):
                    detail_text += f"来源: {item['source']}\n"
                detail_text += "\n" + "=" * 50 + "\n\n"
                detail_text += item['content']
                
                self.knowledge_detail.setPlainText(detail_text)
                break
    
    def add_knowledge_dialog(self):
        # 创建添加知识的对话框，使用QMainWindow以支持最大最小化功能
        dialog = QMainWindow()
        dialog.setWindowTitle('添加知识')
        dialog.resize(600, 300)
        
        # 设置窗口标志，使其具有最大最小化按钮
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        
        central_widget = QWidget()
        dialog.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # 文件上传区域
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel('选择文件:'))
        file_path_input = QLineEdit()
        file_path_input.setReadOnly(True)
        file_layout.addWidget(file_path_input)
        
        file_btn = QPushButton('浏览...')
        file_layout.addWidget(file_btn)
        
        # 按钮布局
        btn_layout = QHBoxLayout()
        add_btn = QPushButton('上传')
        cancel_btn = QPushButton('取消')
        
        # 存储选中的文件路径列表
        selected_files = []
        
        # 分类关键词映射表，用于根据文件名自动匹配分类
        category_keywords = {
            "八字": ["八字", "四柱", "命理", "命盘", "天干", "地支", "五行"],
            "紫微斗数": ["紫微", "紫微斗数", "紫占", "紫微杨", "南北山人", "令东来"],
            "易经": ["易经", "周易", "卦象", "六壬"],
            "堪舆": ["风水", "堪舆", "地理"],
            "基础": ["基础", "入门", "简介", "整理", "原理"]
        }
        
        def select_files():
            nonlocal selected_files
            options = QFileDialog.Options()
            # 设置多选文件选项
            options |= QFileDialog.DontUseNativeDialog
            file_types = "支持的文件 (*.pdf *.docx);;PDF文件 (*.pdf);;Word文档 (*.docx)"
            file_paths, _ = QFileDialog.getOpenFileNames(
                dialog, "选择文件", "", file_types, options=options
            )
            
            if file_paths:
                selected_files = file_paths
                # 显示第一个文件路径作为示例，或显示文件数量
                if len(file_paths) == 1:
                    file_path_input.setText(file_paths[0])
                else:
                    file_path_input.setText(f"已选择 {len(file_paths)} 个文件")
        
        def auto_detect_category(file_name):
            """根据文件名自动检测并返回合适的分类"""
            file_name_lower = file_name.lower()
            # 遍历分类关键词映射表
            for category, keywords in category_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in file_name_lower:
                        return category
            # 如果没有匹配的关键词，返回默认分类
            return "未分类"
        
        def auto_learn_from_files():
            """自动从上传的文件中学习并形成逻辑算法"""
            try:
                print("开始自动学习文件内容...")
                
                # 获取最近上传的文件
                recent_knowledge = []
                for category, items in self.knowledge_base.knowledge.items():
                    # 按添加时间排序，获取最近的文件
                    recent_items = sorted(items, key=lambda x: x['added_at'], reverse=True)[:len(selected_files)]
                    recent_knowledge.extend(recent_items)
                
                # 从最近上传的文件中学习
                for item in recent_knowledge:
                    category = next((cat for cat, items in self.knowledge_base.knowledge.items() 
                                    for i in items if i['id'] == item['id']), "")
                    
                    if category and 'content' in item:
                        # 调用knowledge_base的学习方法
                        print(f"正在学习: {item['title']} (分类: {category})")
                        keywords = self.knowledge_base.learn_from_text(item['content'], category, item['title'])
                        print(f"提取的关键词: {keywords}")
                
                # 更新学习算法
                self.knowledge_base.update_learning_algorithm()
                
                # 增强知识学习能力
                self.knowledge_base.enhance_knowledge_learning()
                
                print("自动学习完成，系统已从上传的文件中获取新的知识和逻辑。")
            except Exception as e:
                print(f"自动学习过程中出错: {str(e)}")
        
        def add_knowledge():
            try:
                added_count = 0
                # 如果选择了多个文件
                if selected_files:
                    for file_path in selected_files:
                        file_ext = os.path.splitext(file_path)[1].lower()
                        # 从文件名提取标题
                        file_title = os.path.splitext(os.path.basename(file_path))[0]
                        # 自动检测分类
                        category = auto_detect_category(file_title)
                        
                        if file_ext == '.pdf':
                            # 解析PDF文件
                            self.knowledge_base.parse_pdf(file_path, category, file_title)
                            added_count += 1
                        elif file_ext == '.docx':
                            # 解析DOCX文件
                            self.knowledge_base.parse_docx(file_path, category, file_title)
                            added_count += 1
                        else:
                            print(f"跳过不支持的文件格式: {file_path}")
                else:
                    QMessageBox.warning(dialog, '警告', '请选择文件!')
                    return
                
                if added_count > 0:
                    # 触发自动学习功能
                    auto_learn_from_files()
                    
                    # 刷新知识表格（只显示文件名和上传时间）
                    self.refresh_knowledge_table()
                    
                    QMessageBox.information(dialog, '成功', f'成功上传 {added_count} 个文件并自动学习!')
                    dialog.close()
                else:
                    QMessageBox.warning(dialog, '警告', '没有成功上传任何文件!')
            except Exception as e:
                QMessageBox.critical(dialog, '错误', f'上传文件时出错: {str(e)}')
        
        file_btn.clicked.connect(select_files)
        add_btn.clicked.connect(add_knowledge)
        cancel_btn.clicked.connect(dialog.close)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(cancel_btn)
        
        # 添加到布局
        layout.addLayout(file_layout)
        # 添加学习中提示标签
        learning_label = QLabel("文件上传后系统将自动学习形成逻辑算法")
        learning_label.setStyleSheet("color: blue;")
        learning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(learning_label)
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        dialog.show()
    
    def delete_knowledge(self):
        # 获取选中的行
        selected_rows = self.knowledge_table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(self, '警告', '请先选择要删除的知识项!')
            return
        
        # 确认删除
        reply = QMessageBox.question(self, '确认', '确定要删除选中的知识项吗?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # 删除选中的知识项
            for row in selected_rows:
                item_id = self.knowledge_table.item(row.row(), 0).text()
                category = self.knowledge_table.item(row.row(), 1).text()
                self.knowledge_base.delete_knowledge(category, item_id)
            
            # 刷新知识表格
            self.refresh_knowledge_table()
            
            # 清空详情显示
            self.knowledge_detail.clear()
            
            QMessageBox.information(self, '成功', '知识删除成功!')

def main():
    # 确保中文显示正常
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = SuanMingApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()