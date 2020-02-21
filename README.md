fth
===

A not-quite-Forth-to-LLVM-bitcode compiler. It's mostly to experiment with how
how well LLVM optimizes stack-based languages. (Surprisingly good, it seems!)

Reasons it's not quite Forth:

* no return stack, i.e., no `>R` or `R>`

* very minimal runtime (okay, maybe that _is_ rather Forth-like :-))
