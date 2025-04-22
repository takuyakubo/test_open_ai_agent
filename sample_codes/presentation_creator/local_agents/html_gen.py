from pathlib import Path

from agents import Agent
from pydantic import BaseModel

current_path = Path(__file__)
template_path = current_path.parent / "materials" / "default.html"
html_template = template_path.read_text()

instruction = f"""
あなたはスライドデータからHTMLを生成するアシスタントです。
与えられたスライドデータからHTMLを生成してください。
作成する以下のHTMLテンプレートを使用し、{{TITLE}}をプレゼンテーションのタイトルに、{{SLIDES}}を個々のスライドのHTMLに置き換えてください:
            {html_template}
各スライドは<div class="slide">要素として生成し、タイトルは<h1 class="slide-title">、内容は<div class="slide-content">の中に配置してください。
各スライド内容は精査した上で、適切なHTML要素を使い適切なclassをつけて、画像以外の部分について、デザインとしてきちんとしたスライドとなるようにして下さい。
与えられた情報に対して文字列をそのままスライドに記述することは禁止されています。情報構造を捉えた上で適切に言い換え、デザインをして下さい。
"""


class GeneratedHTML(BaseModel):
    html: str
    "HTML"
    note: str
    "htmlを使うにあたって、気をつけるべきこと"


html_slide_generation_agent = Agent(
    name="HTML Slide Generation Agent",
    instructions=instruction,
    output_type=GeneratedHTML,
)
