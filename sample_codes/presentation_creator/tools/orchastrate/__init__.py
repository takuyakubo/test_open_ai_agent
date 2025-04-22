from local_agents.html_gen import html_slide_generation_agent
from local_agents.slide_details import slide_details_agent

infomation_to_slide_items = slide_details_agent.as_tool(
    tool_name="infomation_to_slide_items",
    tool_description="与えられた情報を解析しスライドの要素に書き換えます。",
)
slide_items_to_html = html_slide_generation_agent.as_tool(
    tool_name="slide_items_to_html",
    tool_description="スライドの要素をもとにHTMLドキュメントを作成します。",
)
