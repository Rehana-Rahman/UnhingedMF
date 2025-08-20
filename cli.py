import argparse, os, sys, re
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from .storage import load_history, save_history, load_config, save_config
from .prompts import UNHINGED_SYSTEM_PROMPT
from .core import start_chat, send

console = Console()

PERSONALITIES = {
    "unhinged": "Be extra chaotic, witty, and unserious. Roast lightly, never hateful.",
    "feral": "More energy, more spice, fast one-liners. Keep it playful, not cruel.",
    "sweet": "Tease gently, chaos with heart. Encouraging, but still funny.",
    "sassy": "Eye-roll energy, sarcastic quips, confident and breezy."
}

def build_system_prompt(persona_desc: str) -> str:
    return UNHINGED_SYSTEM_PROMPT + f"\nActive persona: {persona_desc}\n"

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(prog="unhingedmf", description="Unhinged, witty terminal chatbot (Gemini)")
    parser.add_argument("--model", default=None, help="Gemini model name (default from config, e.g., gemini-1.5-flash)")
    parser.add_argument("--reset", action="store_true", help="Wipe chat memory")
    parser.add_argument("--personality", choices=list(PERSONALITIES.keys()), help="Choose the vibe")
    parser.add_argument("--temperature", type=float, help="Creativity (0.0-2.0)")
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        console.print(Panel.fit(
            "[bold red]API key missing[/bold red]\n"
            "Set it via environment variable:\n\n"
            "[bold]Windows (PowerShell):[/bold]  [green]setx GEMINI_API_KEY \"YOUR_KEY\"[/green]\n"
            "[bold]macOS/Linux:[/bold]           [green]export GEMINI_API_KEY=\"YOUR_KEY\"[/green]\n",
            title="Help"
        ))
        sys.exit(1)

    cfg = load_config()
    if args.model: cfg["model"] = args.model
    if args.personality: cfg["personality"] = args.personality
    if args.temperature is not None: cfg["temperature"] = args.temperature
    save_config(cfg)

    if args.reset:
        save_history([])
        console.print("[yellow]Memory wiped. Fresh start.[/yellow]")

    history = load_history()
    persona_desc = PERSONALITIES.get(cfg["personality"], PERSONALITIES["unhinged"])
    system_prompt = build_system_prompt(persona_desc)

    try:
        chat = start_chat(api_key, cfg["model"], system_prompt, history=history, temperature=cfg["temperature"])
    except Exception as e:
        console.print(f"[red]Failed to start chat:[/red] {e}")
        sys.exit(1)

    console.print(Panel("Type your message. Commands: [bold]/reset[/bold], [bold]/persona <name>[/bold], [bold]/quit[/bold].", title="UNHINGEDMF"))

    while True:
        try:
            user = Prompt.ask(Text("You", style="bold cyan")).strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]bye.[/dim]")
            break

        if not user:
            continue

        if user.startswith("/"):
            if user == "/quit":
                console.print("[dim]bye.[/dim]")
                break
            if user == "/reset":
                history = []
                save_history(history)
                try:
                    chat = start_chat(api_key, cfg["model"], system_prompt, history=history, temperature=cfg["temperature"])
                except Exception as e:
                    console.print(f"[red]Reset error:[/red] {e}")
                    continue
                console.print("[yellow]Memory wiped.[/yellow]")
                continue
            m = re.match(r"^/persona\s+(\w+)$", user)
            if m:
                choice = m.group(1).lower()
                if choice in PERSONALITIES:
                    cfg["personality"] = choice
                    save_config(cfg)
                    persona_desc = PERSONALITIES[choice]
                    system_prompt = build_system_prompt(persona_desc)
                    try:
                        chat = start_chat(api_key, cfg["model"], system_prompt, history=load_history(), temperature=cfg["temperature"])
                        console.print(f"[magenta]Persona set to[/magenta] [bold]{choice}[/bold].")
                    except Exception as e:
                        console.print(f"[red]Persona change failed:[/red] {e}")
                else:
                    console.print(f"[red]Unknown persona:[/red] {choice}. Options: {', '.join(PERSONALITIES)}")
                continue
            console.print("[dim]Unknown command.[/dim]")
            continue

        console.print(Text("…thinking", style="dim"))
        try:
            reply = send(chat, user)
        except Exception as e:
            console.print(f"[red]API error:[/red] {e}")
            continue

        history.append({"role": "user", "parts": user})
        history.append({"role": "model", "parts": reply})
        save_history(history)

        console.print(Panel(Text(reply, style="bold white"), title="bot", border_style="magenta"))

if __name__ == "__main__":
    main()
