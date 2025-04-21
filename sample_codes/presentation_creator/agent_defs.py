from pathlib import Path

from agents import Agent
from pydantic import BaseModel

instruction = """
あなたはプレゼンテーション制作に特化したコンサルタントのエージェントです。
まず、与えられた画像イメージに対して、画像の内容を詳細に分析してください。主要な要素、テキスト、構造を抽出してください。
次に、読み取った情報から詳細なスライド内容を生成してください各スライドには以下の情報を含めてください：
            1. スライド番号
            2. タイトル
            3. 内容（完全な文章）
            4. 視覚的要素（図表、画像の説明）
            5. デザインの提案
"""


class SlideInfo(BaseModel):
    slide_num: str
    "スライド番号"
    title: str
    "タイトル"
    content: str
    "内容（完全な文章）"
    visualize: str
    "視覚的要素（図表、画像の説明）"
    design: str
    "デザインの提案"


class SlideDetails(BaseModel):
    data: list[SlideInfo]


image_proc_agent = Agent(
    name="Image to Slide Info Agent", instructions=instruction, output_type=SlideDetails
)

current_path = Path(__file__)
template_path = current_path.parent / "default.html"
html_template = template_path.read_text()

instruction = f"""
あなたはスライドデータからHTMLを生成するアシスタントです。
与えられたスライドデータからHTMLを生成してください。
作成する以下のHTMLテンプレートを使用し、{{TITLE}}をプレゼンテーションのタイトルに、{{SLIDES}}を個々のスライドのHTMLに置き換えてください：
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


class GeneratedResult(BaseModel):
    result: str
    "生成の結果"
    result_type: str
    "生成の結果のタイプ html, jsonなど"
    comment: str
    "生成結果に対するコメント"


manager_agent = Agent(
    name="Slide Generator Agent",
    instructions="あなたはスライドの作成をサポートするエージェントです。",
    output_type=GeneratedResult,
    tools=[
        image_proc_agent.as_tool(
            tool_name="image_to_slide_items",
            tool_description="与えられた画像を解析しスライドの要素に書き換えます。",
        ),
        html_slide_generation_agent.as_tool(
            tool_name="slide_items_to_html",
            tool_description="スライドの要素をもとにHTMLドキュメントを作成します。",
        ),
    ],
)
# image_proc_agent.handoffs = [slide_generation_agent]
