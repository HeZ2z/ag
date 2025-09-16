"""
命令行接口模块，提供CLI交互功能。

此模块实现了AI聊天和图像分析的命令行工具，支持文本对话、屏幕截图分析和指定图片分析。
用户可以通过选项直接与AI交互，无需额外子命令。
"""

import os
from typing import Optional
import click
from ..utils.screenshot import get_screenshot
from ..models.client import create_client


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-t", "--text", help="向AI发送的文本提示")
@click.option("-i", "--image", is_flag=True, help="分析屏幕截图")
@click.option("-p", "--path", help="要分析的图片路径")
@click.option("--prompt", help="更改AI的系统提示词，适用于文本对话和图像分析")
@click.option("--start", help="更改交互式模式的开场白")
def cli(
    text: Optional[str],
    image: bool,
    path: Optional[str],
    prompt: Optional[str],
    start: Optional[str],
):
    """
    AI命令行工具 - AI聊天和图像分析。

    支持文本对话、屏幕截图分析和指定图片分析。
    如果未提供任何选项，将进入交互式对话模式。

    示例:
        ag -t "请介绍一下自己"          # 文本对话 \n
        ag -i                         # 分析屏幕截图 \n
        ag -p /path/to/image.png      # 分析指定图片 \n
        ag -t "描述这张图" -i           # 带提示的截图分析 \n
        ag                            # 进入交互式模式 \n
        ag --prompt "你是一个医学专家"   # 设置交互式模式的 Prompt \n
        ag --start "你好，我是AI助手"    # 设置交互式模式的开场白 \n
        ag -h, --help                 # 显示帮助信息
    """
    try:
        if image or path:
            # 图像分析模式
            image_prompt = text if text else "请描述并分析这张图片中的内容"
            image_path = path if path else get_screenshot()
            system_prompt = prompt if prompt else "你是一个擅长分析图像的助手。"

            if not os.path.exists(image_path):
                click.echo(f"错误: 图片文件不存在: {image_path}")
                return

            click.echo(f"正在分析图片: {image_path}")
            client = create_client()
            client.image_text_completion(
                prompt=image_prompt,
                image_path=image_path,
                system_prompt=system_prompt,
                print_output=True,
            )
        elif text:
            # 文本对话模式
            system_prompt = prompt if prompt else "你是一个智能AI助手。"
            client = create_client()
            client.text_completion(
                prompt=text, system_prompt=system_prompt, print_output=True
            )
        else:
            # 交互式模式
            welcome_message = (
                start
                if start
                else "欢迎使用AI助手！我可以回答问题、提供信息或协助您完成任务。输入'exit'或'quit'退出对话。"
            )
            system_prompt = prompt if prompt else "你是一个智能AI助手。"
            click.echo(welcome_message)
            client = create_client()
            while True:
                user_input = click.prompt("用户", type=str)
                if user_input.lower() in ["exit", "quit"]:
                    break
                client.text_completion(
                    prompt=user_input, system_prompt=system_prompt, print_output=True
                )
    except FileNotFoundError as e:
        click.echo(f"文件未找到错误: {e}")
    except ValueError as e:
        click.echo(f"值错误: {e}")
    except OSError as e:
        click.echo(f"操作错误: {e}")


if __name__ == "__main__":
    # Click 自动处理命令行参数
    cli()
