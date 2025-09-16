"""
统一的 AI 客户端模块,支持 OpenAI 规范 API
"""

from typing import Optional, Any, Iterator, List, Union
import os
import base64
from openai import OpenAI
from openai.types.chat import ChatCompletionChunk, ChatCompletionMessageParam
from dotenv import load_dotenv


class AIClient:
    """
    统一的 AI 客户端类,支持 OpenAI 规范的接口
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        初始化 AI 客户端

        Args:
            api_key: API 密钥,如果为 None 则从环境变量读取
            base_url: API 基础 URL,如果为 None 则从环境变量读取
            model: 使用的模型名称,如果为 None 则从环境变量读取
        """
        # 如果未提供参数,从环境变量加载
        if api_key is None or base_url is None or model is None:
            load_dotenv()
            api_key = api_key or os.getenv("API_KEY")
            base_url = base_url or os.getenv("BASE_URL")
            model = model or os.getenv("MODEL")

        # 验证必要的配置
        if not api_key:
            raise ValueError("缺少 API 密钥,请设置环境变量 API_KEY 或在初始化时提供")
        if not base_url:
            raise ValueError(
                "缺少 API 基础 URL,请设置环境变量 BASE_URL 或在初始化时提供"
            )
        if not model:
            raise ValueError("缺少模型名称,请设置环境变量 MODEL 或在初始化时提供")

        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat_completion(
        self,
        messages: List[ChatCompletionMessageParam],
        stream: bool = True,
        include_usage: bool = True,
        **kwargs,
    ) -> Union[Iterator[ChatCompletionChunk], Any]:
        """
        创建聊天完成请求

        Args:
            messages: 消息列表
            stream: 是否使用流式响应
            include_usage: 是否包含使用情况统计
            **kwargs: 其他参数

        Returns:
            流式响应迭代器或完整响应
        """
        # 设置默认参数
        default_params = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
        }

        # 添加流式选项（如果启用了流式响应）
        if stream and include_usage:
            default_params["stream_options"] = {"include_usage": True}

        # 合并用户提供的额外参数
        params = {**default_params, **kwargs}

        # 发送请求
        return self.client.chat.completions.create(**params)

    def process_stream(
        self, completion: Iterator[ChatCompletionChunk], print_output: bool = True
    ) -> str:
        """
        处理流式响应

        Args:
            completion: 流式响应迭代器
            print_output: 是否打印输出

        Returns:
            完整的响应文本
        """
        full_response = ""
        usage_info = None

        try:
            for chunk in completion:
                if (
                    hasattr(chunk, "choices")
                    and chunk.choices
                    and hasattr(chunk.choices[0], "delta")
                    and hasattr(chunk.choices[0].delta, "content")
                ):
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        if print_output:
                            print(content, end="", flush=True)

                # 收集使用情况统计
                if hasattr(chunk, "usage") and chunk.usage:
                    usage_info = chunk.usage

            # 打印使用情况统计（如果有）
            if usage_info and print_output:
                print(
                    f"\n\n提问: {usage_info.prompt_tokens} tokens,"
                    f"回答: {usage_info.completion_tokens} tokens,"
                    f"总长度: {usage_info.total_tokens} tokens."
                )

            return full_response
        except Exception as e:
            if print_output:
                print(f"\n处理响应时发生错误: {e}")
            raise

    def text_completion(
        self,
        prompt: str,
        system_prompt: str = "你是这个领域的专家，请告诉我你会怎么做这件事。",
        stream: bool = True,
        print_output: bool = True,
        **kwargs,
    ) -> str:
        """
        简单的文本完成请求

        Args:
            prompt: 用户提示
            system_prompt: 系统提示
            stream: 是否使用流式响应
            print_output: 是否打印输出
            **kwargs: 其他参数

        Returns:
            完整的响应文本
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        completion = self.chat_completion(messages=messages, stream=stream, **kwargs)

        if stream:
            return self.process_stream(completion, print_output=print_output)

        # 非流式响应处理
        response = completion.choices[0].message.content
        if print_output:
            print(response)
        return response

    def image_text_completion(
        self,
        prompt: str,
        image_path: str,
        system_prompt: str = "你是一个擅长分析图像的助手。",
        stream: bool = True,
        print_output: bool = True,
        **kwargs,
    ) -> str:
        """
        图像分析完成请求

        Args:
            prompt: 用户提示
            image_path: 图像路径或base64编码的图像
            system_prompt: 系统提示
            stream: 是否使用流式响应
            print_output: 是否打印输出
            **kwargs: 其他参数

        Returns:
            完整的响应文本
        """
        # 确定图像格式
        if image_path.startswith("data:image"):
            image_url = image_path
        else:
            # 读取并编码图像
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                image_url = f"data:image/png;base64,{base64_image}"

        # 构建消息
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": system_prompt}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                    {"type": "text", "text": prompt},
                ],
            },
        ]

        # 默认添加 modalities 参数
        if "modalities" not in kwargs:
            kwargs["modalities"] = ["text"]

        # 发送请求
        completion = self.chat_completion(messages=messages, stream=stream, **kwargs)

        if stream:
            return self.process_stream(completion, print_output=print_output)

        # 非流式响应处理
        response = completion.choices[0].message.content
        if print_output:
            print(response)
        return response


# 创建单例实例
def create_client(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
) -> AIClient:
    """
    创建或获取 AI 客户端实例

    Args:
        api_key: API 密钥
        base_url: API 基础 URL
        model: 使用的模型名称

    Returns:
        AIClient 实例
    """
    try:
        return AIClient(api_key=api_key, base_url=base_url, model=model)
    except Exception as e:
        print(f"创建客户端时发生错误: {e}")
        raise
