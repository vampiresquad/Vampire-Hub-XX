# assets/banners.py

from rich.text import Text
from rich.console import Console

console = Console() # Use global console for consistent printing if banners are printed directly

def get_normal_banner_rich():
    banner_text = Text()
    banner_text.append("""
 ____   ____  _____  ____  ____  ____  ____  ____   ____  ____  ____
|_  _| |_  _||_   _||_  _||_  _||_  _||_  _||_  _| |_  _||_  _||_  _|
  | |   | |    | |    | |  | |  | |  | |  | |   | |  | |  | |  | |
  | |___| |    | |    | |__| |  | |__| |  | |___| |   | |__| |  | |
 /_  ___  _\\  _|_|_  /________\\ /________\\ /________\\ /________\\
|___||___|  |_____| |________| |________| |________| |________|
""", style="red")
    banner_text.append("""
       _   _   _   _   _   _   _   _   _   _   _
      / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \
     ( V | A | M | P | I | R | E | - | H | U | B )
      \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/
""", style="cyan")
    banner_text.append("""
          [X] Multi-Supported Ethical Hacking Tool [X]
""", style="bold yellow")
    return banner_text

def get_admin_banner_rich():
    banner_text = Text()
    banner_text.append("""
  ____   ____  _____  ____  ____  ____  ____  ____   ____  ____  ____
 |_  _| |_  _||_   _||_  _||_  _||_  _||_  _||_  _| |_  _||_  _||_  _|
   | |   | |    | |    | |  | |  | |  | |  | |   | |  | |  | |  | |
   | |___| |    | |    | |__| |  | |__| |  | |___| |   | |__| |  | |
  /_  ___  _\\  _|_|_  /________\\ /________\\ /________\\ /________\\
 |___||___|  |_____| |________| |________| |________| |________|
""", style="magenta")
    banner_text.append("""
         .d8888b.  888b     d888 88888888888 8888888b.
        d88P  Y88b 8888b   d8888     888     888  "Y88b
        888    888 88888b.d88888     888     888    888
        888        888Y88888P888     888     888    888
        888  88888 888 Y888P 888     888     888    888
        888    888 888  Y8P  888     888     888    888
        Y88b  d88P 888   "   888     888     888  .d88P
         "Y8888P"  888       888     888     8888888P"
""", style="red")
    banner_text.append("""
          [A] Advanced Admin Mode Active [A]
""", style="dim") # Dim style for light black-ish effect
    return banner_text

