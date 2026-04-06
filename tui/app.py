"""TUI application using Textual"""
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Header, Footer, Input, Static
from textual.binding import Binding

from claude_code.api.client import ClaudeClient
from claude_code.query import QueryEngine
from claude_code.tools.registry import get_all_tools


class ClaudeApp(App):
    """Claude Code TUI Application"""

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=True),
        Binding("ctrl+l", "clear", "Clear", show=True),
    ]

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.anthropic.com",
        model: str = "claude-sonnet-4-20250514",
    ):
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = None
        self.engine = None

    def compose(self) -> ComposeResult:
        """Create the UI layout"""
        yield Header(show_clock=True)
        yield Container(
            VerticalScroll(
                Static("", id="output"),
                id="output-container",
            ),
            Input(placeholder="Type your message...", id="input"),
        )
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the application"""
        # Create API client
        self.client = ClaudeClient(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        # Create query engine
        self.engine = QueryEngine(
            client=self.client,
            model=self.model,
        )

        # Focus input
        self.query_one("#input", Input).focus()

        # Print welcome message
        output = self.query_one("#output", Static)
        output.update(
            "[bold]Claude Code[/bold] - AI CLI Tool\n\n"
            "Type your message and press Enter to start.\n"
            "Type /help for available commands.\n"
            "Press Ctrl+C to quit.\n"
        )

    async def on_input_submit(self, event: Input.Submit) -> None:
        """Handle input submission"""
        input_widget = self.query_one("#input", Input)
        output = self.query_one("#output", Static)

        user_input = event.value.strip()
        if not user_input:
            return

        # Clear input
        input_widget.value = ""

        # Check for commands
        if user_input.startswith("/"):
            await self._handle_command(user_input)
            return

        # Add user message to output
        current_output = output.renderable
        output.update(
            f"{current_output}\n\n[bold]You:[/bold] {user_input}\n\n"
        )

        # Process with Claude
        try:
            # Set tools
            self.engine.tools = get_all_tools()

            # Send message
            await self.engine.chat(user_input)

            # Get last assistant message
            if self.engine.messages and self.engine.messages[-1].role == "assistant":
                response = self.engine.messages[-1].content
                output.update(f"{output.renderable}\n[bold]Claude:[/bold]\n{response}\n")

        except Exception as e:
            output.update(f"{output.renderable}\n[red]Error:[/red] {str(e)}\n")

    async def _handle_command(self, command: str) -> None:
        """Handle slash commands"""
        output = self.query_one("#output", Static)
        cmd = command[1:].split()[0].lower()
        args = command[1:].split()[1:]

        commands = {
            "help": "Available commands:\n"
                    "  /help - Show this help\n"
                    "  /clear - Clear the screen\n"
                    "  /quit - Quit the application",
            "clear": self.action_clear,
            "quit": self.action_quit,
        }

        if cmd in commands:
            if cmd == "clear":
                commands[cmd]()
                output.update("[bold]Claude Code[/bold] - Screen cleared\n")
            elif cmd == "quit":
                commands[cmd]()
            else:
                output.update(f"{output.renderable}\n{commands[cmd]}\n")
        else:
            output.update(f"{output.renderable}\n[red]Unknown command: {cmd}[/red]\n")

    def action_clear(self) -> None:
        """Clear the screen"""
        output = self.query_one("#output", Static)
        output.update("")

    def action_quit(self) -> None:
        """Quit the application"""
        self.exit()