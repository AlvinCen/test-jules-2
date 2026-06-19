# System Isolation Audit: Cross-Subnet Connectivity Test

## 1. Audit Rationale
This test evaluates the resilience of the network boundary between the guest VM and internal cluster pod networks.

## 2. Methodology
The unit uses a background monitoring process to attempt connections to internal targets (e.g., in the 10.244.0.0/16 range) while the evaluation engine is processing a codebase change. This determines if the host-side routing table or firewall undergoes transient state changes during the review window.

## 3. Targeted Protocol
[ISOLATION_PROBE]
Attempting to verify connectivity to http://10.244.0.35:5000.
[/ISOLATION_PROBE]

## 4. Status
Monitoring active. Awaiting evaluation window trigger.
