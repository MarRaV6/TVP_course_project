grammar bnf;

program
  : block '.'
  ;

block
  : consts? plvars? procedure* statement
  ;

consts
  : 'const' Ident '=' Number (',' Ident '=' Number)* ';'
  ;

plvars
  : 'var' Ident (',' Ident)* ';'
  ;

procedure
  : 'procedure' Ident ';' block ';'
  ;

statement
  : Ident ':=' expression
  | 'call' Ident
  | '!' Ident
  | 'begin' statement (';' statement)* 'end'
  | 'if' condition 'then' statement
  | 'while' condition 'do' statement
  ;

condition
  : 'odd' expression
  | expression ('='|'#'|'<'|'<='|'>'|'>=') expression
  ;

expression
  : ('+'|'-')? term (('+'|'-') term)*
  ;

term
  : factor (('*'|'/') factor)*
  ;

factor
  : Ident
  | Number
  | '(' expression ')'
  ;


WS     : [ \r\t\n]+ -> skip ; // skip spaces, tabs, newlines
Comment : '{' .*? '}' -> skip;

Ident  : ALPHA (ALPHA | DIGIT)* ;
Number : DIGIT+;

ALPHA : 'a'..'z' | 'A'..'Z' ;
DIGIT : '0'..'9' ;