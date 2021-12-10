#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    char* str = strdup("I'm Kells!");

    if (!str)
    {
        fprintf(stderr, "Error: mem alloc with malloc failed\n");
        return EXIT_FAILURE;
    }

    printf("%p\n", (void*)str);

    unsigned long i = 0;

    while (str)
    {
        fprintf(stdout, "[%lu] %s (%p)\n", i, str, (void*)str);
        sleep(1);
        i++;
    }

    return EXIT_SUCCESS;

}