import sys
import re
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLineEdit, QLabel, 
                            QTableWidget, QTableWidgetItem, QMessageBox,
                            QCheckBox)
from PyQt6.QtCore import Qt

class PriceQueryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('报价查询系统')
        self.setGeometry(100, 100, 800, 600)
        self.df = None
        self.df_bak = None
        
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 搜索区域
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('请输入搜索关键词...')
        search_layout.addWidget(self.search_input)
        
        # 按钮和复选框区域
        self.search_btn = QPushButton('全字匹配')
        self.auto_search_checkbox = QCheckBox('前缀匹配')
        self.auto_search_checkbox.setChecked(True)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.auto_search_checkbox)
        
        layout.addLayout(search_layout)
        
        # 创建表格
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        # 连接信号
        self.search_btn.clicked.connect(self.exact_search)
        self.search_input.textChanged.connect(self.on_text_changed)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #ddd;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 4px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
            QCheckBox {
                padding: 8px;
            }
        """)

    def on_text_changed(self, text):
        """输入框文本变化时的响应函数"""
        if self.auto_search_checkbox.isChecked() and text:
            self.fuzzy_search()

    def load_data(self):
        """重新加载Excel数据"""
        try:
            # 读取所有sheet页
            all_sheets = pd.read_excel('报价单.xlsx', sheet_name=None)
            # 合并所有sheet页的数据
            self.df = pd.concat(all_sheets.values(), ignore_index=True)
            # 删除所有列都为空的行
            self.df = self.df.dropna(how='all')
            # 备份原始数据
            self.df_bak = self.df.copy()
            # 更新表格列
            self.table.setColumnCount(len(self.df.columns))
            self.table.setHorizontalHeaderLabels(self.df.columns)
            print("成功加载报价单.xlsx的所有sheet页")
        except Exception as e:
            print(self, '错误', f'无法加载报价单.xlsx: {str(e)}')
            return False
        return True
            
    def clear_table(self):
        """清空表格"""
        self.table.setRowCount(0)
        
    def exact_search(self):
        """精确搜索，忽略大小写"""
        # 清空表格
        self.clear_table()
        
        # 重新加载数据
        if not self.load_data():
            return
            
        keyword = self.search_input.text().strip()
        if not keyword:
            print(self, '警告', '请输入搜索关键词')
            return
            
        # 转换关键词为小写
        keyword = keyword.lower()
        print(f"精确搜索关键词: {keyword}")
        
        # 在所有列中搜索
        result_indices = set()
        for column in self.df.columns:
            # 将当前列转换为小写进行搜索
            matches = self.df[column].astype(str).str.lower() == keyword
            result_indices.update(matches[matches].index)
            print(f"列 {column} 中的匹配: {matches[matches].index.tolist()}")
        
        # 使用原始数据更新表格
        if result_indices:
            result_data = self.df_bak.iloc[list(result_indices)]
            self.update_table(result_data)
            print(f"精确搜索结果: {result_data}")
        else:
            print("精确搜索: 未找到匹配项")
        
    def fuzzy_search(self):
        """前缀匹配搜索"""
        # 清空表格
        self.clear_table()
        
        # 重新加载数据
        if not self.load_data():
            return
            
        keyword = self.search_input.text().strip()
        if not keyword:
            print(self, '警告', '请输入搜索关键词')
            return
            
        # 转换关键词为小写
        keyword = keyword.lower()
        print(f"前缀匹配搜索关键词: {keyword}")
        
        # 在所有列中进行前缀匹配搜索
        result_indices = set()
        for column in self.df.columns:
            # 将当前列转换为小写并进行前缀匹配
            matches = self.df[column].astype(str).str.lower().str.startswith(keyword)
            result_indices.update(matches[matches].index)
            print(f"列 {column} 中的前缀匹配: {matches[matches].index.tolist()}")
        
        # 使用原始数据更新表格
        if result_indices:
            result_data = self.df_bak.iloc[list(result_indices)]
            self.update_table(result_data)
            print(f"前缀匹配搜索结果: {result_data}")
        else:
            print("前缀匹配搜索: 未找到匹配项")
        
    def update_table(self, df):
        """更新表格显示"""
        self.table.setRowCount(len(df))
        for i, (_, row) in enumerate(df.iterrows()):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)

def main():
    app = QApplication(sys.argv)
    window = PriceQueryApp()
    window.show()
    # 初始加载数据
    window.load_data()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()