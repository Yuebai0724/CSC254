
#include <stdio.h>

#define read(x) scanf("%d",&x)

#define write(x) printf("%d\n",x)
void state_0_cs254 ( void ) ;
void state_1_cs254 ( void ) ;
void state_2_cs254 ( void ) ;
void state_3_cs254 ( void ) ;
int getnextdigit_cs254 ( void ) { int n_cs254 ;
while ( 0 == 0 ) { printf ( "Give me a number (-1 to quit): " ) ;
read( n_cs254 ) ;
if ( - 1 <= n_cs254 && 1 >= n_cs254 ) { break ;
} printf ( "I need a number that's either 0 or 1.\n" ) ;
} return n_cs254 ;
} void state_0_cs254 ( void ) { int a_cs254 ;
a_cs254 = getnextdigit_cs254 ( ) ;
if ( - 1 == a_cs254 ) { printf ( "You gave me an even number of 0's.\n" ) ;
printf ( "You gave me an even number of 1's.\n" ) ;
printf ( "I therefore accept this input.\n" ) ;
return ;
} if ( 0 == a_cs254 ) { state_2_cs254 ( ) ;
} if ( 1 == a_cs254 ) { state_1_cs254 ( ) ;
} } void state_1_cs254 ( void ) { int a_cs254 ;
a_cs254 = getnextdigit_cs254 ( ) ;
if ( - 1 == a_cs254 ) { printf ( "You gave me an even number of 0's.\n" ) ;
printf ( "You gave me an odd number of 1's.\n" ) ;
printf ( "I therefore reject this input.\n" ) ;
return ;
} if ( 0 == a_cs254 ) { state_3_cs254 ( ) ;
} if ( 1 == a_cs254 ) { state_0_cs254 ( ) ;
} } void state_2_cs254 ( void ) { int a_cs254 ;
a_cs254 = getnextdigit_cs254 ( ) ;
if ( - 1 == a_cs254 ) { printf ( "You gave me an odd number of 0's.\n" ) ;
printf ( "You gave me an even number of 1's.\n" ) ;
printf ( "I therefore reject this input.\n" ) ;
return ;
} if ( 0 == a_cs254 ) { state_0_cs254 ( ) ;
} if ( 1 == a_cs254 ) { state_3_cs254 ( ) ;
} } void state_3_cs254 ( void ) { int a_cs254 ;
a_cs254 = getnextdigit_cs254 ( ) ;
if ( - 1 == a_cs254 ) { printf ( "You gave me an odd number of 0's.\n" ) ;
printf ( "You gave me an odd number of 1's.\n" ) ;
printf ( "I therefore reject this input.\n" ) ;
return ;
} if ( 0 == a_cs254 ) { state_1_cs254 ( ) ;
} if ( 1 == a_cs254 ) { state_2_cs254 ( ) ;
} } int main ( ) { state_0_cs254 ( ) ;
} 