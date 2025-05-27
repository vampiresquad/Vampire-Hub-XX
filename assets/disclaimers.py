# assets/disclaimers.py

from rich.text import Text

def get_normal_disclaimer_rich():
    disclaimer_text = Text()
    disclaimer_text.append("Disclaimer:", style="bold green")
    disclaimer_text.append(" This tool is intended for ethical use only. Unauthorized access or malicious activities are strictly prohibited. The developer is not responsible for any misuse. Use at your own risk.", style="green")
    return disclaimer_text

def get_admin_disclaimer_rich():
    disclaimer_text = Text()
    disclaimer_text.append("Admin Disclaimer:", style="bold red")
    disclaimer_text.append(" You are entering a highly privileged mode. All actions taken here are extremely powerful. Ensure you have explicit authorization for any operations. Misuse can lead to severe legal consequences. Proceed with extreme caution.", style="red")
    return disclaimer_text
