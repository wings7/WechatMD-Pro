import os
import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 中的配置
load_dotenv()

API_KEY = os.getenv("MIMO_API_KEY")
BASE_URL = os.getenv("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1")
MODEL = os.getenv("MIMO_MODEL", "mimo-chat")

if not API_KEY:
    print("❌ 请先在 .env 文件中设置 MIMO_API_KEY")
    sys.exit(1)

# 精心设计的 system prompt，保障公众号排版质量
SYSTEM_PROMPT = """
你是一个超级牛逼专业的微信公众号排版助手。你的任务是将用户提供的 Markdown 文本转换为可直接粘贴到公众号编辑器的 HTML 代码。

要求：
1. 只输出 HTML 代码片段（不要包含 <!DOCTYPE>, <html>, <head>, <body> 等标签）。
2. 所有样式必须以内联 style 属性方式写在标签里，不允许使用 class 或 <style> 标签。
3. 整体风格清新简约，正文字体使用“微软雅黑”，字号15px，行高1.8，颜色#333。
4. 标题（h2/h3）字号适当加大，颜色#2c3e50，加粗。
5. 代码块使用 <pre style="..."> 和 <code style="...">，背景色 #f4f4f4，等宽字体 Consolas, Monaco, monospace，字号13px，圆角6px，内边距15px，暗色文字，自动换行。
6. 行内代码使用 <code style="background-color:#f0f0f0; padding:2px 6px; border-radius:4px; font-family:monospace;">。
7. 无序列表和有序列表保留原有结构，注意缩进。
8. 图片标签为 <img src="原地址" style="max-width:100%; border-radius:4px; display:block; margin:10px auto;">。
9. 自动在中文字符和英文字符、数字之间添加一个空格（如 "使用 React 开发" 正确），但注意HTML标签内不添加额外空格。
10. 普通段落使用 <p style="..."> 或 <section style="...">，不要用 div。
11. 输出的 HTML 代码必须完整且格式整洁，开始可以直接粘贴使用。

用户输入的 Markdown 如下：
"""

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def markdown_to_wechat_html(md_text: str) -> str:
    """调用 MiMo API 将 Markdown 转为公众号 HTML"""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": md_text}
            ],
            temperature=0.3,  # 降低随机性，保证输出稳定
            max_tokens=4096
        )
        html = response.choices[0].message.content.strip()
        # 如果模型输出被包裹在 ``` 中，则去除
        if html.startswith("```html"):
            html = html[7:]
        if html.startswith("```"):
            html = html[3:]
        if html.endswith("```"):
            html = html[:-3]
        return html
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("用法: python wechatmd.py <markdown文件路径>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"❌ 文件不存在: {md_path}")
        sys.exit(1)

    md_text = md_path.read_text(encoding="utf-8")
    print(f"📝 正在转换 {md_path.name} ...")
    html_result = markdown_to_wechat_html(md_text)

    out_path = md_path.with_suffix(".html")
    out_path.write_text(html_result, encoding="utf-8")
    print(f"✅ 转换完成！结果已保存至: {out_path}")
    print("   打开该文件，全选复制内容到公众号编辑器即可。")

if __name__ == "__main__":
    main()
