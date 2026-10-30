# Lab M'Ambassadeurs : ThousandEyes, Meraki et Webex dans Mistral Vibe

Dans ce lab, on branche trois serveurs MCP Cisco sur Mistral Vibe avec un simple compte gratuit, puis on les interroge en français, comme on parlerait à un collègue.

Comptez environ 45 minutes :

| Étape | Contenu | Durée |
|---|---|---|
| 0 | Préparer Mistral Vibe | 5 min |
| 1 | ThousandEyes | 10 min |
| 2 | Meraki | 10 min |
| 3 | Webex Messaging | 15 min |
| 4 | Les trois ensemble | 5 min |

> [!IMPORTANT]
> Ce dépôt ne contient aucun token ni aucune clé API. L'animateur vous les donne le jour du lab. Quand vous voyez `<...>` dans le guide, remplacez-le par la valeur qu'il vous a remise.

> [!TIP]
> Vous préférez un autre outil ? Si vous avez déjà vos habitudes avec Claude Code, Codex, Cursor ou VS Code, gardez-les. Les trois serveurs MCP sont des endpoints HTTP standards et marchent avec n'importe quel client MCP. Seule l'interface change, pas les URL ni les tokens. Quelques exemples sont donnés à la fin du guide, dans [Utiliser un autre client MCP](#utiliser-un-autre-client-mcp).

## Les endpoints

| Service | URL |
|---|---|
| ThousandEyes | `https://api.thousandeyes.com/mcp` |
| Meraki | `https://mcp.meraki.com/mcp` |
| Webex Messaging | `https://mcp.webexapis.com/mcp/webex-messaging` |

## Ce qu'il vous faut

- [ ] Un compte gratuit Mistral AI pour accéder à Mistral Vibe ([chat.mistral.ai](https://chat.mistral.ai)). Un navigateur suffit.
- [ ] Un token ThousandEyes qui a la permission *API Access*. Il est fourni pour le lab.
- [ ] Une clé API Meraki Dashboard. Elle est aussi fournie.
- [ ] Un compte Webex, et une intégration OAuth créée depuis votre profil [developer.webex.com](https://developer.webex.com).
- [ ] Un espace Webex de test sans rien de sensible dedans, par exemple « M'Ambassadeurs ».

## Schéma du lab

<img width="901" height="455" alt="Schéma du lab" src="https://github.com/user-attachments/assets/b91a5adb-8fa4-4853-b6d4-818e7c773060" />

---

## Étape 0 : préparer Mistral Vibe

1. Connectez-vous sur [chat.mistral.ai](https://chat.mistral.ai).
2. Dans le menu de gauche, ouvrez **Contexte**, puis **Connecteurs**.
3. Cliquez sur **Nouveau connecteur**, puis sur **Nouveau connecteur personnalisé**.

Pour chaque serveur, Mistral vous demande trois informations :

- **Un nom**, par exemple `ThousandEyes`, `Meraki` ou `Webex-Messaging`.
- **L'URL du serveur MCP**.
- **La méthode d'authentification**, soit un token (`Authorization: Bearer <TOKEN>`), soit OAuth.

---

## Étape 1 : ThousandEyes

### Créer le connecteur

1. Allez dans **Contexte**, puis **Connecteurs**, puis **Nouveau connecteur**, puis **Nouveau connecteur personnalisé**.
2. Remplissez :
   - Nom : `ThousandEyes`
   - Serveur : `https://api.thousandeyes.com/mcp`
   - Authentification : *Authentification par token API*
   - Bearer : `<TOKEN_THOUSANDEYES>`
3. Enregistrez, puis vérifiez que le statut indique une connexion valide.

> [!NOTE]
> Collez le token seul. Mistral ajoute lui-même le mot `Bearer`.

### Tester

Ouvrez une nouvelle conversation et collez ce prompt :

```text
Utilise uniquement le serveur MCP thousandeyes. Liste les tests ThousandEyes configurés et retourne au maximum les cinq premiers, avec leur nom et leur type si disponibles. N'effectue aucun changement, ne lance pas de test actif et ne modifie aucune configuration.
```

Vous devriez voir apparaître de vrais tests ThousandEyes. Si ça ne marche pas, vérifiez d'abord que le token a bien la permission *API Access*.

---

## Étape 2 : Meraki

### La clé API

Pour le lab, utilisez la clé fournie par l'animateur (`<CLE_API_MERAKI>`).

Pour générer la vôtre une fois de retour chez vous :

1. Connectez-vous sur [dashboard.meraki.com](https://dashboard.meraki.com).
2. Ouvrez **Organization**, puis **API & Webhooks** (ou passez par votre profil, rubrique **Clés API**).
3. Générez une nouvelle clé.

> [!WARNING]
> Une clé API Meraki a les mêmes droits que le compte qui l'a créée. Pour ce genre de test, créez-la depuis un compte en lecture seule.

### Créer le connecteur

1. Allez dans **Contexte**, puis **Connecteurs**, puis **Nouveau connecteur**, puis **Nouveau connecteur personnalisé**.
2. Remplissez :
   - Nom : `Meraki`
   - Serveur : `https://mcp.meraki.com/mcp`
   - Authentification : *Authentification par token API*
   - Bearer : `<CLE_API_MERAKI>`
3. Cliquez sur **Ajouter un connecteur**.

### Tester

```text
Utilise uniquement le serveur MCP meraki. Recherche les organisations et réseaux Meraki auxquels la clé API donne accès. Retourne uniquement les noms et identifiants des cinq premiers résultats maximum. Ne modifie aucune configuration et n'exécute aucune action d'écriture.
```

Vous devriez obtenir la liste des organisations et des networks accessibles. Si rien ne remonte, vérifiez que la clé a été copiée en entier (elle fait 40 caractères) et que l'accès API est activé sur l'organisation.

---

## Étape 3 : Webex Messaging

### Créer l'intégration OAuth côté Webex

1. Connectez-vous sur [developer.webex.com](https://developer.webex.com).
2. Cliquez sur votre avatar, puis **My Webex Apps**, **Create a New App** et enfin **Create an Integration**.
3. Remplissez :
   - Integration name : `Mistral Vibe MCP Lab`
   - Icon : celle que vous voulez
   - Description : `Lab M'Ambassadeurs`
   - Redirect URI : l'URL de retour que Mistral vous donnera au moment de créer le connecteur (voir plus bas)
   - Scopes : `spark:messages_read`, `spark:messages_write`, `spark:rooms_read`, `spark:people_read`
4. Cliquez sur **Add Integration**.
5. Notez le **Client ID** et le **Client Secret**.

> [!CAUTION]
> Webex n'affiche le Client Secret qu'une seule fois. Copiez-le tout de suite.

### Créer le connecteur dans Mistral

1. Allez dans **Contexte**, puis **Connecteurs**, puis **Nouveau connecteur**, puis **Nouveau connecteur personnalisé**.
2. Remplissez :
   - Nom : `Webex-Messaging`
   - Serveur : `https://mcp.webexapis.com/mcp/webex-messaging`
   - Authentification : *OAuth*
3. Mistral affiche une URL de redirection. Copiez-la dans le champ **Redirect URI** de votre intégration Webex.
4. Collez le Client ID et le Client Secret.
5. Enregistrez, puis acceptez l'autorisation dans la fenêtre Webex qui s'ouvre.

> [!TIP]
> Si OAuth vous bloque, passez par un token. Choisissez *Authentification par token API* et collez votre *Personal Access Token*, que vous trouverez sur [developer.webex.com/docs/getting-started](https://developer.webex.com/docs/getting-started). Il expire au bout de 12 heures, ce qui est largement suffisant pour le lab.

### Tester en lecture

```text
Utilise uniquement le serveur MCP webex-messaging. Liste les espaces Webex auxquels j'ai accès et retourne au maximum les cinq premiers, avec leur titre. N'envoie aucun message.
```

L'espace « M'Ambassadeurs » doit apparaître dans la liste.

### Tester en écriture

```text
Utilise uniquement le serveur MCP webex-messaging. Envoie le message « Bonjour depuis Mistral Vibe 👋 » dans l'espace Webex « M'Ambassadeurs », et uniquement dans cet espace.
```

Le message doit apparaître dans l'espace. Si ce n'est pas le cas, vérifiez que le scope `spark:messages_write` est bien coché et que vous faites partie de l'espace.

---

## Étape 4 : les trois ensemble

Une seule demande suffit pour faire travailler les trois connecteurs :

```text
1. Avec le serveur MCP meraki, liste les réseaux de la première organisation accessible (cinq maximum).
2. Avec le serveur MCP thousandeyes, liste les alertes actives (cinq maximum).
3. Rédige un résumé de cinq lignes maximum de l'état du réseau et des alertes.
4. Avec le serveur MCP webex-messaging, publie ce résumé dans l'espace « M'Ambassadeurs ».
N'effectue aucune modification sur Meraki ni sur ThousandEyes.
```

Si tout fonctionne, un résumé du réseau et des alertes est publié dans votre espace Webex.

> [!NOTE]
> Commencer chaque prompt par « Utilise uniquement le serveur MCP … » évite que le modèle aille chercher la réponse ailleurs. Et rappeler « ne modifie rien » ne coûte rien, même avec des clés en lecture seule.

---

## Si ça coince

| Ce que vous voyez | Cause probable | Ce qu'il faut faire |
|---|---|---|
| `401 Unauthorized` | Le token est mal copié | Recollez-le seul, sans `Bearer ` ni espace autour |
| `403 Forbidden` | Il manque un droit | ThousandEyes : *API Access*. Meraki : accès API activé. Webex : les scopes |
| Le connecteur n'est pas proposé dans le chat | Il n'est pas activé pour cette conversation | Activez-le dans le sélecteur d'outils de la conversation |
| Le modèle utilise le mauvais outil | Le prompt est trop vague | Commencez par « Utilise uniquement le serveur MCP … » |

## Utiliser un autre client MCP

Les URL et les tokens sont les mêmes partout. Voici deux exemples pour Meraki, que vous pouvez adapter aux deux autres serveurs.

**Claude Code**

```bash
claude mcp add --transport http meraki https://mcp.meraki.com/mcp --header "Authorization: Bearer <CLE_API_MERAKI>"
```

**Codex** (`~/.codex/config.toml`)

```toml
[mcp_servers.meraki]
url = "https://mcp.meraki.com/mcp"
bearer_token_env_var = "MERAKI_API_KEY"
```

> [!NOTE]
> Ces commandes changent d'une version à l'autre. En cas de doute, regardez la documentation de votre client à la rubrique « remote MCP » ou « streamable HTTP ».

## Avant de partir

1. Supprimez les trois connecteurs dans **Contexte**, puis **Connecteurs**.
2. Supprimez l'intégration Webex depuis **My Webex Apps**.

L'animateur révoque les clés du lab à la fin de la session.

---

## Contribuer

Avant chaque commit, lancez le contrôle anti-fuite :

```bash
./scripts/check-secrets.sh
```

Il refuse le commit s'il trouve quelque chose qui ressemble à une clé Meraki, un token ThousandEyes ou un token Webex. Tous les prompts du lab sont aussi disponibles séparément dans [`prompts/`](prompts/).
