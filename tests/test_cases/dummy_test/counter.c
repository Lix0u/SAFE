#include "stdio.h"


int counter(){
    int c = 0;
    while (c<10){
        c++;
    }
    printf("%d",c);
}

int main(){
    counter();
    return 0;
}