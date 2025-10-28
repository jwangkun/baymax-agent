# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BayMax Agent is a Python-based AI-powered financial research agent for stock analysis and investment research. It uses LangChain to integrate with multiple LLM providers (DeepSeek, OpenAI, Anthropic, Google Gemini) and provides financial data analysis through tools like AkShare.

## Development Commands

### Environment Setup
```bash
# Create virtual environment with uv (recommended)
uv venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate    # Windows

# Install dependencies
uv pip install -e .

# Alternative with pip
pip install -e .
```

### Running the Application
```bash
# Start interactive CLI
baymax

# Verify installation
baymax --version
```

### Testing
```bash
# Run tests (Note: No test configuration currently exists)
pytest
pytest tests/test_agent.py -v
```

## Architecture Overview

### Core Components

1. **Agent System** (`src/baymax/agent.py`):
   - Task planning and execution with multi-step reasoning
   - Orchestrates financial tools and LLM interactions
   - Safety limits: `max_steps=20` global, `max_steps_per_task=5`

2. **Model Management** (`src/baymax/model.py`, `model_manager.py`):
   - Unified interface for multiple LLM providers
   - Currently focused on DeepSeek with OpenAI compatibility
   - Supports streaming and structured output

3. **Financial Tools** (`src/baymax/tools/`):
   - `financials.py`: Income statements, balance sheets, cash flow statements
   - `filings.py`: SEC filings (10-K, 10-Q, 8-K)
   - `api.py`: API utilities and data fetching
   - Uses AkShare for Chinese market data

4. **CLI Interface** (`src/baymax/cli.py`):
   - Interactive prompt with history support via prompt-toolkit
   - Entry point: `baymax = baymax.cli:main`

### Key Design Patterns

- **Tool Registry**: All tools are registered in `src/baymax/tools/__init__.py`
- **Schema Validation**: Uses Pydantic for structured LLM outputs (`schemas.py`)
- **Progress Indicators**: UI utilities show task progress (`utils/ui.py`)
- **Environment Configuration**: Loads `.env` before any imports in CLI

### Data Flow

1. User query → CLI → Agent
2. Agent plans tasks using LLM with tool descriptions
3. Each task executed with relevant financial tools
4. Results aggregated and analyzed by LLM
5. Final answer presented to user

## Important Configuration

### Environment Variables (`.env`)
```bash
# Required: At least one LLM API key
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
GOOGLE_API_KEY=your-key

# Optional: Custom endpoints
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Dependencies
- Python >=3.10 required
- Uses `uv` for package management
- Key packages: langchain, akshare, prompt-toolkit, pydantic

## Development Notes

- **No test framework configured** - Consider adding pytest configuration
- **No linting setup** - Consider adding black, flake8, or ruff
- **Chinese documentation** - README.md is primarily in Chinese
- **Recent focus** - DeepSeek integration and AkShare data sources
- **Package naming** - Project name "baymax" conflicts with dependency name

## Common Tasks

### Adding New Financial Tools
1. Create tool in `src/baymax/tools/`
2. Register in `src/baymax/tools/__init__.py`
3. Update tool descriptions in agent planning prompts

### Modifying LLM Behavior
- Model configuration: `src/baymax/model.py`
- Prompt templates: `src/baymax/prompts.py`
- Output schemas: `src/baymax/schemas.py`

### Debugging
- Enable debug logging in `src/baymax/utils/logger.py`
- Check `.env` configuration for API keys
- Monitor tool execution in agent loop