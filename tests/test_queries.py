import pytest
import ast

import codequery
from codequery import Module


@pytest.fixture(scope="session")
def mod():
    mod_filename = codequery.__file__.replace("__init__", "module")
    mod = Module(mod_filename)
    return mod


def test_imports(mod):
    assert mod.imports("ast")
    assert mod.imports("json")
    assert mod.imports("tokenize.TokenError")
    assert not mod.imports("math")
    assert not mod.imports("collections")


def test_defs(mod):
    assert mod.defs_class("Module")
    assert mod.defs_function("__parse")
    assert mod.defs_function("__tokenize")
    assert mod.defs_function("tokcount")


def test_calls(mod):
    assert mod.calls(".parse")
    assert mod.calls(".pop")
    assert mod.calls("BytesIO")
    assert not mod.calls("Module")
    assert not mod.calls("CodeQuery")


def test_count(mod):
    # count classes
    assert mod.count("ClassDef") == 1

    # count functions
    assert mod.count("FunctionDef") == 4

    # count other elements
    assert mod.count("While") == 0
    assert mod.count("Slice") == 0
    assert mod.count("Constant") == 12


def test_select(mod):
    # select by node type
    classes = mod.select("ClassDef")
    assert classes[0].name == "Module"

    # select by type from inner nodes (not only the module node)
    methods = [m.name for m in classes[0].select("FunctionDef")]
    assert set(methods) == set({"__init__", "__parse", "__tokenize", "tokcount"})

    # select by name matching
    functions = mod.select("FunctionDef", name="tokcount")
    assert [f.name for f in functions] == ["tokcount"]
