import sys
import ast
from tokenize import tokenize, tok_name, TokenError
import json

from io import BytesIO
from collections import Counter

from . codequery import CodeQuery, CodeQueryException

IGNORE_TOKENS = [
    'NL', 'NEWLINE', 'INDENT', 'DEDENT', 'ENCODING', 'ENDMARKER', 'COMMENT',
]

class Module(CodeQuery):
    def __init__(self, filename=None, node=None):
        assert node and not filename or filename and not node, "node xor filename"
        self.errors = []
        self.filename = filename
        self._bytes = open(self.filename, mode="br").read()
        try:
            self.tokens = self.__tokenize()
            self._ast = self.__parse()
            CodeQuery.__init__(self, self._ast)
        except TokenError as e:
            self.errors.append(e)
            raise CodeQueryException()

        messages = [e.msg for e in self.errors]
        if self.errors: raise CodeQueryException(''.join(messages))

    def __parse(self):
        try:
            _ast = ast.parse(self._bytes)
        except SyntaxError as e:
            self.errors.append(e)
            _ast = ast.AST()
        return _ast

    def __tokenize(self):
        try:
            tokens = list(tokenize(BytesIO(self._bytes).readline))

        except Exception as e:
            raise CodeQueryException(e.__class__.__name__)

        return tokens

    def tokcount(self):
        vector = Counter(tok_name[tk.type] for tk in self.tokens)
        for token_type in IGNORE_TOKENS:
            vector.pop(token_type, None)
        return json.dumps(vector)
