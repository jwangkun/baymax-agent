import os
import time
from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool
from pydantic import BaseModel
import warnings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 全局ModelManager实例
_model_manager = None

def get_model_manager():
    """获取ModelManager实例"""
    global _model_manager
    if _model_manager is None:
        from baymax.model_manager import ModelManager
        _model_manager = ModelManager()
    return _model_manager

def call_llm(prompt: str, system_prompt=None, output_schema=None, tools=None):
    """统一的LLM调用接口"""
    model_manager = get_model_manager()
    model = model_manager.get_current_model()
    
    if not model:
        raise RuntimeError("没有可用的模型")
    
    try:
        if tools:
            return model.generate_with_tools(prompt, tools, system_prompt)
        elif output_schema:
            return model.generate_structured(prompt, output_schema, system_prompt)
        else:
            return model.generate(prompt, system_prompt)
    except Exception as e:
        raise RuntimeError(f"LLM调用失败: {e}")

class Model:
    """统一的AI模型接口"""
    
    def __init__(self, provider: str, api_key: str, model_name: str, base_url: str = None):
        self.provider = provider
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """初始化对应的LLM实例"""
        try:
            # 禁用SSL警告
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            if self.provider == 'openai':
                # 为DeepSeek等兼容OpenAI API的模型添加SSL验证禁用
                if self.base_url and "deepseek" in self.base_url.lower():
                    import httpx
                    http_client = httpx.Client(verify=False)
                else:
                    http_client = None
                    
                self.llm = ChatOpenAI(
                    model=self.model_name,
                    temperature=0,
                    api_key=self.api_key,
                    base_url=self.base_url,
                    http_client=http_client,
                    model_kwargs={"response_format": {"type": "json_object"}} if "gpt-4" in self.model_name.lower() or "gpt-3.5" in self.model_name.lower() else {}
                )
            elif self.provider == 'gemini':
                self.llm = ChatGoogleGenerativeAI(
                    model=self.model_name,
                    temperature=0,
                    google_api_key=self.api_key
                )
            elif self.provider == 'claude':
                self.llm = ChatAnthropic(
                    model=self.model_name,
                    temperature=0,
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            else:
                raise ValueError(f"不支持的模型提供商: {self.provider}")
        except Exception as e:
            warnings.warn(f"初始化 {self.provider} 模型失败: {e}")
            self.llm = None
    
    def is_available(self) -> bool:
        """检查模型是否可用"""
        return self.llm is not None and self.api_key and len(self.api_key) > 0
    
    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """生成文本响应"""
        if not self.is_available():
            raise RuntimeError(f"模型 {self.provider} 不可用")
        
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            
            if system_prompt:
                # 使用正确的消息结构
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=prompt)
                ]
                result = self.llm.invoke(messages)
            else:
                # 如果没有系统提示，直接使用简单的消息格式
                messages = [HumanMessage(content=prompt)]
                result = self.llm.invoke(messages)
            
            if hasattr(result, 'content'):
                return result.content
            else:
                return str(result)
                
        except Exception as e:
            raise RuntimeError(f"{self.provider} 模型生成失败: {e}")
    
    def generate_with_tools(self, prompt: str, tools: List[BaseTool], system_prompt: str = None) -> AIMessage:
        """使用工具生成响应"""
        if not self.is_available():
            raise RuntimeError(f"模型 {self.provider} 不可用")
        
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            
            llm_with_tools = self.llm.bind_tools(tools)
            
            if system_prompt:
                # 使用正确的消息结构
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=prompt)
                ]
                result = llm_with_tools.invoke(messages)
            else:
                messages = [HumanMessage(content=prompt)]
                result = llm_with_tools.invoke(messages)
            
            return result
            
        except Exception as e:
            raise RuntimeError(f"{self.provider} 模型工具调用失败: {e}")
    
    def generate_structured(self, prompt: str, output_schema: type[BaseModel], system_prompt: str = None) -> BaseModel:
        """生成结构化输出"""
        if not self.is_available():
            raise RuntimeError(f"模型 {self.provider} 不可用")
        
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            
            # 对于OpenAI模型，使用function_calling方法
            if self.provider == 'openai':
                llm_with_structured = self.llm.with_structured_output(output_schema, method="function_calling")
            else:
                llm_with_structured = self.llm.with_structured_output(output_schema)
            
            if system_prompt:
                # 使用正确的消息结构
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=prompt)
                ]
                result = llm_with_structured.invoke(messages)
            else:
                messages = [HumanMessage(content=prompt)]
                result = llm_with_structured.invoke(messages)
            
            return result
            
        except Exception as e:
            raise RuntimeError(f"{self.provider} 模型结构化输出失败: {e}")
    
    def test_connection(self) -> Dict[str, Any]:
        """测试模型连接"""
        if not self.is_available():
            return {
                'success': False,
                'error': '模型未初始化或API密钥无效',
                'provider': self.provider,
                'model_name': self.model_name
            }
        
        try:
            # 发送测试请求
            test_prompt = "Hello, this is a test message. Please respond with 'OK'."
            response = self.generate(test_prompt)
            
            return {
                'success': True,
                'response': response,
                'provider': self.provider,
                'model_name': self.model_name
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': self.provider,
                'model_name': self.model_name
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            'provider': self.provider,
            'model_name': self.model_name,
            'base_url': self.base_url,
            'available': self.is_available()
        }