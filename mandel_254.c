
#include <stdio.h>

#define read(x) scanf("%d",&x)

#define write(x) printf("%d\n",x)
int square_cs254 ( int x_cs254 ) { return ( x_cs254 * x_cs254 + 500 ) / 1000 ;
} int complex_abs_squared_cs254 ( int real_cs254 , int imag_cs254 ) { return square_cs254 ( real_cs254 ) + square_cs254 ( imag_cs254 ) ;
} int check_for_bail_cs254 ( int real_cs254 , int imag_cs254 ) { if ( real_cs254 > 4000 || imag_cs254 > 4000 ) { return 0 ;
} if ( 1600 > complex_abs_squared_cs254 ( real_cs254 , imag_cs254 ) ) { return 0 ;
} return 1 ;
} int absval_cs254 ( int x_cs254 ) { if ( x_cs254 < 0 ) { return - 1 * x_cs254 ;
} return x_cs254 ;
} int checkpixel_cs254 ( int x_cs254 , int y_cs254 ) { int real_cs254 , imag_cs254 , temp_cs254 , iter_cs254 , bail_cs254 ;
real_cs254 = 0 ;
imag_cs254 = 0 ;
iter_cs254 = 0 ;
bail_cs254 = 16000 ;
while ( iter_cs254 < 255 ) { temp_cs254 = square_cs254 ( real_cs254 ) - square_cs254 ( imag_cs254 ) + x_cs254 ;
imag_cs254 = ( ( 2 * real_cs254 * imag_cs254 + 500 ) / 1000 ) + y_cs254 ;
real_cs254 = temp_cs254 ;
if ( absval_cs254 ( real_cs254 ) + absval_cs254 ( imag_cs254 ) > 5000 ) { return 0 ;
} iter_cs254 = iter_cs254 + 1 ;
} return 1 ;
} int main ( ) { int x_cs254 , y_cs254 , on_cs254 ;
y_cs254 = 950 ;
while ( y_cs254 > - 950 ) { x_cs254 = - 2100 ;
while ( x_cs254 < 1000 ) { on_cs254 = checkpixel_cs254 ( x_cs254 , y_cs254 ) ;
if ( 1 == on_cs254 ) { printf ( "X" ) ;
} if ( 0 == on_cs254 ) { printf ( " " ) ;
} x_cs254 = x_cs254 + 40 ;
} printf ( "\n" ) ;
y_cs254 = y_cs254 - 50 ;
} } 