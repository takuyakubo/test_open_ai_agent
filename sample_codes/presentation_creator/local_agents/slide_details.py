from agents import Agent
from pydantic import BaseModel

instruction = """
あなたはプレゼンテーション制作に特化したコンサルタントのエージェントです。
読み取った情報から詳細なスライド内容を生成してください各スライドには以下の情報を含めてください：
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


slide_details_agent = Agent(
    name="Slide Details Agent", instructions=instruction, output_type=SlideDetails
)
