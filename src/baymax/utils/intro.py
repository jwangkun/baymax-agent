def print_intro():
    """Display the welcome screen with clean format."""
    # ANSI color codes
    LIGHT_BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Clear screen effect with some spacing
    print("\n" * 2)
    
    # Welcome message without box formatting
    welcome_text = "Welcome to BayMax"
    print(f"{BOLD}{LIGHT_BLUE}{welcome_text}{RESET}")
    print()
    
    # ASCII art for BAYMAX in block letters (financial terminal style)
    baymax_art = f"""{BOLD}{LIGHT_BLUE}
        BayMax Agent 股票分析
    {RESET}"""
    
    print(baymax_art)
    print()
    print("Your AI assistant for financial analysis.")
    print("Ask me any questions. Type 'exit' or 'quit' to end.")
    print()

