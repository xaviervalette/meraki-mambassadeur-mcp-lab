# Lab M'Ambassadeurs — ThousandEyes, Meraki et Webex dans Mistral Vibe

Connecter trois serveurs MCP Cisco à Mistral Vibe (compte gratuit), puis les interroger en langage naturel.

**Durée totale : environ 45 minutes.**

| Étape | Quoi | Durée |
|---|---|---|
| 0 | Préparer Mistral Vibe | 5 min |
| 1 | ThousandEyes MCP | 10 min |
| 2 | Meraki MCP | 10 min |
| 3 | Webex Messaging MCP | 15 min |
| 4 | Scénario combiné | 5 min |

> **Tokens et clés API** : aucun secret n'est stocké dans ce dépôt. L'animateur vous les remet le jour du lab. Partout où vous voyez `<...>`, remplacez par la valeur reçue.

---

## Endpoints MCP

| Service | Endpoint |
|---|---|
| ThousandEyes | `https://api.thousandeyes.com/mcp` |
| Meraki | `https://mcp.meraki.com/mcp` |
| Webex Messaging | `https://mcp.webexapis.com/mcp/webex-messaging` |

## Prérequis

- [ ] **Mistral Vibe** : compte gratuit sur [chat.mistral.ai](https://chat.mistral.ai), depuis n'importe quel navigateur.
- [ ] **ThousandEyes** : token API avec la permission *API Access* (fourni par l'animateur).
- [ ] **Meraki** : clé API Dashboard (fournie par l'animateur).
- [ ] **Webex** : compte Webex + intégration OAuth créée sur votre profil [developer.webex.com](https://developer.webex.com).
- [ ] **Espace Webex de test** sans contenu sensible, par exemple « M'Ambassadeurs ».


## Schéma du lab
<img width="901" height="455" alt="image" src="https://github.com/user-attachments/assets/b91a5adb-8fa4-4853-b6d4-818e7c773060" />

---

## Étape 0 — Préparer Mistral Vibe (5 min)

### 0.1 Ouvrir les connecteurs

1. Connectez-vous sur [chat.mistral.ai](https://chat.mistral.ai).
2. Menu de gauche : cliquez sur **Contexte**.
3. Sous-menu : cliquez sur **Connecteurs**.
4. Cliquez sur **Nouveau connecteur**, puis **Nouveau connecteur personnalisé**.

### 0.2 Ce que demande chaque connecteur MCP distant

| Champ | Exemple |
|---|---|
| Nom | `ThousandEyes`, `Meraki`, `Webex-Messaging` |
| Serveur | URL de l'endpoint MCP |
| Authentification | Header `Authorization: Bearer <TOKEN>` **ou** OAuth |

---

## Étape 1 — ThousandEyes MCP (10 min)

Endpoint : `https://api.thousandeyes.com/mcp`

### 1.1 Créer le connecteur

1. **Contexte** → **Connecteurs** → **Nouveau connecteur** → **Nouveau connecteur personnalisé**.
2. Renseignez :
   - **Nom** : `ThousandEyes`
   - **Serveur** : `https://api.thousandeyes.com/mcp`
   - **Authentification** : *Authentification par token API*
   - **Bearer** : `<TOKEN_THOUSANDEYES>`
3. Enregistrez. Vérifiez que le statut indique une connexion valide.

### 1.2 Valider

Ouvrez une nouvelle conversation et collez :

```text
Utilise uniquement le serveur MCP thousandeyes. Liste les tests ThousandEyes configurés et retourne au maximum les cinq premiers, avec leur nom et leur type si disponibles. N'effectue aucun changement, ne lance pas de test actif et ne modifie aucune configuration.
```

- ✅ **Attendu** : des tests ThousandEyes réels apparaissent dans le chat.
- ❌ **Échec** : vérifiez que le token a la permission *API Access* et que vous avez collé le token seul, sans le mot `Bearer`.

---

## Étape 2 — Meraki MCP (10 min)

Endpoint hébergé par Cisco : `https://mcp.meraki.com/mcp`

### 2.1 Clé API Meraki

**Pour le lab, utilisez la clé fournie par l'animateur** (`<CLE_API_MERAKI>`).

Pour générer votre propre clé plus tard :

1. Connectez-vous sur [dashboard.meraki.com](https://dashboard.meraki.com).
2. Ouvrez **Organization → API & Webhooks** (ou **Profil → Clés API**).
3. Générez une clé. Utilisez de préférence un compte en lecture seule.

### 2.2 Créer le connecteur

1. **Contexte** → **Connecteurs** → **Nouveau connecteur** → **Nouveau connecteur personnalisé**.
2. Renseignez :
   - **Nom** : `Meraki`
   - **Serveur** : `https://mcp.meraki.com/mcp`
   - **Authentification** : *Authentification par token API*
   - **Bearer** : `<CLE_API_MERAKI>`
3. Cliquez sur **Ajouter un connecteur**.

### 2.3 Valider

```text
Utilise uniquement le serveur MCP meraki. Recherche les organisations et réseaux Meraki auxquels la clé API donne accès. Retourne uniquement les noms et identifiants des cinq premiers résultats maximum. Ne modifie aucune configuration et n'exécute aucune action d'écriture.
```

- ✅ **Attendu** : la liste des organisations et networks Meraki accessibles.
- ❌ **Échec** : vérifiez que la clé est bien copiée en entier (40 caractères) et que l'accès API est activé sur l'organisation.

---

## Étape 3 — Webex Messaging MCP (15 min)

Endpoint : `https://mcp.webexapis.com/mcp/webex-messaging`

### 3.1 Créer l'intégration OAuth Webex

1. Connectez-vous sur [developer.webex.com](https://developer.webex.com).
2. Cliquez sur votre avatar → **My Webex Apps** → **Create a New App** → **Create an Integration**.
3. Renseignez :
   - **Integration name** : `Mistral Vibe MCP Lab`
   - **Icon** : n'importe laquelle
   - **Description** : `Lab M'Ambassadeurs`
   - **Redirect URI** : l'URL de callback affichée par Mistral Vibe dans le formulaire OAuth du connecteur (voir 3.2, étape 3)
   - **Scopes** : `spark:messages_read`, `spark:messages_write`, `spark:rooms_read`, `spark:people_read`
4. Cliquez sur **Add Integration**.
5. Copiez le **Client ID** et le **Client Secret**. Le secret ne s'affiche qu'une fois.

### 3.2 Créer le connecteur

1. **Contexte** → **Connecteurs** → **Nouveau connecteur** → **Nouveau connecteur personnalisé**.
2. Renseignez :
   - **Nom** : `Webex-Messaging`
   - **Serveur** : `https://mcp.webexapis.com/mcp/webex-messaging`
   - **Authentification** : *OAuth*
3. Copiez l'URL de redirection affichée par Mistral, et collez-la dans le champ **Redirect URI** de votre intégration Webex (3.1).
4. Collez le **Client ID** et le **Client Secret** Webex.
5. Enregistrez, puis acceptez l'autorisation dans la fenêtre Webex qui s'ouvre.

> **Plan B (si OAuth bloque)** : choisissez *Authentification par token API* et collez votre *Personal Access Token* depuis [developer.webex.com/docs/getting-started](https://developer.webex.com/docs/getting-started). Il expire au bout de 12 heures, ce qui suffit pour le lab.

### 3.3 Valider (lecture)

```text
Utilise uniquement le serveur MCP webex-messaging. Liste les espaces Webex auxquels j'ai accès et retourne au maximum les cinq premiers, avec leur titre. N'envoie aucun message.
```

- ✅ **Attendu** : l'espace « M'Ambassadeurs » apparaît dans la liste.

### 3.4 Valider (écriture)

```text
Utilise uniquement le serveur MCP webex-messaging. Envoie le message « Bonjour depuis Mistral Vibe 👋 » dans l'espace Webex « M'Ambassadeurs », et uniquement dans cet espace.
```

- ✅ **Attendu** : le message apparaît dans l'espace Webex.
- ❌ **Échec** : vérifiez que le scope `spark:messages_write` est coché sur l'intégration et que vous êtes membre de l'espace.

---

## Étape 4 — Scénario combiné (5 min)

Les trois connecteurs travaillent ensemble dans une seule demande :

```text
1. Avec le serveur MCP meraki, liste les réseaux de la première organisation accessible (cinq maximum).
2. Avec le serveur MCP thousandeyes, liste les alertes actives (cinq maximum).
3. Rédige un résumé de cinq lignes maximum de l'état du réseau et des alertes.
4. Avec le serveur MCP webex-messaging, publie ce résumé dans l'espace « M'Ambassadeurs ».
N'effectue aucune modification sur Meraki ni sur ThousandEyes.
```

- ✅ **Attendu** : un résumé réseau + alertes apparaît dans l'espace Webex.

---

## Dépannage rapide

| Symptôme | Cause probable | Correction |
|---|---|---|
| `401 Unauthorized` | Token mal copié | Recollez le token seul, sans `Bearer ` ni espace |
| `403 Forbidden` | Permission manquante | ThousandEyes : *API Access*. Meraki : accès API activé. Webex : scopes |
| Le connecteur n'apparaît pas dans le chat | Connecteur désactivé dans la conversation | Activez-le dans le sélecteur d'outils de la conversation |
| Mistral utilise le mauvais outil | Prompt trop vague | Commencez le prompt par « Utilise uniquement le serveur MCP … » |

## Après le lab

1. Supprimez les trois connecteurs dans **Contexte → Connecteurs**.
2. Supprimez l'intégration Webex dans **My Webex Apps**.

Les clés fournies pour le lab sont révoquées par l'animateur à la fin de la session.

---

## Pour les contributeurs

Avant chaque commit, lancez le contrôle anti-fuite :

```bash
./scripts/check-secrets.sh
```

Les prompts du lab sont aussi disponibles séparément dans [`prompts/`](prompts/).
