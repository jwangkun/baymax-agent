import os
import time
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import Type, List, Optional
from langchain_core.tools import BaseTool
from langchain_core.messages import AIMessage
from openai import APIConnectionError

from dexter.prompts import DEFAULT_SYSTEM_PROMPT

# Initialize the DeepSeek client using OpenAI API format
# DeepSeek API is compatible with OpenAI API format
# Only initialize if API key is provided
import warnings

def validate_api_key(api_key, provider):
    """Validate API key format"""
    if not api_key:
        return False
    if provider == "deepseek" and not api_key.startswith("sk-"):
        return False
    if provider == "openai" and not api_key.startswith("sk-"):
        return False
    return True

def initialize_llm():
    """Initialize LLM with proper error handling"""
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    # Try DeepSeek first
    if deepseek_key and validate_api_key(deepseek_key, "deepseek"):
        try:
            return ChatOpenAI(
                model="deepseek-chat",
                temperature=0,
                api_key=deepseek_key,
                base_url="https://api.deepseek.com/v1"
            )
        except Exception as e:
            warnings.warn(f"Failed to initialize DeepSeek: {e}")

    # Fallback to OpenAI
    if openai_key and validate_api_key(openai_key, "openai"):
        try:
            return ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0,
                api_key=openai_key
            )
        except Exception as e:
            warnings.warn(f"Failed to initialize OpenAI: {e}")

    # If no valid API keys, return a mock LLM that raises informative errors
    class MockLLM:
        def __getattr__(self, name):
            def mock_method(*args, **kwargs):
                raise RuntimeError(
                    "No valid API key found. Please set either:\n"
                    "- DEEPSEEK_API_KEY for DeepSeek model\n"
                    "- OPENAI_API_KEY for OpenAI model\n"
                    "Make sure the API keys are valid and start with 'sk-'"
                )
            return mock_method

    return MockLLM()

llm = initialize_llm()

def call_llm(
    prompt: str,
    system_prompt: Optional[str] = None,
    output_schema: Optional[Type[BaseModel]] = None,
    tools: Optional[List[BaseTool]] = None,
) -> AIMessage:
    final_system_prompt = system_prompt if system_prompt else DEFAULT_SYSTEM_PROMPT
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", final_system_prompt),
        ("user", "{prompt}")
    ])

    runnable = llm
    if output_schema:
        runnable = llm.with_structured_output(output_schema, method="function_calling")
    elif tools:
        runnable = llm.bind_tools(tools)
    
    chain = prompt_template | runnable
    
    # Retry logic for transient connection errors with timeout
    for attempt in range(3):
        try:
            # 添加超时机制，防止无限等待
            import concurrent.futures
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("LLM调用超时（30秒）")
            
            # 设置30秒超时
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(30)
            
            try:
                result = chain.invoke({"prompt": prompt})
                signal.alarm(0)  # 取消超时
                signal.signal(signal.SIGALRM, old_handler)
                return result
            except TimeoutError as te:
                signal.alarm(0)  # 取消超时
                signal.signal(signal.SIGALRM, old_handler)
                raise te
            except Exception as e:
                signal.alarm(0)  # 取消超时
                signal.signal(signal.SIGALRM, old_handler)
                raise e
                
        except TimeoutError as te:
            if attempt == 2:  # Last attempt
                raise
            # 超时重试前等待更长时间
            time.sleep(2 * (attempt + 1))
        except Exception as e:
            if attempt == 2:  # Last attempt
                raise
            time.sleep(0.5 * (2 ** attempt))  # 0.5s, 1s, 2s backoff
