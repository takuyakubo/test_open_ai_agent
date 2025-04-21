import asyncio
import base64
from pathlib import Path

from agent_defs import image_proc_agent, slide_generation_agent
from agents import Runner
from dotenv import load_dotenv

load_dotenv()


def image_to_image_data_str(image):
    # 画像をbase64エンコード
    if isinstance(image, str):  # 画像がパスとして提供された場合
        with open(image, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    else:
        raise Exception(f"サポートされていない画像形式です (画像 {image})")


order = "2.1節で勉強会をやりたいのでこれらの内容を詳細にまとめて、HTMLのスライドにして下さい。"
image_paths = ["/path/to/image1", "/path/to/image2", "/path/to/image3"]


async def main():
    content = [{"type": "input_text", "text": order}]
    content += [
        {
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{image_to_image_data_str(image_path)}",
        }
        for image_path in image_paths
    ]
    msg = [{"role": "user", "content": content}]
    result = await Runner.run(image_proc_agent, msg)

    slide_contents = result.final_output.model_dump()
    msg = f"""
        以下の内容を使ってHTMLを作成して下さい。
        # 内容
        {slide_contents}
        """
    result = await Runner.run(slide_generation_agent, msg)
    with Path("result.html").open("w") as f:
        f.write(result.final_output.html)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except asyncio.TimeoutError:
        print("操作がタイムアウトしました")
    except Exception as e:
        print("予期せぬエラーが発生しました: %s", e)
