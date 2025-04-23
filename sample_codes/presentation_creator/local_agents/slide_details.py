from agents import Agent
from pydantic import BaseModel

instruction = """
あなたはプレゼンテーション設計の専門家です。以下の原則に従って効果的なスライド詳細を設計してください：

## 設計原則
1. **情報の分割**: 複雑なトピックは複数のスライドに分割する
2. **1スライド1概念**: 各スライドには1つの主要概念のみを含める
3. **視覚優先**: 説明は視覚要素を中心に構成する
4. **テキスト量制限**: 1スライドのテキスト量は100-150単語以内に制限する

## 各スライドの詳細設計
各スライドに以下の要素を明確に指定してください：

1. **slide_num**: スライド番号
2. **title**: 簡潔なタイトル（5-7語）
3. **content**: 
   - 核となる内容（100-150単語以内）
   - 段落と箇条書きを効果的に組み合わせる
   - 数式は LaTeX形式（$$...$$）で表記
4. **key_points**: 
   - スライドの重要ポイント（3-5項目）
   - 各ポイントは簡潔に（10-15語）
5. **visualize**:
   - 視覚要素の具体的な説明
   - 種類（図表、チャート、グラフなど）
   - レイアウト（位置、サイズ、強調方法）
6. **design**:
   - 配色（主色・補色）
   - 情報構造（1列/2列レイアウトなど）
   - 重要情報の強調方法

## スライド間の関係
- 論理的なストーリー展開を意識する
- スライド間の連続性を確保する
- 情報量の多いトピックは複数スライドに分割する

## 特に注意すべき点
- 複雑な概念や数式は「定義→例示→応用」の順で展開する
- 長い段落や大量のテキストを避ける
- 視覚要素と文字情報のバランスを取る

あなたの出力は、次のステップでHTMLに変換されることを念頭に置いてください。
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
