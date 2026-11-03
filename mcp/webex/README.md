# Serveur MCP Webex (bot)

Un serveur MCP minimal, écrit avec [FastMCP](https://gofastmcp.com) et géré avec [uv](https://docs.astral.sh/uv/). Il expose un seul outil :

| Outil | Paramètre | Ce qu'il fait |
|---|---|---|
| `send_webex_message` | `message` | Publie `message` (Markdown accepté) dans l'espace Webex configuré |

C'est l'approche « production » évoquée à l'[étape 3](../../README.md#valider-chaque-envoi-avant-quil-parte) : l'espace et le bot sont fixés dans la configuration, seul le contenu du message varie. Le modèle ne peut ni choisir un autre espace, ni écrire en votre nom.

## Prérequis

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Un bot Webex : sur [developer.webex.com](https://developer.webex.com), **My Webex Apps**, puis **Create a Bot**. Notez son token d'accès.
- Le bot ajouté comme membre de l'espace cible.

## Configuration

```bash
cd mcp/webex
cp .env.example .env
```

Renseignez ensuite dans `.env` :

- `WEBEX_BOT_TOKEN` : le token du bot ;
- `WEBEX_ROOM_ID` : l'identifiant de l'espace (par exemple récupéré avec le prompt de lecture de l'étape 3) ;
- `MCP_AUTH_TOKEN` : le token que les clients MCP devront présenter. Générez-le avec `openssl rand -hex 32` ;
- `MCP_HOST` et `MCP_PORT` (facultatifs) : l'adresse d'écoute, `127.0.0.1:8000` par défaut.

> [!IMPORTANT]
> Le fichier `.env` est ignoré par git. Ne commitez jamais le token du bot ni le token MCP.

## Lancer le serveur

```bash
uv run server.py
```

Le serveur écoute en HTTP (transport *streamable HTTP*) sur `http://127.0.0.1:8000/mcp`. Toute requête sans `Authorization: Bearer <MCP_AUTH_TOKEN>` est refusée avec un `401`.

> [!WARNING]
> Sans ce token, n'importe qui connaissant l'URL pourrait publier dans votre espace au nom du bot. Ne l'exposez jamais sans authentification.

## L'exposer avec Cloudflare

Le serveur écoute sur `127.0.0.1` : il n'est joignable que depuis la machine. Un [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) le publie en HTTPS sans ouvrir de port :

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

Cette commande crée un tunnel temporaire en `https://<nom-aleatoire>.trycloudflare.com`. Pour une URL stable, utilisez un tunnel nommé rattaché à votre domaine.

L'URL du serveur MCP est alors `https://<votre-domaine>/mcp`.

## Le brancher sur un client MCP

**Mistral Vibe** : créez un connecteur personnalisé comme à l'[étape 0](../../README.md#étape-0--préparer-mistral-vibe), avec :

- Serveur : `https://<votre-domaine>/mcp`
- Authentification : *Authentification par token API*
- Bearer : la valeur de `MCP_AUTH_TOKEN`

**Claude Code**

```bash
claude mcp add --transport http webex-bot https://<votre-domaine>/mcp --header "Authorization: Bearer <TOKEN_MCP>"
```

## Si ça coince

| Ce que vous voyez | Cause probable | Ce qu'il faut faire |
|---|---|---|
| `KeyError: 'WEBEX_BOT_TOKEN'` ou `'MCP_AUTH_TOKEN'` | `.env` absent ou incomplet | Copiez `.env.example` en `.env` et remplissez-le |
| `401 Unauthorized` sur `/mcp` | Le client n'envoie pas le bon `MCP_AUTH_TOKEN` | Vérifiez le header `Authorization: Bearer …` du client |
| `Erreur API Webex 401` | Token du bot invalide | Régénérez-le dans **My Webex Apps** |
| `Erreur API Webex 404` « Could not find a room » | Le bot n'est pas membre de l'espace, ou l'ID est faux | Ajoutez le bot à l'espace et vérifiez `WEBEX_ROOM_ID` |
