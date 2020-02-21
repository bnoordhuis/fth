: drop ( a -- ) a ! ;
: dup  ( a -- a a ) a ! a @ a @ ;
: swap ( a b -- b a ) b ! a ! b @ a @ ;
: over ( a b -- a b a ) b ! a ! a @ b @ a @ ;
: 2dup ( a b -- a b a b ) b ! a ! a @ b @ a @ b @ ;
: rot  ( a b c -- b c a ) c ! b ! a ! b @ c @ a @ ;
: -rot ( a b c -- c a b ) c ! b ! a ! c @ a @ b @ ;

: msb (   -- a ) $8000000000000000 ;
: 1-  ( a -- a ) 1 - ;
: -1  (   -- a ) 0 1- ;
: not ( a -- a ) -1 xor ;
: +   ( a b -- c ) not - 1- ;
: 0<> ( a b -- c ) 0= not ;
: <>  ( a b -- c ) - 0<> ;
: =   ( a b -- c ) - 0= ;
: >=  ( a b -- c ) - msb and 0= ; \ msb clear, i.e., a-b >= 0
: <   ( a b -- c ) >= not ;
: >   ( a b -- c ) swap < ;
: <=  ( a b -- c ) > not ;

: cr 10 emit ;

: . ( n -- ) 10 div dup 0= if drop else . then 48 + emit ;
