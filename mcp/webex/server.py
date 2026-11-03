import os

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

WEBEX_BOT_TOKEN = os.environ["WEBEX_BOT_TOKEN"]
WEBEX_ROOM_ID = os.environ["WEBEX_ROOM_ID"]
WEBEX_API_URL = "https://webexapis.com/v1/messages"

# Token que les clients MCP doivent envoyer en "Authorization: Bearer <MCP_AUTH_TOKEN>"
MCP_AUTH_TOKEN = os.environ["MCP_AUTH_TOKEN"]
MCP_HOST = os.environ.get("MCP_HOST", "127.0.0.1")
MCP_PORT = int(os.environ.get("MCP_PORT", "8000"))

auth = StaticTokenVerifier(tokens={MCP_AUTH_TOKEN: {"client_id": "mcp-client", "scopes": []}})
mcp = FastMCP("webex", auth=auth)


@mcp.tool
def send_webex_message(message: str) -> str:
    """Envoie un message dans l'espace Webex configuré. Le Markdown est accepté."""
    response = httpx.post(
        WEBEX_API_URL,
        headers={"Authorization": f"Bearer {WEBEX_BOT_TOKEN}"},
        json={"roomId": WEBEX_ROOM_ID, "markdown": message},
        timeout=15,
    )
    if response.is_error:
        return f"Erreur API Webex {response.status_code}: {response.text}"
    return f"Message envoyé (id : {response.json().get('id')})"


if __name__ == "__main__":
    mcp.run(transport="http", host=MCP_HOST, port=MCP_PORT)
