#include <linux/bpf.h>

#define SEC(NAME) __attribute__((section(NAME), used))

#define __uint(name, val) int (*name)[val]
#define __type(name, val) typeof(val) *name

struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __uint(max_entries, 1);
    __type(key, unsigned int);
    __type(value, unsigned int);
} my_map SEC(".maps");

SEC("prog")
int xdp_prog(void *ctx) {
    return 2; /* XDP_PASS */
}

char _license[] SEC("license") = "GPL";
