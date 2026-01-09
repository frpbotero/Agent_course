"""
Chat module - Terminal interface for the RAG Agent.
Handles user interaction via command line.
"""

import sys
from agent import Agent
from tools import ingest, ingest_file, search


# ANSI colors for terminal output
class Colors:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_colored(text: str, color: str = Colors.RESET) -> None:
    """Print text with color."""
    print(f"{color}{text}{Colors.RESET}")


def print_help() -> None:
    """Print help message with available commands."""
    help_text = """
╔══════════════════════════════════════════════════════════════╗
║                    Comandos Disponíveis                       ║
╠══════════════════════════════════════════════════════════════╣
║  /ingest <texto>      - Ingere texto na base de conhecimento ║
║  /ingest_file <path>  - Ingere arquivo na base               ║
║  /search <query>      - Busca direta na base (sem chat)      ║
║  /clear               - Limpa histórico da conversa          ║
║  /help                - Mostra esta mensagem                 ║
║  /exit ou /quit       - Sair do chat                         ║
╚══════════════════════════════════════════════════════════════╝
"""
    print_colored(help_text, Colors.CYAN)


def handle_command(command: str, args: str, agent: Agent) -> bool:
    """
    Handle special commands.
    
    Returns:
        True if the program should continue, False if it should exit
    """
    command = command.lower()
    
    if command in ["/exit", "/quit"]:
        print_colored("\n👋 Até mais!", Colors.YELLOW)
        return False
    
    elif command == "/help":
        print_help()
    
    elif command == "/clear":
        agent.clear_history()
        print_colored("✓ Histórico limpo.", Colors.GREEN)
    
    elif command == "/ingest":
        if not args:
            print_colored("❌ Erro: Forneça o texto para ingerir.", Colors.RED)
        else:
            print_colored("⏳ Ingerindo texto...", Colors.YELLOW)
            result = ingest(args)
            if result["status"] == "success":
                print_colored(f"✓ {result['message']} ({result['text_length']} caracteres)", Colors.GREEN)
            else:
                print_colored(f"❌ Erro: {result['message']}", Colors.RED)
    
    elif command == "/ingest_file":
        if not args:
            print_colored("❌ Erro: Forneça o caminho do arquivo.", Colors.RED)
        else:
            print_colored(f"⏳ Ingerindo arquivo: {args}...", Colors.YELLOW)
            result = ingest_file(args.strip())
            if result["status"] == "success":
                print_colored(f"✓ {result['message']} - {result['source']} ({result['text_length']} caracteres)", Colors.GREEN)
            else:
                print_colored(f"❌ Erro: {result['message']}", Colors.RED)
    
    elif command == "/search":
        if not args:
            print_colored("❌ Erro: Forneça a query de busca.", Colors.RED)
        else:
            print_colored("⏳ Buscando...", Colors.YELLOW)
            results = search(args, top_k=5)
            if results:
                print_colored(f"\n📚 {len(results)} resultado(s) encontrado(s):\n", Colors.GREEN)
                for i, result in enumerate(results, 1):
                    source = f" ({result['source']})" if result.get('source') else ""
                    similarity = f"{result['similarity']:.2%}"
                    print_colored(f"[{i}] {similarity}{source}", Colors.CYAN)
                    print(f"    {result['text'][:200]}{'...' if len(result['text']) > 200 else ''}\n")
            else:
                print_colored("Nenhum resultado encontrado.", Colors.YELLOW)
    
    else:
        print_colored(f"❌ Comando desconhecido: {command}", Colors.RED)
        print_colored("Digite /help para ver os comandos disponíveis.", Colors.YELLOW)
    
    return True


def main():
    """Main chat loop."""
    print_colored("""
╔══════════════════════════════════════════════════════════════╗
║              🤖 Agente RAG - Chat Console                    ║
║                                                              ║
║   Digite sua pergunta ou use comandos com /                  ║
║   Digite /help para ver os comandos disponíveis              ║
╚══════════════════════════════════════════════════════════════╝
""", Colors.BOLD + Colors.CYAN)
    
    # Initialize agent
    agent = Agent()
    
    while True:
        try:
            # Get user input
            user_input = input(f"{Colors.GREEN}Você: {Colors.RESET}").strip()
            
            if not user_input:
                continue
            
            # Check if it's a command
            if user_input.startswith("/"):
                parts = user_input.split(" ", 1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                
                if not handle_command(command, args, agent):
                    break
                continue
            
            # Regular chat - process with RAG
            print_colored("⏳ Pensando...", Colors.YELLOW)
            
            response = agent.process(user_input)
            
            # Clear "Pensando..." line and print response
            print(f"\033[A\033[K", end="")  # Move up and clear line
            print_colored(f"\n🤖 Agente: {Colors.RESET}{response}\n", Colors.BLUE)
            
        except KeyboardInterrupt:
            print_colored("\n\n👋 Até mais!", Colors.YELLOW)
            break
        except Exception as e:
            print_colored(f"\n❌ Erro: {str(e)}", Colors.RED)
            continue


if __name__ == "__main__":
    main()
