# .chm_XLF_Translator-
这是一款专为.chm等文档批量翻译而设计的极简图形化工具 This is a minimalist graphical tool designed for batch translation of .chm and other documents


# XLF一键翻译助手

## 什么是 .chm 文件？

`.chm` 文件（Compiled HTML Help）是微软推出的一种帮助文档格式，广泛用于软件的离线帮助系统。它本质上是将HTML、图片、索引等内容打包压缩成一个文件，支持目录、全文检索、超链接等功能。



## 依赖安装

本工具基于 Python 3 开发，需安装以下依赖：

```bash
pip install pygtrans docts
```

## 使用流程

### 1. 用 Sisulizer 导出 XLF 文件

1. 安装并打开 Sisulizer（建议使用专业版）。
2. 新建项目，导入你的 `.chm` 文件。
3. 在 Sisulizer 菜单中选择"导出"或"导出为 XLIFF (XLF)"格式。
4. 选择导出路径，得到 `.xlf` 文件。

### 2. 用 XLF一键翻译助手 翻译 XLF 文件

1. 运行本工具（`xlf_translator_gui.py`）。
2. 选择 Sisulizer 导出的 `.xlf` 文件。
3. 可自定义过滤关键词（如 `TODO,不翻译`）和类型（如 `code,page:3`），避免不需要的内容被翻译。
4. 如需代理，填写代理地址。
5. 点击"一键翻译"，等待进度条完成。
6. 翻译完成后，工具会自动生成翻译后的 `.xlf` 文件。

### 3. 用 Sisulizer 导入翻译后的 XLF 并编译为 .chm

1. 回到 Sisulizer，打开原项目。
2. 选择"导入"功能，将翻译后的 `.xlf` 文件导入。
3. 检查翻译内容，有需要可手动修正。
4. 点击"用选定的语言建立所有的源"按钮，导出最终的翻译后的 `.chm` 文件。
<img width="425" alt="屏幕截图 2025-05-01 225426" src="https://github.com/user-attachments/assets/f25bcf79-c2d2-4ba0-bb13-5581c701bc5f" />

5.目录下即可看到输出的文件
ps:如果出现错误可以在releases中下载“htmlhelp.exe”安装一遍 Sisulizer软件也可见于releases中 点击评估版的就行 30天也够用。

---

本工具支持深色/浅色/系统主题、进度条显示、高分屏适配，适合批量文档本地化、技术资料翻译等场景。 




