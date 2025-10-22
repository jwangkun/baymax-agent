#!/bin/bash

# BayMax Agent 启动脚本
# 使用当前Python环境运行baymax

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 运行baymax CLI
python -m baymax.cli "$@"