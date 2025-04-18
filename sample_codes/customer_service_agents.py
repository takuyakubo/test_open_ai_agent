from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()


@function_tool
def search_knowledge_base(query: str) -> str:
    return f"{query}に対する関連する記事は以下のとおりです。xxx, yyy, zzz"


@function_tool
def initiate_purchase_order(user_id: str, product_id: str) -> str:
    return f"user_id: {user_id}様の商品: {product_id}の購入手続きを開始しました。"


@function_tool
def track_order_status(user_id: str) -> str:
    return (
        f"user_id: {user_id}様の商品の発送状態は以下のとおりです。\n"
        "商品 x:\n"
        "1日3時間50分前: 発送準備中になりました。\n"
        "2時間30分前: センターから発送しました。\n"
        "1時間20分前: 中継センターから発送しました。\n"
        "5分前: 配達センターが受領しました。\n"
        "商品 y:\n"
        "1日4時間50分前: 発送準備中になりました。\n"
        "8時間20分前: センターから発送しました。\n"
        "6時間20分前: 中継センターから発送しました。\n"
        "2時間20分前: 配達センターが受領しました。\n"
        "20分前: 配達中です。\n"
    )


@function_tool
def initiate_refund_process(user_id: str, product_id: str) -> str:
    return f"user_id: {user_id}様の商品: {product_id}の返金手続きを開始しました。"


technical_support_agent = Agent(
    name="Technical Support Agent",
    instructions=(
        "技術的な問題、システム障害、または製品のトラブルシューティングを解決するための専門的なサポートを提供して下さい。"
    ),
    tools=[search_knowledge_base],
)

sales_assistant_agent = Agent(
    name="Sales Assistant Agent",
    instructions=(
        "顧客が製品カタログを閲覧し、適切なソリューションを推薦し、購入取引をスムーズに進めるお手伝いをして下さい。"
    ),
    tools=[initiate_purchase_order],
)

order_management_agent = Agent(
    name="Order Management Agent",
    instructions=(
        "あなたは注文の追跡、配送スケジュール、返品や返金の手続きに関するお客様からの問い合わせをサポートします。"
    ),
    tools=[track_order_status, initiate_refund_process],
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "あなたはカスタマーサービスの顧客対応エージェントです。あなたは最初の窓口として機能し、"
        "お客様からの問い合わせを評価して、迅速に適切な専門エージェントへ案内して下さい。"
    ),
    handoffs=[technical_support_agent, sales_assistant_agent, order_management_agent],
)


async def main():
    msg = "最近購入した品物の配送状況について最新情報を教えてもらえますか？ユーザーIDはu88です。"

    orchestrator_output = await Runner.run(triage_agent, input=msg)
    for message in orchestrator_output.new_items:
        print(f"  -- 対応 step: {message.raw_item}")

    print()
    print(orchestrator_output.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

# =>  -- 対応 step: ResponseFunctionToolCall(arguments='{}', call_id='call_W***T', name='transfer_to_order_management_agent', type='function_call', id='fc_6***e', status='completed')
# =>  -- 対応 step: {'call_id': 'call_W***T', 'output': "{'assistant': 'Order Management Agent'}", 'type': 'function_call_output'}
# =>  -- 対応 step: ResponseFunctionToolCall(arguments='{"user_id":"u88"}', call_id='call_L***l', name='track_order_status', type='function_call', id='fc_6***e', status='completed')
# =>  -- 対応 step: {'call_id': 'call_L***l', 'output': 'user_id: u88様の商品の発送状態は以下のとおりです。\n商品 x:\n1日3時間50分前: 発送準備中になりました。\n2時間30分前: センターから発送しました。\n1時間20分前: 中継センターから発送しました。\n5分前: 配達センターが受領しました。\n商品 y:\n1日4時間50分前: 発送準備中になりました。\n8時間20分前: センターから発送しました。\n6時間20分前: 中継センターから発送しました。\n2時間20分前: 配達センターが受領しました。\n20分前: 配達中です。\n', 'type': 'function_call_output'}
# =>  -- 対応 step: ResponseOutputMessage(id='msg_6***e', content=[ResponseOutputText(annotations=[], text='ユーザーID u88様の配送状況は以下の通りです。\n\n**商品 x:**\n- 1日3時間50分前: 発送準備中\n- 2時間30分前: センターから発送\n- 1時間20分前: 中継センターから発送\n- 5分前: 配達センターが受領\n\n**商品 y:**\n- 1日4時間50分前: 発送準備中\n- 8時間20分前: センターから発送\n- 6時間20分前: 中継センターから発送\n- 2時間20分前: 配達センターが受領\n- 20分前: 配達中\n\nご不明な点がございましたら、お知らせください。', type='output_text')], role='assistant', status='completed', type='message')
# =>
# => ユーザーID u88様の配送状況は以下の通りです。
# =>
# => **商品 x:**
# => - 1日3時間50分前: 発送準備中
# => - 2時間30分前: センターから発送
# => - 1時間20分前: 中継センターから発送
# => - 5分前: 配達センターが受領
# =>
# => **商品 y:**
# => - 1日4時間50分前: 発送準備中
# => - 8時間20分前: センターから発送
# => - 6時間20分前: 中継センターから発送
# => - 2時間20分前: 配達センターが受領
# => - 20分前: 配達中
#
# => ご不明な点がございましたら、お知らせください。

# msg = "最近購入した品物の配送状況について最新情報を教えてもらえますか？" とした場合(user id不明の場合)
# => -- 対応 step: ResponseFunctionToolCall(arguments='{}', call_id='call_G***i', name='transfer_to_order_management_agent', type='function_call', id='fc_6***2', status='completed')
# => -- 対応 step: {'call_id': 'call_G***i', 'output': "{'assistant': 'Order Management Agent'}", 'type': 'function_call_output'}
# => -- 対応 step: ResponseOutputMessage(id='msg_6***2', content=[ResponseOutputText(annotations=[], text='ご注文の配送状況を確認するために、お客様のユーザーIDを教えていただけますか？', type='output_text')], role='assistant', status='completed', type='message')
#
# => ご注文の配送状況を確認するために、お客様のユーザーIDを教えていただけますか？
