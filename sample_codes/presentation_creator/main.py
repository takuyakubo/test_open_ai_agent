import asyncio
import base64
import mimetypes
from pathlib import Path

from agent_defs import manager_agent
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


def image_path_to_image_data(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    image_data = image_to_image_data_str(image_path)
    return mime_type, image_data


order = "2.1節で勉強会をやりたいのでこれらの内容を詳細にまとめて、HTMLのスライドにして下さい。"
image_paths = ["/path/to/image1", "/path/to/image12", "/path/to/image3"]


async def main():
    content = [{"type": "input_text", "text": order}]
    content += [
        {
            "type": "input_image",
            "image_url": f"data:{mime_type};base64,{image_data}",
        }
        for mime_type, image_data in [
            image_path_to_image_data(image_path) for image_path in image_paths
        ]
    ]
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
