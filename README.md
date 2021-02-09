# SLY s-expressions parser

There is very little information and guides on how to write parsers in SLY (https://sly.readthedocs.io/en/latest/sly.html) on the Internet, so I hope this will help you. This program parses my custom syntax S-expressions (https://en.wikipedia.org/wiki/S-expression).


#### EBNF of the syntax that this parser reads:
```
<symbol> :: = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "-" | "_"
<NUMBER> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<NAME> ::= <symbol> | <symbol> <NUMBER> | <NUMBER> <symbol>  | <symbol> <symbol>
<LPAREN> ::= "("
<RPAREN> ::= ")"
<Object> ::= <NUMBER> | <NAME>
<List> ::= <Object> <List>
<Main construction> ::= <LPAREN> <List> <RPAREN>
```
