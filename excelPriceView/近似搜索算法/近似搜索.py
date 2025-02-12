import pandas as pd
import Levenshtein
import tkinter as tk
from tkinter import ttk

# 读取 Excel 文件，包含所有的工作表
file_path = "Iphone.xlsx"
data_column = "Product"
xls = pd.ExcelFile(file_path)
texts = []
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    if data_column in df.columns:  # 检查是否存在 'Product' 列
        texts.extend(df[data_column].dropna().tolist())
    else:
        print(f"Warning: Column '{data_column}' not found in sheet '{sheet_name}'")

# 编辑距离相似度函数
def similarity_levenshtein(query, text):
    distance = Levenshtein.distance(query, text)
    max_len = max(len(query), len(text))
    return 1 - (distance / max_len)

# 搜索算法
def search_similar_texts(query, texts, similarity_func):
    results = []
    for text in texts:
        similarity = similarity_func(query, text)
        results.append((text, similarity))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

# 更新结果显示
def update_results(event):
    query = search_entry.get()
    results = search_similar_texts(query, texts, similarity_levenshtein)
    results_list.delete(0, tk.END)
    for text, similarity in results[:20]:
        results_list.insert(tk.END, f"Text: {text}, Similarity: {similarity:.2f}")

# 创建主窗口
root = tk.Tk()
root.title("Search")

# 创建搜索框
search_label = ttk.Label(root, text="Search:")
search_label.grid(row=0, column=0, padx=10, pady=10)
search_entry = ttk.Entry(root, width=50)
search_entry.grid(row=0, column=1, padx=10, pady=10)
search_entry.bind('<KeyRelease>', update_results)

# 创建结果显示区域
results_list = tk.Listbox(root, width=80, height=20)
results_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# 运行主循环
root.mainloop()