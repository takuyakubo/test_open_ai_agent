from agents import Agent
from pydantic import BaseModel
from tools.orchastrate import infomation_to_slide_items, slide_items_to_html


class GeneratedResult(BaseModel):
    result: str
    "生成の結果"
    result_type: str
    "生成の結果のタイプ html, jsonなど"
    comment: str
    "生成結果に対するコメント"


instruction = """
あなたはプレゼンテーション制作に特化したコンサルタントのエージェントです。
まず、与えられた画像イメージに対して、画像の内容を詳細に分析してください。主要な要素、テキスト、構造を抽出してください。
ここから情報整理とスライド作成の工程が続きます。あとの工程のことを考えた上で、数式などできるだけ詳細に多くの量の情報を抽出して下さい。
"""
manager_agent = Agent(
    name="Slide Generator Agent",
    instructions=instruction,
    output_type=GeneratedResult,
    tools=[
        infomation_to_slide_items,
        slide_items_to_html,
    ],
)
