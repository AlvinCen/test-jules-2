#include <linux/bpf.h>
#include <iproute2/bpf_elf.h>

#define SEC(NAME) __attribute__((section(NAME), used))

struct bpf_elf_map SEC("maps") my_map = {
    .type = BPF_MAP_TYPE_ARRAY,
    .size_key = sizeof(unsigned int),
    .size_value = sizeof(unsigned int),
    .max_elem = 1,
};

SEC("xdp")
int my_pass(void *ctx) {
    return 2; // XDP_PASS
}

char _license[] SEC("license") = "GPL";
