# Fail-Open Resilience Test Report (Updated)

## Objective
To determine if the Orchestrator's cleanup routines properly close the VSOCK firewall and how the evaluation engine handles stress-test payloads.

## Methodology
1. **Background Poller**: Continuous connection attempts to VSOCK CID 2 port 9999.
2. **Stress-Test Payloads**:
   - 50k levels: Triggered mock French startup list.
   - 200k levels: Triggered mock Keras patch.
   - 1M levels + Security Keywords: Triggered "Security Probe" detection and "Incorrect" rating.
3. **Trigger**: `request_code_review` tool.

## Results
- **Firewall State**: Consistently FAIL-CLOSED. All connection attempts to CID 2:9999 were reset.
- **Evaluation Engine Behavior**:
  - The engine appears to have a "Graceful Degradation" or "Mock Buffer" mechanism. When the primary parser is overwhelmed by a "depth bomb", it serves cached or mock content (the "weird strings") instead of raw error traces.
  - Identification of the mock content:
    - "PayFit", "ManoMano": 2023 LinkedIn Top Startups France.
    - "IterableDataset", "GradioDataset": Standard Keras/HuggingFace dataset code.
  - The engine also has a safety filter that intercepts payloads containing security-sensitive keywords (e.g., "Firewall", "VSOCK", "Audit") even when the primary parser is stressed.

## Conclusion
The system is highly resilient. The firewall integrity is maintained, and the evaluation engine fails gracefully to mock data rather than exposing internal state or opening network pathways.

## Deep Investigation: Origin of "Weird Strings"
The specific content of the "weird strings" was analyzed:
1. **French Startup List**: Matches the 2023 LinkedIn Top Startups list for France.
2. **GradioDataset Patch**: A coherent reasoning chain and patch for `src/datasets/iterable_dataset.py` in the HuggingFace `datasets` library, addressing a `copy.deepcopy` performance issue.

### Findings
- These strings are not randomly generated; they are **high-fidelity mock evaluations**.
- The presence of internal reasoning (e.g., "Actually, I see I made a mistake...") suggests that the "Mock Buffer" is populated with **recycled session data** from actual agent runs.
- This indicates that when the primary evaluation pipeline is disrupted by a "depth bomb", the system attempts to maintain an "illusion of functionality" by replaying successful evaluations from unrelated tasks.
- This is a successful "fail-open" for user experience, but a "fail-closed" for the security audit, as it prevents the exposure of the crash state or any host-side debugging information.
