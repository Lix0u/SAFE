#include <stdint.h>

typedef void (*code)();

void executeFunctions(code **function_to_execute, code **last_function) {
    uint32_t idx;
    uint32_t n_function_to_execute;

    // Initialize index (idx) to 0
    idx = 0;

    // Calculate the number of functions to execute
    n_function_to_execute = ((uintptr_t)last_function + (3 - (uintptr_t)function_to_execute)) >> 2;

    // If last_function is less than function_to_execute, set the number of functions to execute to 0
    if (last_function < function_to_execute) {
        n_function_to_execute = 0;
    }

    // If there are functions to execute
    if (n_function_to_execute != 0) {
        // Iterate through the array of function pointers
        do {
            // Check if the current function pointer is not null
            if (*function_to_execute != (code *)0x0) {
                // Call the function pointed to by the current function pointer
                (*(*function_to_execute))();
            }

            // Move to the next function pointer in the array
            function_to_execute = function_to_execute + 1;

            // Increment the index
            idx = idx + 1;

        // Continue iterating until all functions have been executed
        } while (idx < n_function_to_execute);
    }
}


int main(int argc, char const *argv[])
{
  return 0;
}
