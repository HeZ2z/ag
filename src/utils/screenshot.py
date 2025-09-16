"""
截图处理模块,负责截取屏幕截图并将其发送到 AI 服务进行分析
"""

import os
from typing import Optional, Union, Iterator
import base64
import pyautogui
from openai.types.chat import ChatCompletionChunk

from src.models.client import create_client


def get_screenshot(save_path: str = "./test.png") -> str:
    """
    截取屏幕截图并保存

    Args:
        save_path: 保存截图的路径

    Returns:
        保存的截图路径
    """
    # 确保目录存在
    os.makedirs(os.path.dirname(os.path.abspath(save_path)) or ".", exist_ok=True)

    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)
    return save_path


def encode_image(image_path: str) -> str:
    """
    将图片编码为 base64

    Args:
        image_path: 图片路径

    Returns:
        base64 编码的图片

    Raises:
        FileNotFoundError: 如果图片不存在
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze_screenshot(
    prompt: str = "图中描绘的是什么景象？", image_path: Optional[str] = None
) -> Union[str, Iterator[ChatCompletionChunk]]:
    """
    分析截图并返回AI的描述

    Args:
        prompt: 发送给AI的提示
        image_path: 图片路径,如果为None则自动截图

    Returns:
        AI的描述或流式响应对象
    """
    # 如果未提供图片路径,则自动截图
    if not image_path:
        image_path = get_screenshot()

    try:
        # 创建客户端
        client = create_client()

        # 发送图像分析请求
        return client.image_text_completion(
            prompt=prompt,
            image_path=image_path,
            system_prompt="你是一个擅长分析图像的助手。",
            stream=True,
            print_output=False,
        )
    except Exception as e:
        print(f"分析截图时发生错误: {e}")
        raise
