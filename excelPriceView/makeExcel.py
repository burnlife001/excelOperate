import pandas as pd
import numpy as np


# 定义灵动微表的数据生成函数
def generate_lingdongwei_data():
    names = ['MM32F0010', 'MM32G0001']
    prices = np.random.uniform(0.5, 1.0, 100)
    suppliers = np.random.choice(['上海', '北京', '深圳'], 100)
    return pd.DataFrame({'名称': names * 50, '价格': prices, '供应商': suppliers})

# 定义意法半导体表的数据生成函数
def generate_stmicro_data():
    names = ['STM32F0010', 'STM32F103RB', 'STM32F103RG']
    prices = np.random.uniform(2.5, 3.5, 100)
    suppliers = np.random.choice(['上海', '北京', '深圳'], 100)
    return pd.DataFrame({'名称': names * 33 + names[:1], '价格': prices, '供应商': suppliers})

# 生成数据
lingdongwei_df = generate_lingdongwei_data()
stmicro_df = generate_stmicro_data()

# 创建Excel文件并写入数据
with pd.ExcelWriter('报价单.xlsx') as writer:
    lingdongwei_df.to_excel(writer, sheet_name='灵动微', index=False)
    stmicro_df.to_excel(writer, sheet_name='意法半导体', index=False)
