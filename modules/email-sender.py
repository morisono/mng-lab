import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import yaml
from typing import Optional, List
import typer

app = typer.Typer()

def send_email(sender_email: str, password: str, recipient_email: str, subject: str, body: str, smtp_server: str, smtp_port: int, verbose: bool):
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    try:
        server.login(sender_email, password)

        if verbose:
            typer.echo(f"Sender's Email: {sender_email}")
            typer.echo(f"Recipient's Email: {recipient_email}")
            typer.echo(f"Subject: {subject}")
            typer.echo(f"SMTP Server: {smtp_server}")
            typer.echo(f"SMTP Port: {smtp_port}")


        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        body_text = MIMEText(body, "plain")
        message.attach(body_text)

        server.sendmail(sender_email, recipient_email, message.as_string())
        typer.echo("Email sent successfully!")

    except smtplib.SMTPAuthenticationError as e:
        typer.echo(f"Authentication failed: {e}")

    except smtplib.SMTPException as e:
        typer.echo(f"An error occurred while sending the email: {e}")

    finally:
        server.quit()

def load_config():
    try:
        with open("config.yml", "r") as file:
            config = yaml.safe_load(file)
            return config.get("preset_addresses", [])
    except FileNotFoundError:
        return []

def get_sender_info(config: List[str]) -> Optional[str]:
    try:
        choices = config
        message = 'Select the sender email address (Ctrl-D to quit):'
        print(message)
        print("\n".join([f"{i+1}. {email}" for i, email in enumerate(choices)]))
        sender_index = int(input("Enter the number corresponding to the sender email: ")) - 1

        if 0 <= sender_index < len(choices):
            sender_email = choices[sender_index]
            return sender_email
        else:
            print("Invalid input. Please enter a valid number.")
            return get_sender_info(config)

    except EOFError:
        return None  # User pressed Ctrl-D

def read_template(template_file: str, params: dict) -> str:
    with open(template_file, "r") as file:
        content = file.read()

    # Split content into front matter and body
    front_matter_end = content.find("---", 3)
    if front_matter_end != -1:
        front_matter = content[3:front_matter_end].strip()
        body = content[front_matter_end+3:].strip()
    else:
        front_matter = ""
        body = content.strip()

    # Parse YAML front matter
    front_matter_params = yaml.safe_load(front_matter)

    # Merge parameters from YAML front matter and input parameters
    merged_params = {**params, **front_matter_params}

    # Replace placeholders in the body
    for key, value in merged_params.items():
        body = body.replace("{" + key + "}", str(value))

    return body


def select_email_address(message: str, choices: List[str]) -> str:
    print(message)
    for i, choice in enumerate(choices, start=1):
        print(f"{i}. {choice}")

    while True:
        try:
            choice_index = int(input("Enter the number corresponding to the email address: ")) - 1
            if 0 <= choice_index < len(choices):
                return choices[choice_index]
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

@app.command()
def main(
    subject: str = typer.Argument(..., help="Email subject"),
    body: str = typer.Argument(..., help="Email body"),
    template: Optional[str] = typer.Option(None, "--template", help="Email template"),
    schedule: Optional[str] = typer.Option(None, "--schedule", help="Email schedule"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show verbose information"),
    signature: Optional[str] = typer.Option(None, "--signature", help="Email signature"),
):
    config = load_config()

    if verbose:
        print("Active sender email addresses:")
        for sender_email in config:
            print(f"- {sender_email}")

    while True:
        sender_email = get_sender_info(config)
        if sender_email is None:
            break  # User pressed Ctrl-D, exit the program

        smtp_settings = config.get("smtp_settings", {})

        sender_name = sender_email.split('@')[0]  # Extract sender name from email address

        recipient_email = select_email_address("Select the recipient email address:", config)
        if recipient_email is None:
            break  # User pressed Ctrl-D, exit the program

        if verbose:
            print(f"Sender Email: {sender_email}")
            print(f"Recipient Email: {recipient_email}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")
            if template:
                print(f"Template: {template}")
            print("\nSending email...\n")

        if signature:
            body += f"\n\nSignature: {signature}"

        if template:
            template_params = {
                "recipient_name": recipient_email.split('@')[0],
                "sender_name": sender_name,
                # add other template parameters as needed
            }
            template_content = read_template(template, template_params)
            body += f"\n\nTemplate:\n{template_content}"

        if schedule:
            print(f"Scheduled email will be sent on: {schedule}")

        password = getpass.getpass("Enter the sender's email password: ")

        send_email(
            sender_email,
            password,
            recipient_email,
            subject,
            body,
            smtp_server,
            smtp_port,
            verbose,
        )

if __name__ == "__main__":
    app()
