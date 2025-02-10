# 对 Excel 文件中的内容进行翻译的工具(谷歌)

## 依赖

```sh
pip install -r requirements.txt
```

## 使用方法

将需要翻译的 Excel 文件命名为 prompt.xlsx 并放置在项目根目录下。
确保 Excel 文件中包含以下列：
提示词(CN)：需要翻译的中文内容
提示词(EN)：翻译后的英文内容

运行 main.py 脚本进行翻译，当安装了虚拟环境时，用run_mian.py 运行main.py。
