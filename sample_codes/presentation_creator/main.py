import asyncio
from pathlib import Path

from agents import Runner
from dotenv import load_dotenv
from local_agents.manager_agents import manager_agent
from utils import image_paths_to_image_data_lists_open_ai

load_dotenv()

order = "2.1節で勉強会をやりたいのでこれらの内容を詳細にまとめて、HTMLのスライドにして下さい。"
image_paths = ["/path/to/image1", "/path/to/image12", "/path/to/image3"]
image_paths = [
    "/Users/takuyakubo/Desktop/転移学習スクショ/2章/2.1/IMG_0162.PNG",
    "/Users/takuyakubo/Desktop/転移学習スクショ/2章/2.1/IMG_0163.PNG",
    "/Users/takuyakubo/Desktop/転移学習スクショ/2章/2.1/IMG_0164.PNG",
]


async def main():
    content = [{"type": "input_text", "text": order}]
    content += image_paths_to_image_data_lists_open_ai(image_paths)
    msg = [{"role": "user", "content": content}]

    result = await Runner.run(manager_agent, msg)
    print(result.final_output)
    with Path("result.html").open("w") as f:
        f.write(result.final_output.result)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except asyncio.TimeoutError:
        print("操作がタイムアウトしました")
    except Exception as e:
        print("予期せぬエラーが発生しました: %s", e)
