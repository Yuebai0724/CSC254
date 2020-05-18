
#include <stdio.h>

#define read(x) scanf("%d",&x)

#define write(x) printf("%d\n",x)
int array_cs254 [ 32 ] ;
void initialize_array_cs254 ( void ) { int idx_cs254 , bound_cs254 ;
bound_cs254 = 32 ;
idx_cs254 = 0 ;
while ( idx_cs254 < bound_cs254 ) { array_cs254 [ idx_cs254 ] = - 1 ;
idx_cs254 = idx_cs254 + 1 ;
} } int fib_cs254 ( int val_cs254 ) { if ( val_cs254 < 2 ) { return 1 ;
} if ( array_cs254 [ val_cs254 ] == - 1 ) { array_cs254 [ val_cs254 ] = fib_cs254 ( val_cs254 - 1 ) + fib_cs254 ( val_cs254 - 2 ) ;
} return array_cs254 [ val_cs254 ] ;
} int main ( void ) { int idx_cs254 , bound_cs254 ;
bound_cs254 = 32 ;
initialize_array_cs254 ( ) ;
idx_cs254 = 0 ;
printf ( "The first few digits of the Fibonacci sequence are:\n" ) ;
while ( idx_cs254 < bound_cs254 ) { write( fib_cs254 ( idx_cs254 ) ) ;
idx_cs254 = idx_cs254 + 1 ;
} } 