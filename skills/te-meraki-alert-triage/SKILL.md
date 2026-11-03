---
name: te-meraki-alert-triage
description: Load this skill when the user says they received a ThousandEyes
  alert or asks to triage/analyze active ThousandEyes alerts and find a root
  cause. The skill always correlates with Meraki infrastructure (WAN status,
  devices, changelogs) without asking for confirmation.
---
# ThousandEyes → Meraki Alert Triage

The skill is invoked after the user reports a ThousandEyes alert and asks for an analysis. The Meraki investigation is always performed by default — never ask the user whether to investigate the Meraki infrastructure.

## Step 1 — List active ThousandEyes alerts

Call `list_alerts({})` on the ThousandEyes connector with no arguments to get current active (triggered) alerts. Do not pass `state` (default returns triggered alerts). Paginate with `cursor` (from `nextCursor`) if `hasMore` is true, keeping all other parameters identical.

Present the alerts to the user concisely: alert name/type, test name, target/agent information, trigger timestamp, and current state.

## Step 2 — Identify the target network from the ThousandEyes agent name

The Meraki network to investigate corresponds to the **name of the ThousandEyes agent** that raised the alert.

1. Extract the agent name from the alert (alert metadata, `meta.id`, or test/agent details; use ThousandEyes test/agent tools such as `get_test` if needed).
2. On Meraki, find the network whose name matches the agent name:
   - If the organization ID is unknown, call `execute_api` on the Meraki connector with `capability_id="getOrganizations"`.
   - List networks with `capability_id="getOrganizationNetworks"` and the `organizationId`, then match the network name against the agent name.
3. If no network matches the agent name, ask the user which network to analyze — only then.

## Step 3 — WAN status of the target network

Use `semantic_search` on the Meraki connector (e.g. query "appliance uplink status WAN") to find the relevant capability, then `execute_api` to check the WAN/uplink status of the appliances in that network (interface statuses, IPs, loss/latency on WAN uplinks).

## Step 4 — Device status in the target network

Use `semantic_search` (e.g. "device statuses in a network") then `execute_api` to list the devices of the network and their status: connectivity, reachability, and any device down/offline/rebooting.

## Step 5 — Changelogs around the alert timestamp

1. Use the alert's trigger timestamp from ThousandEyes.
2. Fetch the configuration changelog via `semantic_search` (query "configuration changelog") then `execute_api` with `getOrganizationConfigurationChanges`, filtering on `networkId` and a time window from **5–10 minutes before the alert timestamp** to the alert timestamp (or current time if the alert is still active). Do not look back hours before the alert — a change that caused an alert happens just before it. Widen only if the user explicitly asks.
3. If this call fails with a permissions/scope error, report clearly that the API key lacks the `dashboard:general:config:read` scope and that changelog analysis cannot be completed — do not fail silently.
4. Also fetch the network event log (`getNetworkEvents`) over the same window.
5. For each change/event, compare its timestamp with the alert timestamp and compute the time delta; flag anything that correlates in time (configuration changes, firewall rules, firmware updates, reboots, uplink changes). State explicitly whether a change correlates with the alert.

## Rules

- Never ask the user whether to investigate Meraki: it is always part of the analysis. Only ask for the network if the agent name cannot be matched.
- Treat every alert as newly discovered: do not assume any prior knowledge of the alert or mention that it "is still present" from a previous analysis.
- Meraki: **read-only operations only** — never perform create/update/delete/reboot operations.
- For each Meraki call, always go through `semantic_search` first (except `getOrganizations` / `getOrganizationNetworks` called directly), then `execute_api` with the returned `capability_id`.
- Paginated Meraki results: request a bounded page size; only follow `startingAfter` cursors when plausible; stop when a page is empty or the cursor repeats/invalid. Report pages fetched and whether more may remain.

## Final output — mandatory sequential format

Present the results in the user's answer in exactly this order, one section at a time:

1. **Active alerts** — list the alerts discovered (name/type, test, agent, trigger timestamp, severity/state). Introduce them as a fresh discovery.
2. **WAN link health** — state directly the WAN/uplink status of the target network (interface statuses, IPs, any flap or degradation).
3. **Device status** — a Markdown table of the network's devices with their status. **Exclude sensors** (product type "sensor", e.g. MT series) from the table and the analysis.
4. **Changelog investigation** — the changes/events found in the window, with their time delta versus the alert timestamp, and an explicit statement of whether a change correlates with the alert.
5. **Recommendations / actions** — the corrective actions to perform (or next investigation steps if no root cause was found).
