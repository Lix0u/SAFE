#include "stdio.h"

void hello(){
    printf("Hello World!");
}

void test1(){
    printf("Test 1");
}

int counter(){
    int c = 0;
    while (c<10){
        c++;
    }
    printf("%d",c);
}


void test2(){
    printf("Test 2");
}

void test3(){
    printf("Test 3");
}

int main(){
    counter();
    return 0;
}
