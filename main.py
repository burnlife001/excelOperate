import pandas as pd
from deep_translator import GoogleTranslator

# 宏定义
SOURCE_COLUMN = '提示词(CN)'
TARGET_COLUMN = '提示词(EN)'
SHEET_NAME = 'aicoder'

# 初始化谷歌翻译器
translator = GoogleTranslator(source='zh-CN', target='en')  # 中文 --> 英语

# 读取Excel文件
file_path = 'prompt.xlsx'
df = pd.read_excel(file_path, sheet_name=SHEET_NAME)

# 翻译并写入目标列
for index, row in df.iterrows():
    prompt = row[SOURCE_COLUMN]
    if pd.notna(prompt):  # 检查是否为 NaN
        # 使用谷歌翻译引擎
        translation = translator.translate(prompt)
        df.at[index, TARGET_COLUMN] = translation

# 保存修改后的Excel文件
df.to_excel(file_path, sheet_name=SHEET_NAME, index=False)