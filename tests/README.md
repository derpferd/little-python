# Little Python Tests

The original tests were written using the classic unittest framework.
Now we have moved to using [pytest](https://docs.pytest.org/en/latest/).

**Note:** We are currently converting some of the *old* tests to the new framework.
These last old tests can be found in [tests>interpreter>test_lp.py](tests/interpreter/test_lp.py).
Below is a complete list of the functions yet to be ported.

 - Tests to go into `test_edges.py`
    - test_variable_assignment_to_int
    - test_variable_with_underscore
    - test_variable_with_underscore_at_beginning
    - test_variable_assignment_to_simple_expression
    - test_variable_assignment_to_other_variables
    - test_long_alphanumeric_variable_name
    - ~~test_sample~~
    - ~~test_blank~~
    - ~~test_only_newlines~~
    - ~~test_trailing_newlines~~
 - Tests to go into `test_feature_if.py`
    - test_if_with_is_no_trailing_newline
    - test_if_with_not
    - test_if_with_var
    - test_if_with_var_reassignment
    - test_if_with_var_undefined
    - test_if_with_var_undefined_2
    - test_if_with_var_undefined_3
    - test_nested_if
    - test_nested_if_with_var_reassignment
    - test_multiple_ifs
    - test_if_else
    - test_empty_if
    - test_empty_if_2
    - test_empty_if_else
    - test_empty_if_else_2
    - test_empty_if_else_3
    - test_empty_if_else_4
    - test_nested_empty_if_else
    - test_nested_empty_if_else_2
 - Tests to go into `test_comment.py`
    - test_line_comment
    - test_inline_comment_with_spaces
    - test_inline_comment_without_space
    - test_inline_comment_in_statement
    - test_inline_comment_in_nested_statement
 - Don't know why this test exists...?
    - test_beginning_state
 - Tests to go into `test_feature_array.py`
    - test_array_access
    - test_array_modify
    - test_array_access_undefined
    - test_array_access_undefined_2
    - test_array_access_expr
    - test_array_modify_expr
    - test_2d_array_access
    - test_2d_array_modify
 - Tests to go into `test_feature_for_loop.py`
    - test_for_loop
    - test_for_loop_array_set
    - test_for_loop_array_get_and_set
 - Tests to go into `test_feature_func.py`
    - test_simple_func
    - test_func_no_return
    - test_func_return
    - test_func_scope_1
    - test_func_recur
    - test_func_recur_large
    - test_func_recur_count_exceeded
 - Tests to go into `test_feature_other.py`
    - test_execution_count_exceeded
 - Tests to go into `test_op.py`
    - ~~test_op_plus~~
    - ~~test_op_negative_const~~
    - ~~test_op_minus_positive~~
    - ~~test_op_minus_negative~~
    - ~~test_op_mult_zero~~
    - ~~test_op_mult_one~~
    - ~~test_op_mult_other~~
    - ~~test_op_div_normal~~
    - ~~test_op_div_fraction_positive~~
    - ~~test_op_div_fraction_zero~~
    - ~~test_op_div_zero~~
    - ~~test_op_mod~~
    - ~~test_op_mod_zero~~
    - ~~test_op_lt~~
    - ~~test_op_gt~~
    - ~~test_op_lte~~
    - ~~test_op_gte~~
    - ~~test_op_or~~
    - ~~test_op_and~~
    - ~~test_op_is~~
    - ~~test_op_is_not~~
    - ~~test_op_not~~
    - ~~test_op_not_or~~

## Organization

The tests are organized into four directories based on the component they test.
The `__init__.py` file inside each directory contain functions make life easier when writing tests.
Don't forget to use the `@pytest.mark.parametrize` decorator when possible it saves a lot of time writing test code.
Two good example situations where you would use this are: parameter combinations and merging multiple tests into one.

Below are descriptions of the different tests.

### AST
#### `test_eq`
This file tests the `__eq__` operator on the children of the `AST` class.
Basically it tests to make sure that if two `AST` classes have the same data than `__eq__` returns `True` otherwise `False`

#### `test_str`
This file tests the `__str__` operator on all the children of the `AST` class.
The `__str__` method should return a "pretty" printed version of the AST block.
Hopefully sometime in the future this can be used to automatically reformat code to insure code stays clean and consistent.

### Interpreter
#### `test_const`
This file tests the correctness of the assignment of variables to constants(aka. literals).
Example being `a = -1` the variable `a` should contain `-1` not `1` or another different value.
This will be useful for making sure variable set to arrays and other more complex constants are correct.

#### `test_edges`
This file tests edge cases that relate to the program code text. Ex: An empty string program.

#### `test_lp`
This file contains the old tests.
This is kept just in case some part of it is missing when it was ported.
Maybe sometime it will be removed.

#### `test_op`
This file tests to make sure that the interpreter handles all programs containing all the different operators littlepython supports.

### Parser
Each of the test files in this directory test a different feature which the parser can parse. (Note: except for `test_parser_errors`)
Ex: `test_expression` tests the parser against every different valid expression.
#### `test_parser_errors`
This file tests the parsers error cases.  (Note: this file isn't very complete)

### Tokenizer
#### `test_tokenizer`
This file tests all the different tokens that the tokenizer needs to tokenize.

#### `test_features`
This file tests the tokenizer against tokens for each feature.
