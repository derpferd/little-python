# Little Python

*A Super Simplified Python with a Little Syntactic Sugar*  
*MIT License*

**Tests:** [![Build Status](https://travis-ci.org/derpferd/little-python.svg?branch=master)](https://travis-ci.org/derpferd/little-python)
[![Requirements Status](https://requires.io/github/derpferd/little-python/requirements.svg?branch=master)](https://requires.io/github/derpferd/little-python/requirements/?branch=master)
[![codecov](https://codecov.io/gh/DerPferd/little-python/branch/master/graph/badge.svg)](https://codecov.io/gh/DerPferd/little-python)

**Package:** [![Version](https://img.shields.io/pypi/v/littlepython.svg)](https://pypi.python.org/pypi/littlepython)
[![supported-versions](https://img.shields.io/pypi/pyversions/littlepython.svg)](https://pypi.python.org/pypi/littlepython)

### Statement of Purpose

> The intent of the Little Python programming language is to implement a simple language that is easy for people with little to no coding experience to create a program. The need for such a language arose when creating a framework for competitions  where individuals of all skill levels can create a rudimentary AI to compete against various challenges. We wanted to “level” the playing field by having a language that is limited in functionality, creating an even playing field. Please keep this in mind when suggesting and/or commenting on the design features.

### Install
Run this following command to install from PyPI.

```pip install littlepython```

### Setup for development
Run ```pip install -e .``` to install the package locally using sym links so changes to the code in the repo will be reflected globally.
To run all the tests run ```python setup.py test```.

### Todo
*This list has been moved to Issues instead*
- [X] Add better metadata to setup.py
- [ ] Add negative constant numbers
- [ ] Add arrays
- [ ] Add functions
- [ ] Add scoping
- [ ] Get to and stay at 100% code coverage.
   - Currently at 95% for interpreter.py and 91% for parser.py
   - Most of the uncovered code are edge cases, therefore we need more test cases.


## Warning the following was created for version 0.1

### Design Thoughts
> Data Types
> > For now I think that there is need for only two data types: boolean and integer.

> Variables
> > Names are case sensitive.
> > Must start with letter or underscore otherwise must be alphanumeric or an underscore.

> Operators
> > Tentative list of operators: +,-,*,/,or,and,not,is(==),<,>,<=,>=

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
* is, is not, <, >, <=, >=
* not
* and, or



### Syntax
**statements** ::= statement
                 | statement statements

**statement**  ::= variable '=' expression newline
                 | control newline

**control**    ::= 'if ' ctrl_exp { statements }
                 | 'if ' ctrl_exp { statements } 'else' { statements }
                 | 'if ' ctrl_exp { statements } elif 'else' { statements }

**elif**       ::= 'elif ' ctrl_exp { statements }
                 | elif 'elif ' ctrl_exp { statements }

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
                 | term '%' factor

**factor**     ::= number
                 | variable
                 | '(' expression ')'

**newline**    ::= '\n'

### Interpreter/Compiler design
> I have for better or worse started with a design for a two part system. First the script will be compiled into an AST. Then it will be able to be run(interpreted). State will not be saved however it is possible to pass global variables into the program and get the state of all variables at the end of the program.
> - Parse script into Abstract Syntax Tree. (This is where all syntax error will be caught)
> - Reduce Abstract Syntax Tree.
> - Execute Abstract Syntax Tree with arguments.
