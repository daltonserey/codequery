# codequery

A library to make it easy to write code queries, asserts on code
facts and design tests for Python code. It provides a simple
wrapper object with an easiear, more readable API to write
queries on ast nodes as well as the tokenizer standard libraries.

> BEWARE This is just a proof of concept and should be used with
> care in any professional context.  My personal and primary use
> for this package is to check students code in the context of an
> introductory programming course. While automated tests do
> provide good feedback and guidance wrt to functional aspects of
> the code (whether it does what it is expected to do), they do
> not provide any feedback wrt to how the code has been written
> (and, in particular, wrt the way it was NOT expected to be). I
> use `codequery` to write easy to read and understand design
> tests that the students use to restrict the solution space,
> while still using a conventional testing framework and tooling
> (namely, pytest and unittests).

## how to install

```
pip3 install codequery
```

## how to use

TBD. However, the following examples should make it clear for
simple cases. Soon I will add here a minimal documentation for
each query method available in the API.

## examples

The test below is used in a programming problem in which the
student is asked to implement an in-place bubble sort. It
prevents the module under test from: i) importing any modules;
ii) using the `sort()` method and the `sorted()` function (python
built-in functions); and iii) using methods that change lists in
structural way, to assure the algorithm is in-place (this forces
the programmer to manipulate the list as if it was a simple
array, namely, using only item assignments). The `calls()` method
receives a function (or class) name and returns a boolean stating
whether that function is called or not from that module.

```python
from codequery import Module

mod = Module(filename="answer.py")

def test_is_inplace():
    assert not mod.imported
    assert not mod.calls("sorted")
    assert not mod.calls(".sort")
    assert not mod.calls(".append")
    assert not mod.calls(".pop")
    assert not mod.calls(".insert")
```

The test below could be used to complement a query-sort
implementation, to require that a recursive solution be written.
Observe the `select()` function being used. It receives either an
ast node type (or a string that matches the type name) and returns
all the elements in the tree rooted at the given node (in this
case, the whole module `mod`). I'll assume the assert line is
self-explanatory (the `call()` is the same in the example above).

```python
def test_is_recursive():
    functions = mod.select("FunctionDef")
    assert any(f.calls(f) for f in functions)
```

The next test checks whether the module implements the python _main
pattern_ and that it has a `main()` function, called from it.

```python
def test_uses_main_section():
    mainsect = next(e for e in mod.select("If") if e.get("left") == "__name__")
    mainsect.calls("main")
```

> In fact, as selecting the main section is such a common
> pattern, `codequery` has a helper method that makes this code
> become simpler and more readable. The first line in the example
> above could be: `mainsect = mod.select("main_section")`.

## scripts

Two scripts that use `codequery` to analyze code scripts are also
provided: `code-outline` and `code-profile`, which are used to
create code outlines (a listing of the most relevant node
elements that give the code its outline structure) and code
profiles (a vector containing an ordered counting of the most
important elements in the code under analysis).
