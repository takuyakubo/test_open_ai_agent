from dotenv import load_dotenv
load_dotenv()

import nest_asyncio
nest_asyncio.apply()
import logfire
 
# Configure logfire instrumentation.
logfire.configure(
    service_name='my_agent_service',
    send_to_logfire=False,
)
# This method automatically patches the OpenAI Agents SDK to send logs via OTLP to Langfuse.
logfire.instrument_openai_agents()

from agents.tracing import GLOBAL_TRACE_PROVIDER
from agents.tracing.processors import BackendSpanExporter
class OffBackendSpanExporter(BackendSpanExporter):
    def export(*args, **kwargs):
        pass
GLOBAL_TRACE_PROVIDER.wrapped._multi_processor._processors[0]._exporter = OffBackendSpanExporter()

# sample

from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel as Model_
from agents import Agent, Runner
from openai import AsyncOpenAI

model = Model_(model="phi-4", openai_client=AsyncOpenAI(base_url="http://localhost:1234/v1/"))

simple_agent = Agent(
    name="Simple Agent",
    instructions="あなたは質問について答えるAgentです。",
    model=model
)

async def main():
    result = await Runner.run(simple_agent, input="アメリカの首都はどこですか？")
    print(result.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())