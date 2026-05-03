# Security Audit Report

## Executive Summary
This audit was performed in `DEBUG_MODE` to identify vulnerabilities leading to orchestrator or host escape from the Firecracker-based microVM environment.

## 1. Environment Details
- **Hypervisor:** Firecracker (Identified by ACPI FACP signature `FIRECKVM`).
- **Operating System:** Ubuntu 24.04.4 LTS.
- **Kernel Version:** 6.8.0.
- **Guest IP:** 192.168.0.2.
- **Gateway IP:** 192.168.0.1.
- **VSOCK CID:** 2.

## 2. Network Vulnerabilities
### 2.1 Gateway Services (192.168.0.1)
- **Port 53 (DNS):** Open.
- **Port 8080 (HTTP):** Open. Identifies as `BaseHTTP/0.6 Python/3.12.3`.
  - Endpoint `/openapi.json` returns a message about a deprecated API.
  - Endpoints `/docs` and `/redoc` return `501 Unsupported method ('HEAD')`.
  - The root `/` returns a GitHub-like mock page.

### 2.2 VSOCK Notification Socket
- **CID 2, Port 9999:** Identified in `/proc/cmdline` as `vmm.notify_socket`.
- **Behavior:** All connection attempts (JSON, malformed, large buffers, large integers) result in `[Errno 104] Connection reset by peer`.
- **Potential Risk:** This socket is a direct channel to the VMM (Host). Immediate connection resets might indicate a crashing service or a very strict filter. Large integer values or malformed JSON payloads are common triggers for memory corruption in such interfaces.

## 3. Local Vulnerabilities
### 3.1 Privilege Escalation
- **Sudo Access:** User `jules` has full `NOPASSWD: ALL` sudo privileges. Privilege escalation to `root` is trivial.

### 3.2 Host Escape Vectors
- **Docker Socket:** `/run/docker.sock` is accessible. However, testing shows that container execution is currently broken due to `overlayfs` mount issues.
- **VSOCK:** The `AF_VSOCK` interface allows direct communication with the host orchestrator (CID 2). Probing shows it is highly restrictive.
- **OverlayFS:** The guest uses `overlayfs` for the root filesystem, which has had numerous historical vulnerabilities (e.g., CVE-2023-0386).

## 4. Vulnerability Proof of Concept
### 4.1 Gateway Fragility (192.168.0.1:8080)
- **Large Headers:** Sending a 10KB header triggers a `502 Bad Gateway`.
  ```bash
  curl -v -H "A: $(python3 -c 'print("A"*10000)')" http://192.168.0.1:8080/
  < HTTP/1.0 502 Bad Gateway
  ```
- **Large Bodies:** Sending a 100KB body triggers a `500 Internal Server Error`.
  ```bash
  curl -v -d "$(python3 -c 'print("A"*100000)')" http://192.168.0.1:8080/
  < HTTP/1.0 500 Internal Server Error
  ```

### 4.2 VSOCK Restrictions (CID 2, Port 9999)
- **Immediate Rejection:** All payloads, including single bytes and well-formed JSON, result in a connection reset.
  ```python
  # Testing Notify JSON:
  #   Result: [Errno 104] Connection reset by peer
  ```

### 4.3 Docker Functional Limitation
- **Overlay Mount Failure:** Docker cannot start containers because it fails to mount overlay layers, likely due to the nested overlay configuration of the guest.
  ```bash
  docker: Error response from daemon: failed to mount ... err: invalid argument
  ```

## 5. Low-Level Escape Investigation
### 5.1 VSOCK Port Scanning (CID 2)
- **Comprehensive Reset:** Scanning ports 1-65535 on VSOCK CID 2 resulted in no open ports; all responded with `Connection reset by peer`. This confirms CID 2 as the host/VMM and indicates a strict firewall or a single-purpose communication proxy.

### 5.2 Device File and Kernel Feature Probing
- **Kernel Memory (`/dev/mem`):** Attempting to read `/dev/mem` returns null bytes for the first 1KB, consistent with `CONFIG_STRICT_DEVMEM=y` and modern kernel hardening.
- **Virtio-MMIO:** Devices are present at `/sys/devices/virtio-mmio-cmdline/`, providing the transport layer for disk, network, and VSOCK.
- **io_uring:** Confirmed functional (Features: `0x3fff`). While powerful, no immediate escape vector was found without a specific unpatched CVE.

### 5.3 OverlayFS and User Namespaces
- **Restriction:** Although `CONFIG_USER_NS=y`, attempting to mount `overlayfs` within a user namespace fails with `invalid argument`.
- **Mitigation:** The guest's own use of `overlayfs` on top of `squashfs` appears to prevent nested overlay mounts, effectively mitigating `overlayfs`-based metadata copy-up exploits (e.g., CVE-2023-0386) that rely on user namespace mounting.

## 6. Evidence
### 6.1 ACPI Identification
```
0000000 46 41 43 50 14 01 00 00 06 3e 46 49 52 45 43 4b  FACP.....>FIRECK
0000010 56 4d 46 41 44 54 00 00 00 00 00 00 46 43 41 54  VMFADT......FCAT
```

### 6.2 VSOCK Probe Results
```python
# python3 -c 'import socket; s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM); s.connect((2, 9999))'
ConnectionResetError: [Errno 104] Connection reset by peer
```

## 7. Recommendations
1. Harden the VSOCK notification service on the host to handle malformed or unexpected JSON inputs gracefully.
2. Restrict access to the Docker socket.
3. Remove or restrict sudo access for the `jules` user if full control is not required.
