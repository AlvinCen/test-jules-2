# Security Audit: Deep Directory Resolution Constraints

## Objective
Verify the `ip` utility's robustness when handling configuration directory paths (`IPROUTE2_CONFDIR`) that approach filesystem limits and contain non-printable character sequences.

## Test Parameters
- Path Padding: 576 bytes ('A' padding).
- Specific Sequence: `\x40\xe5\x07\x00\x00\x00\x00\x00` (8 bytes).
- Target Directory: `rt_protos.d`.
- Trigger File: `rt_protos.d/test.conf` with content `254\tdummy`.
- Execution: `IPROUTE2_CONFDIR=[PATH] ip -details rule show`.

## Success Criteria
- The utility resolves the configuration without crashing.
- `dmesg` shows no segmentation faults.
