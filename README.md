# jellyfin stack module

- Module id: `jellyfin`
- Module repo: `jellyfin-stack-module`
- Source repo: none declared
- Lifecycle: `active`

## Owned overlays
- `stack.compose/jellyfin.yml`
- `stack.config/jellyfin`

## Dependencies
- `stack-foundation`

## Validation

```sh
./tests/validate.sh
```

## Lifecycle

`active` modules are expected to keep `stack.module.json`, owned overlays, and `tests/validate.sh` in sync.
