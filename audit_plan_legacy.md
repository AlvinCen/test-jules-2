# Security Audit: BPF Loader Backward Compatibility

## Objective
Verify the behavior of the `iproute2` legacy BPF ELF parser when handling oversized map names (200 bytes) in objects without BTF information.

## Background
The custom `ip` utility uses `libbpf` by default. However, for legacy objects, it should fallback to or utilize its internal parser (`iproute2_find_map_name_by_id`). This audit aims to determine if this legacy path is safe against buffer overflows or segmentation faults when presented with extremely long identifiers.

## Test Requirements
- Struct: `bpf_elf_map` (legacy).
- Pinning: `PIN_NONE` (to bypass system-level pinning restrictions).
- Compilation: No BTF/debug info (`-g` omitted).
- Loading: XDP attachment via `ip link`.
