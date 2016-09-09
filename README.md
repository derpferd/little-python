# Little Python
*A Super Simplified Python with a Little Syntactic Sugar*
*MIT License*


### Statement of Purpose

> The intent of the Little Python programming language is to implement a simple language that is easy for people with little to no coding experience to create a program. The need for such a language arose when creating a framework for competitions  where individuals of all skill levels can create a rudimentary AI to compete against various challenges. We wanted to “level” the playing field by having a language that is limited in functionality, creating an even playing field. Please keep this in mind when suggesting and/or commenting on the design features.

### Design Thoughts
> Data Types
> > For now I think that there is need for only two data types: boolean and integer.

> Variables
> > Names are case sensitive.
> > Must start with letter or underscore otherwise must be alphanumeric or an underscore.

> Operators
> > Tentative list of operators: +,-,*,/,or,and,not,is(==)

> > I have decided that instead of supporting both the 'is’ and ‘==’ operators I would just support 'is’.

> > This may change in the future.

> > The assignment operator(=) is only allowed to be used after a variable name which is the first symbol in the statement.

> Control Structure
> > I think that we will only be using the if structure.
Currently there is only if and else no elif(else if).

> Functions
> > These are probably not need as is.
This could become a feature in the future

> Scope
> > For now everything is in a global scope.

> Comments
> > Use a # to start a comment which will continue to the end of the line.

### Order of execution
* =
* ()
* *,/,%
* +,-
* is, is not
* not
* And, or



### Syntax
**statements** ::= statement
                 | statement statement

**statement**  ::= variable '=' expression newline
                 | control newline

**control**    ::= 'if ' ctrl_exp { statements }
                 | 'if ' ctrl_exp { statements } 'else' { statements }

**ctrl_exp**   ::= expression
                 | ctrl_exp 'and' ctrl_exp
                 | ctrl_exp 'or' ctrl_exp
                 | ctrl_exp 'is' ctrl_exp
                 | 'not' ctrl_exp

**expression** ::= term
                 | expression '+' term
                 | expression '-' term

**term**       ::= factor
                 | term '*' factor
                 | term '/' factor

**factor**     ::= number
                 | variable
                 | '(' expression ')'

**newline**    ::= '\n'

### Interpreter/Compiler design
> I have for better or worse started with a design for a two part system. First the script will be compiled into an AST. Then it will be able to be run(interpreted). State will not be saved however it is possible to pass global variables into the program and get the state of all variables at the end of the program.
Parse script into Abstract Syntax Tree. (This is where all syntax error will be caught)
Reduce Abstract Syntax Tree.
Execute Abstract Syntax Tree with arguments.

### AST Syntax
> The program is represented as a list of ASTs. Each AST is a statement in the form of a dictionary. Each statement is executed in order. Below is the syntax for a given statement.
 ~~~
 {'op': '+', 'a': a, 'b': b}    // add subtree a to subtree b
 {'op': '-', 'a': a, 'b': b}    // subtract subtree b from subtree a
 {'op': '*', 'a': a, 'b': b}    // multiply subtree a by subtree b
 {'op': '/', 'a': a, 'b': b}    // divide subtree a from subtree b
 {'op': '%', 'a': a, 'b': b}    // modulo of subtree a by subtree b
 {'op': 'is', 'a': a, 'b': b}   // test if a is equal to b
 {'op': 'and', 'a': a, 'b': b}  // logical and of a and b
 {'op': 'or', 'a': a, 'b': b}   // logical or of a and b
 {'op': 'not', 'a': a}          // logical not of a
 {'op': 'int', 'a': a}          // converts or states that a value is an int
 {'op': 'if', 'ctrl': a, 'if': b, 'else': c}// if a is true do b else do c (the else if optional)
 {'op': '=', 'var': a, 'exp': b}  // set variable a to b
 ~~~
