import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from datetime import datetime

from storage import HistoryManager, ConfigManager
from personas import PERSONAS
from chat import ChatSession

console = Console()

def format_timestamp():
    return datetime.now().strftime("%H:%M")

def show_welcome():
    welcome = """
    # 🔥 UnhingedMF
    
    Your feral AI companion that talks like a menace.
    
    **Commands:**
    - `/quit` - peace out
    - `/reset` - wipe memory
    - `/persona <name>` - change vibe
    - `/model <name>` - switch model
    """
    console.print(Panel(Markdown(welcome), border_style="magenta", title="[bold]Welcome[/bold]"))

def display_message(role, content, style="white"):
    timestamp = format_timestamp()
    if role == "user":
        console.print(f"\n[dim]{timestamp}[/dim] [bold cyan]You[/bold cyan]")
        console.print(f"  {content}")
    else:
        console.print(f"\n[dim]{timestamp}[/dim] [bold magenta]UnhingedMF[/bold magenta]")
        console.print(Panel(content, border_style="magenta", padding=(0, 2)))

def main():
    parser = argparse.ArgumentParser(prog="unhingedmf")
    parser.add_argument("--model", help="Override model name")
    parser.add_argument("--persona", choices=list(PERSONAS.keys()), help="Set personality")
    parser.add_argument("--temp", type=float, help="Temperature (0.0-2.0)")
    parser.add_argument("--reset", action="store_true", help="Clear chat history")
    args = parser.parse_args()

    config = ConfigManager()
    history = HistoryManager()

    if args.reset:
        history.clear()
        console.print("[yellow]Memory wiped clean.[/yellow]")
        return

    if args.model:
        config.set("model", args.model)
    if args.persona:
        config.set("persona", args.persona)
    if args.temp is not None:
        config.set("temperature", args.temp)

    show_welcome()

    try:
        session = ChatSession(
            model=config.get("model"),
            persona=config.get("persona"),
            temperature=config.get("temperature"),
            history=history.load()
        )
    except Exception as e:
        console.print(f"[bold red]Failed to initialize:[/bold red] {e}")
        console.print("\n[yellow]Make sure your API key is set:[/yellow]")
        console.print("  export GEMINI_API_KEY='your-key-here'")
        sys.exit(1)

    while True:
        try:
            user_input = Prompt.ask(f"\n[bold cyan]You[/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]later ✌️[/dim]")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            cmd_parts = user_input[1:].split(maxsplit=1)
            cmd = cmd_parts[0].lower()
            arg = cmd_parts[1] if len(cmd_parts) > 1 else None

            if cmd == "quit":
                console.print("[dim]peace out ✌️[/dim]")
                break

            elif cmd == "reset":
                history.clear()
                session.reset()
                console.print("[yellow]Memory cleared. Fresh start.[/yellow]")
                continue

            elif cmd == "persona":
                if arg and arg in PERSONAS:
                    config.set("persona", arg)
                    session.change_persona(arg)
                    console.print(f"[magenta]Switched to {arg} mode[/magenta]")
                else:
                    options = ", ".join(PERSONAS.keys())
                    console.print(f"[red]Unknown persona.[/red] Try: {options}")
                continue

            elif cmd == "model":
                if arg:
                    config.set("model", arg)
                    session.change_model(arg)
                    console.print(f"[green]Model changed to {arg}[/green]")
                else:
                    console.print("[red]Specify a model name[/red]")
                continue

            else:
                console.print("[dim]Unknown command[/dim]")
                continue

        with Live(Spinner("dots", text="[dim]thinking...[/dim]"), console=console, transient=True):
            try:
                response = session.send(user_input)
            except Exception as e:
                console.print(f"[red]Error:[/red] {e}")
                continue

        history.append("user", user_input)
        history.append("model", response)

        display_message("bot", response)

if __name__ == "__main__":
    main()
