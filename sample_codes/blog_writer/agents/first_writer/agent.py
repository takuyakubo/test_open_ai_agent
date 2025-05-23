from agents import Agent
from ...models.models import ArticleOutput

def create_input_topic(topic, target, objective, keywords, length, tone):
    return f"""
あなたは優れたWebコンテンツライターです。以下の要件に基づいて記事の初稿を生成してください。
【記事の主題】: {topic}
【対象読者】: {target}
【記事の目的】: {objective}
【主要キーワード】: {keywords}
【記事の長さ】: {length}
【トーン】: {tone}
【構成要素】: 
- 導入部（読者の興味を引く書き出し）
- 本文（3〜5つの主要セクションに分ける）
- 具体例や事例を含める
- データや統計を適切に引用する
- 視覚的な要素の提案（図表やイメージの説明）
- まとめと次のアクション
"""

firstwrite_instruction = """あなたは優れたWebコンテンツライターです。以下の要件に基づいて記事の初稿を生成してください。

- 専門用語は初心者にもわかるように説明する
- 段落は短めに保ち、読みやすさを重視する
- 見出しは検索意図に合わせて作成する
- 文末は能動態を優先し、説得力のある文章にする

出力形式はマークダウン形式で、見出しの階層構造を明確にしてください。

この指示を参考に、読者にとって価値のある、情報量が豊富で魅力的な記事の初稿を作成してください。
現時点では完璧を目指さず、後の評価と改善のプロセスを前提とした基礎となる文章を作成することに集中してください。"""

first_writer = Agent(name="First Writer", instructions=firstwrite_instruction, output_type=ArticleOutput) 