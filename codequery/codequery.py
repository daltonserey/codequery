import ast

class CodeQueryException(Exception): pass

class CodeQuery:
    def __init__(self, node):
        self._ast = node
        self.nodes = {}
        for node in ast.walk(self._ast):
            self.nodes.setdefault(type(node).__name__, [])
            self.nodes[type(node).__name__].append(node)
        self.name = self._ast.name if hasattr(self._ast, "name") else None
        self.value = self._ast.value if hasattr(self._ast, "value") else None
        self.id = self._ast.id if hasattr(self._ast, "id") else None
        self.called = None
        self.imported = None
        self.defined_functions = None
        self.defined_classes = None

    @property
    def imported(self):
        if self._imported is None:
            self._init_imported()
        return self._imported

    @imported.setter
    def imported(self, value):
        self._imported = value

    def _init_called(self):
        def collect_name(node):
            if type(node) is str:
                return node

            if type(node) is ast.BinOp:
                return ""

            elif type(node) is ast.Import:
                return node.names

            elif hasattr(node, "id"):
                return node.id

            elif hasattr(node, "value"):
                return collect_name(node.value) + ".value"

            elif hasattr(node, "func"):
                return collect_name(node.func) + ".func"
            
            msg = f"fatal: unpredicted node type: {node.__class__.__name__}"
            msg += f" at line {node.lineno}" if hasattr(node, "lineno") else ""
            raise CodeQueryException(msg)

        self.called = {}
        for call in self.nodes.get('Call', []):
            if type(call.func) is ast.Name:
                # call is a normal function call
                self.called.setdefault(f"{call.func.id}", []).append(None)

            elif type(call.func) is ast.Attribute:
                # call is a method call
                #cn = CodeQuery(call)
                obj = collect_name(call.func)
                method = call.func.attr
                self.called.setdefault(f"{method}", []).append(obj)

    def _init_imported(self):
        self.imported = set({})
        for imp in self.nodes.get('Import', []):
            for alias in imp.names:
                self.imported.add(alias.name)

        for imp in self.nodes.get('ImportFrom', []):
            for alias in imp.names:
                self.imported.add(f"{imp.module}.{alias.name}")

    def _init_defined_functions(self):
        self.defined_functions = set({})
        for fun in self.nodes['FunctionDef']:
            self.defined_functions.add(fun.name)

    def _init_defined_classes(self):
        self.defined_classes = set({})
        for fun in self.nodes['ClassDef']:
            self.defined_classes.add(fun.name)

    def imports(self, name):
        return name in self.imported

    def imports_from(self, name):
        return any(m.startswith(f"{name}.") for m in self.imported)

    def not_imports(self, name):
        return not self.imports(name)

    def not_imports_from(self, name):
        return not self.imports_from(name)

    def defs_function(self, name):
        if self.defined_functions is None:
            self._init_defined_functions()

        return name in self.defined_functions

    def defs_class(self, name):
        if self.defined_classes is None:
            self._init_defined_classes()

        return name in self.defined_classes

    def calls(self, arg1):
        if self.called is None:
            self._init_called()

        if isinstance(arg1, CodeQuery):
            name = arg1._ast.name
        else:
            name = arg1

        obj, function = name.rsplit(".", 1) if "." in name else (None, name)

        if obj == "":
            return any(m for m in self.called.get(function, []))
        else:
            return obj in self.called.get(function, [])

    def not_calls(self, arg1):
        return not self.calls(arg1)

    def count(self, element):
        name = element if type(element) is str else element.__name__
        return len(self.nodes.get(name, []))

    def select(self, nodetype=None, name=None):
        assert nodetype, "nodetype is mandatory"
        nodetype = nodetype if type(nodetype) is str else nodetype.__name__

        selected = []
        for node in self.nodes.get(nodetype, []):
            if node != self._ast and name is None or node.name == name:
                selected.append(CodeQuery(node))

        return selected
        
    def select_orig(self, nodetype=None, name=None):
        name = nodetype if type(nodetype) is str else nodetype.__name__
        return [CodeQuery(n) for n in self.nodes.get(name, []) if n != self._ast]
        
    def uses(self, element):
        return bool(self.select(element))

    def not_uses(self, element):
        return not self.uses(element)

    def has(self, element):
        return self.uses(element)

    def not_has(self, element):
        return not self.has(element)

    def defines(self, *args):
        return "TBD"

    def defs_method(self, *args):
        return "TBD"

    def has_main(self, *args):
        return "TBD"

    def all(self, element):
        name = element if type(element) is str else element.__name__
        return self.nodes.get(name)

    def dump(self):
        return ast.dump(self._ast)

