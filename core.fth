: drop ( a -- ) a ! ;
: dup  ( a -- a a ) a ! a @ a @ ;
: swap ( a b -- b a ) b ! a ! b @ a @ ;
: over ( a b -- a b a ) b ! a ! a @ b @ a @ ;
: 2dup ( a b -- a b a b ) b ! a ! a @ b @ a @ b @ ;
: rot  ( a b c -- b c a ) c ! b ! a ! b @ c @ a @ ;
: -rot ( a b c -- c a b ) c ! b ! a ! c @ a @ b @ ;

: 1- ( a -- a ) 1 - ;
: -1 ( -- a ) 0 1- ;
: not ( a -- a ) -1 xor ;

: + ( a b -- c ) not - 1- ;
: > ( a b -- c ) swap < ;
: <> ( a b -- c ) b ! a ! a @ b @ < b @ a @ < xor ;
: = ( a b -- c ) <> not ;
: 0= ( a -- b ) 0 = ;
: 0<> ( a -- b ) 0 <> ;
: >= ( a b -- c ) < not ;
: <= ( a b -- c ) > not ;

: cr 10 emit ;

: . ( n -- ) 10 div dup 0= if drop else . then 48 + emit ;
