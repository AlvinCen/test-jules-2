#include <stdio.h>

int main() {
    unsigned long canary;
    asm("mov %%fs:0x28, %0" : "=r"(canary));
    printf("Canary: 0x%016lx\n", canary);
    return 0;
}
