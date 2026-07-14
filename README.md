# jellyfin stack module

- Module id: `jellyfin`
- Module repo: `jellyfin-stack-module`
- Source repo: none declared
- Lifecycle: `active`

## Owned overlays
- `stack.runtime.yaml`
- `stack.config/jellyfin`

## Dependencies
- `stack-foundation`

## Deployed contract

Jellyfin is a browser-visible public service behind the shared Keycloak edge.
The module is not considered clean-deploy ready until the deployed service:

- completes the Jellyfin startup wizard automatically
- exposes `/System/Info/Public` with `ProductName` set to `Jellyfin Server`
  and `StartupWizardCompleted` set to `true`
- blocks password login on the external native-client route
- supports Keycloak OIDC login for browser access
- has at least one configured media library so authenticated screenshots do
  not show the empty first-run state

Visual evidence for Jellyfin must show a populated authenticated application
state. A login page, setup wizard, or "Nothing here. Ask an administrator to
create a library." page is a failing screenshot even if routing and SSO worked.

## Validation

```sh
./tests/validate.sh
```

## Lifecycle

`active` modules are expected to keep `stack.module.json`, owned overlays, and `tests/validate.sh` in sync.
