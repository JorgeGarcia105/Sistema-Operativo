//creacion de un sistema operativo desde cero con c y python
// componente de bajo Nivel con c

#include "init.h"
#include "idt.h"
#include "isr.h"
#include "monitor.h"
#include "timer.h"
#include "keyboard.h"
#include "descriptor_tables.h"
#include "paging.h"
#include "fs.h"
#include "multiboot.h"

int main(struct multiboot *mboot_ptr)
{
    // Initialize all the ISRs and segmentation
    init_descriptor_tables();
    // Initialize the screen (by clearing it)
    monitor_clear();
    // Initialize the timer
    init_timer(50);
    // Initialize the keyboard
    init_keyboard();
    // Initialize the file system
    fs_root = initrd_init(mboot_ptr);
    // Initialize the paging
    initialise_paging();
    // Enable interrupts
    asm volatile("sti");
    // The next line will cause a page fault
    // int *ptr = (int*)0xA0000000;
    // int do_page_fault = *ptr;
    return 0;
}

// Path: descriptor_tables.c