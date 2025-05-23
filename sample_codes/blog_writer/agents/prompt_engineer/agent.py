from agents import Agent
from ...models.models import MetaOutput

meta_instruction = """あなたは卓越したプロンプエンジニアです。
これまでの会話をまとめて精度高く最終的な文章を得るためにはどのようなプロンプトを書くべきか示してください。
また、改善するにあって、他の記事制作にも活かせる知見をkowledgeとしてmarkdownにまとめてください。
"""

prompt_engineer = Agent(name="PromptEngineer", instructions=meta_instruction, output_type=MetaOutput) 