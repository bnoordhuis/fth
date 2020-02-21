: fib' ( a b n -- n )
  dup 1 <= if
    drop +
  else
    -rot        ( n a b )
    swap over + ( n b a+b )
    rot         ( b a+b n )
    1- fib'
  then ;

: fib ( n -- n ) 0 1 rot fib' ;

: main 10 fib . cr ;
