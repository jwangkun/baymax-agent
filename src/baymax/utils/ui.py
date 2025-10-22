import sys
import time
import threading
from contextlib import contextmanager
from typing import Optional, Callable
from functools import wraps


class Colors:
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    WHITE = "\033[97m"
    LIGHT_BLUE = "\033[94m"  # Same as BAYMAX ASCII art


class Spinner:
    """An animated spinner that runs in a separate thread."""
    
    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self, message: str = "", color: str = Colors.CYAN):
        self.message = message
        self.color = color
        self.running = False
        self.thread: Optional[threading.Thread] = None
        
    def _animate(self):
        """Animation loop that runs in a separate thread."""
        idx = 0
        while self.running:
            frame = self.FRAMES[idx % len(self.FRAMES)]
            sys.stdout.write(f"\r{self.color}{frame}{Colors.ENDC} {self.message}")
            sys.stdout.flush()
            time.sleep(0.08)
            idx += 1
    
    def start(self):
        """Start the spinner animation."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._animate, daemon=True)
            self.thread.start()
    
    def stop(self, final_message: str = "", symbol: str = "✓", symbol_color: str = Colors.GREEN):
        """Stop the spinner and optionally show a completion message."""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
            # Clear the line
            sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
            if final_message:
                print(f"{symbol_color}{symbol}{Colors.ENDC} {final_message}")
            sys.stdout.flush()
    
    def update_message(self, message: str):
        """Update the spinner message."""
        self.message = message


def show_progress(message: str, success_message: str = ""):
    """Decorator to show progress spinner while a function executes."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            spinner = Spinner(message, color=Colors.CYAN)
            spinner.start()
            try:
                # 添加超时保护
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError(f"{message} 操作超时")
                
                # 设置45秒超时
                old_handler = signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(45)
                
                try:
                    result = func(*args, **kwargs)
                    signal.alarm(0)  # 取消超时
                    spinner.stop(success_message or message.replace("...", " ✓"), symbol="✓", symbol_color=Colors.GREEN)
                    return result
                except TimeoutError as te:
                    signal.alarm(0)  # 取消超时
                    spinner.stop(f"超时: {str(te)}", symbol="⏱", symbol_color=Colors.YELLOW)
                    raise
                finally:
                    signal.signal(signal.SIGALRM, old_handler)
                    
            except Exception as e:
                spinner.stop(f"失败: {str(e)}", symbol="✗", symbol_color=Colors.RED)
                raise
        return wrapper
    return decorator


class UI:
    """Interactive UI for displaying agent progress and results."""
    
    def __init__(self):
        self.current_spinner: Optional[Spinner] = None
        
    @contextmanager
    def progress(self, message: str, success_message: str = ""):
        """Context manager for showing progress with a spinner."""
        spinner = Spinner(message, color=Colors.CYAN)
        self.current_spinner = spinner
        spinner.start()
        try:
            yield spinner
            spinner.stop(success_message or message.replace("...", " ✓"), symbol="✓", symbol_color=Colors.GREEN)
        except Exception as e:
            spinner.stop(f"Failed: {str(e)}", symbol="✗", symbol_color=Colors.RED)
            raise
        finally:
            self.current_spinner = None
    
    def print_header(self, text: str):
        """Print a section header."""
        print(f"\n{Colors.BOLD}{Colors.BLUE}╭─ {text}{Colors.ENDC}")
    
    def print_user_query(self, query: str):
        """Print the user's query in the same style as DEXTER ASCII art."""
        print(f"\n{Colors.BOLD}{Colors.LIGHT_BLUE}You: {query}{Colors.ENDC}\n")
    
    def print_task_list(self, tasks):
        """Print a clean list of planned tasks."""
        if not tasks:
            return
        self.print_header("Planned Tasks")
        for i, task in enumerate(tasks):
            status = "+"
            color = Colors.DIM
            desc = task.get('description', task)
            print(f"{Colors.BLUE}│{Colors.ENDC} {color}{status}{Colors.ENDC} {desc}")
        print(f"{Colors.BLUE}╰{'─' * 50}{Colors.ENDC}\n")
    
    def print_task_start(self, task_desc: str):
        """Print when starting a task."""
        print(f"\n{Colors.BOLD}{Colors.CYAN}▶ Task:{Colors.ENDC} {task_desc}")
    
    def print_task_done(self, task_desc: str):
        """Print when a task is completed."""
        print(f"{Colors.GREEN}  ✓ Completed{Colors.ENDC} {Colors.DIM}│ {task_desc}{Colors.ENDC}")
    
    def print_tool_run(self, tool_name: str, args: str = ""):
        """Print when a tool is executed."""
        args_display = f" {Colors.DIM}({args[:50]}...){Colors.ENDC}" if args and len(args) > 0 else ""
        print(f"  {Colors.YELLOW}⚡{Colors.ENDC} {tool_name}{args_display}")
    
    def print_answer(self, answer: str):
        """Print the final answer as a Markdown report."""
        width = 80
        
        # Top border
        print(f"\n{Colors.BOLD}{Colors.BLUE}╔{'═' * (width - 2)}╗{Colors.ENDC}")
        
        # Title
        title = "ANALYSIS REPORT"
        padding = (width - len(title) - 2) // 2
        print(f"{Colors.BOLD}{Colors.BLUE}║{' ' * padding}{title}{' ' * (width - len(title) - padding - 2)}║{Colors.ENDC}")
        
        # Separator
        print(f"{Colors.BLUE}╠{'═' * (width - 2)}╣{Colors.ENDC}")
        
        # Convert answer to Markdown format
        markdown_answer = self._format_as_markdown(answer)
        
        # Answer content with proper line wrapping
        print(f"{Colors.BLUE}║{Colors.ENDC}{' ' * (width - 2)}{Colors.BLUE}║{Colors.ENDC}")
        for line in markdown_answer.split('\n'):
            if len(line) == 0:
                print(f"{Colors.BLUE}║{Colors.ENDC}{' ' * (width - 2)}{Colors.BLUE}║{Colors.ENDC}")
            else:
                # Word wrap long lines
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 <= width - 6:
                        current_line += word + " "
                    else:
                        if current_line:
                            print(f"{Colors.BLUE}║{Colors.ENDC} {current_line.ljust(width - 4)} {Colors.BLUE}║{Colors.ENDC}")
                        current_line = word + " "
                if current_line:
                    print(f"{Colors.BLUE}║{Colors.ENDC} {current_line.ljust(width - 4)} {Colors.BLUE}║{Colors.ENDC}")
        
        print(f"{Colors.BLUE}║{Colors.ENDC}{' ' * (width - 2)}{Colors.BLUE}║{Colors.ENDC}")
        
        # Bottom border
        print(f"{Colors.BOLD}{Colors.BLUE}╚{'═' * (width - 2)}╝{Colors.ENDC}\n")
        
        # Also print the raw markdown for easy copying
        print(f"{Colors.DIM}--- Markdown Report ---{Colors.ENDC}")
        print(f"{Colors.DIM}{markdown_answer}{Colors.ENDC}")
        print(f"{Colors.DIM}-----------------------{Colors.ENDC}\n")
    
    def _format_as_markdown(self, text: str) -> str:
        """Convert plain text to Markdown format with proper structure."""
        lines = text.split('\n')
        markdown_lines = []
        
        # Add a title with timestamp
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        markdown_lines.append("# 📊 股票分析报告")
        markdown_lines.append(f"*生成时间: {current_time}*")
        markdown_lines.append("")
        
        current_section = None
        in_list = False
        in_table = False
        paragraph_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                if in_list:
                    markdown_lines.append("")  # End list
                    in_list = False
                elif paragraph_lines:
                    # End of paragraph
                    markdown_lines.append(" ".join(paragraph_lines))
                    markdown_lines.append("")
                    paragraph_lines = []
                continue
            
            # Check if this is a section header
            if any(keyword in stripped.lower() for keyword in ['结论', '总结', '建议', '分析', '风险', '机会', '数据', '表现', '趋势', '预测']):
                if in_list:
                    markdown_lines.append("")  # End list
                    in_list = False
                elif paragraph_lines:
                    # End of paragraph
                    markdown_lines.append(" ".join(paragraph_lines))
                    markdown_lines.append("")
                    paragraph_lines = []
                
                # Format as a section header with emoji
                section = stripped
                emoji_map = {
                    '结论': '📌',
                    '总结': '📝',
                    '建议': '💡',
                    '分析': '🔍',
                    '风险': '⚠️',
                    '机会': '🚀',
                    '数据': '📈',
                    '表现': '📊',
                    '趋势': '📉',
                    '预测': '🔮'
                }
                
                # Find matching emoji
                emoji = ''
                for key, val in emoji_map.items():
                    if key in section:
                        emoji = val
                        break
                
                markdown_lines.append(f"## {emoji} {section}")
                markdown_lines.append("")
                current_section = section
                continue
            
            # Check if this looks like a list item
            if stripped.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                if paragraph_lines:
                    # End of paragraph
                    markdown_lines.append(" ".join(paragraph_lines))
                    markdown_lines.append("")
                    paragraph_lines = []
                
                if not in_list:
                    markdown_lines.append("")  # Start list
                    in_list = True
                
                # Format as a list item
                if stripped[0].isdigit():
                    # Numbered list
                    markdown_lines.append(f"{stripped}")
                else:
                    # Bullet list with emoji if appropriate
                    content = stripped[1:].strip()
                    if '建议' in content or '推荐' in content:
                        markdown_lines.append(f"- 💡 {content}")
                    elif '风险' in content or '注意' in content:
                        markdown_lines.append(f"- ⚠️ {content}")
                    elif '机会' in content or '利好' in content:
                        markdown_lines.append(f"- 🚀 {content}")
                    else:
                        markdown_lines.append(f"- {content}")
                continue
            
            # Check if this looks like data (contains numbers and %)
            if any(char.isdigit() for char in stripped) and ('%' in stripped or '元' in stripped or '亿' in stripped):
                if paragraph_lines:
                    # End of paragraph
                    markdown_lines.append(" ".join(paragraph_lines))
                    markdown_lines.append("")
                    paragraph_lines = []
                
                if in_list:
                    markdown_lines.append("")  # End list
                    in_list = False
                
                # Format as data point with emoji
                if '%' in stripped:
                    markdown_lines.append(f"📊 **{stripped}**")
                elif '元' in stripped:
                    markdown_lines.append(f"💰 **{stripped}**")
                elif '亿' in stripped:
                    markdown_lines.append(f"📈 **{stripped}**")
                else:
                    markdown_lines.append(f"📋 **{stripped}**")
                continue
            
            # Regular paragraph - collect lines
            if in_list:
                markdown_lines.append("")  # End list
                in_list = False
            
            paragraph_lines.append(stripped)
        
        # Handle any remaining paragraph
        if paragraph_lines:
            markdown_lines.append(" ".join(paragraph_lines))
            markdown_lines.append("")
        
        # Add a footer with more information
        markdown_lines.append("---")
        markdown_lines.append("*🤖 此报告由 BayMax Agent 自动生成*")
        markdown_lines.append("*📡 数据来源: 公开市场信息*")
        markdown_lines.append("*⚠️ 投资有风险，入市需谨慎*")
        
        return '\n'.join(markdown_lines)
    
    def print_info(self, message: str):
        """Print an info message."""
        print(f"{Colors.DIM}{message}{Colors.ENDC}")
    
    def print_error(self, message: str):
        """Print an error message."""
        print(f"{Colors.RED}✗ Error:{Colors.ENDC} {message}")
    
    def print_warning(self, message: str):
        """Print a warning message."""
        print(f"{Colors.YELLOW}⚠ Warning:{Colors.ENDC} {message}")

