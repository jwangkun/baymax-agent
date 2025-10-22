import os
from typing import List, Dict, Any, Optional
from baymax.model import Model

class ModelManager:
    """模型管理器，负责管理和切换不同的AI模型"""
    
    def __init__(self):
        self.models = {}
        self.current_model_name = None
        self._initialize_models()
    
    def _initialize_models(self):
        """初始化所有可用的模型"""
        # DeepSeek 模型 (使用OpenAI兼容接口)
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
        deepseek_base_url = os.getenv("DEEPSEEK_BASE_URL") or os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
        if deepseek_api_key:
            self.models["deepseek"] = Model(
                provider="openai",  # DeepSeek使用OpenAI兼容接口
                api_key=deepseek_api_key,
                model_name=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
                base_url=deepseek_base_url
            )
        
        # OpenAI 模型
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_base_url = os.getenv("OPENAI_BASE_URL")
        if openai_api_key and not deepseek_api_key:  # 避免重复配置
            self.models["openai"] = Model(
                provider="openai",
                api_key=openai_api_key,
                model_name=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                base_url=openai_base_url
            )
        
        # Google Gemini 模型
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key:
            self.models["gemini"] = Model(
                provider="gemini",
                api_key=gemini_api_key,
                model_name=os.getenv("GEMINI_MODEL", "gemini-pro")
            )
        
        # Anthropic Claude 模型
        claude_api_key = os.getenv("CLAUDE_API_KEY")
        claude_base_url = os.getenv("CLAUDE_BASE_URL")
        if claude_api_key:
            self.models["claude"] = Model(
                provider="claude",
                api_key=claude_api_key,
                model_name=os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229"),
                base_url=claude_base_url
            )
        
        # 设置默认模型 - 优先使用DeepSeek
        if "deepseek" in self.models:
            self.current_model_name = "deepseek"
        elif "openai" in self.models:
            self.current_model_name = "openai"
        elif "gemini" in self.models:
            self.current_model_name = "gemini"
        elif "claude" in self.models:
            self.current_model_name = "claude"
    
    def get_available_models(self) -> List[str]:
        """获取所有可用的模型名称"""
        return [name for name, model in self.models.items() if model.is_available()]
    
    def get_current_model(self) -> Optional[Model]:
        """获取当前使用的模型"""
        if self.current_model_name and self.current_model_name in self.models:
            return self.models[self.current_model_name]
        return None
    
    def set_current_model(self, model_name: str) -> bool:
        """设置当前使用的模型"""
        if model_name in self.models and self.models[model_name].is_available():
            self.current_model_name = model_name
            return True
        return False
    
    def get_model_info(self, model_name: str = None) -> Dict[str, Any]:
        """获取模型信息"""
        if model_name is None:
            model_name = self.current_model_name
        
        if model_name and model_name in self.models:
            return self.models[model_name].get_model_info()
        return {}
    
    def test_model(self, model_name: str) -> Dict[str, Any]:
        """测试指定模型的连接"""
        if model_name in self.models:
            return self.models[model_name].test_connection()
        return {"success": False, "error": f"模型 {model_name} 不存在"}
    
    def test_all_models(self) -> Dict[str, Dict[str, Any]]:
        """测试所有模型的连接"""
        results = {}
        for name, model in self.models.items():
            results[name] = model.test_connection()
        return results