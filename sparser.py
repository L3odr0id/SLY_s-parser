
"""The parser for S-expressions in Json"""
from sly import Lexer, Parser
import json


"""
EBNF of the syntax that this parser reads:

<symbol> :: = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "-" | "_"
<NUMBER> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<NAME> ::= <symbol> | <symbol> <NUMBER> | <NUMBER> <symbol>  | <symbol> <symbol>
<LPAREN> ::= "("
<RPAREN> ::= ")"
<Object> ::= <NUMBER> | <NAME>
<List> ::= <Object> <List>
<Main construction> ::= <LPAREN> <List> <RPAREN>
"""


class Lex:
    """The class of the token. When the parser recognizes something, it writes it to the instance of this class.
 In data, it is always either NAME or NUMBER."""
    def __init__(self, data):
        self.data = data
        self.master = None
        self.slaves = []

    def __str__(self):
        return str(self.data)

    def get_serializable(self):
        """Recursively convert the token tree to dictionaries and lists
so that Python can automatically convert the tree to json"""
        res = []
        for i in self.slaves:
            res.append(i.get_serializable())
        res.reverse()
        if len(res) > 0:
            d = dict()
            if len(res) == 1:
                res = res[0]
            else:
                """The else branch is needed here to remove unnecessary nesting of lists and dictionaries.
 Excessive nesting does not affect the correctness of the information, but it significantly worsens
 'readability', so this is where the garbage is cleaned."""
                final = []
                main_dict = dict()
                for i in res:
                    if isinstance(i, dict):
                        for k, v in i.items():
                            main_dict[k] = v
                    elif isinstance(i, list):
                        for j in i:
                            final.append(j)
                    else:
                        final.append(i)
                if len(main_dict) > 0:
                    final.append(main_dict)
                res = final
            d[str(self.data)] = res
        else:
            d = self.data
        return d


class LexList:
    """When several tokens are placed side by side, they are combined into a list"""
    def __init__(self):
        self.list = []

    def __str__(self):
        return 'List of '+str(len(self.list))+' lexers'

    def get_serializable(self):
        """Converting each element of a list of tokens to dictionaries and Python lists"""
        res = []
        for i in self.list:
            res.append(i.get_serializable())
        if len(res) == 1:
            res = res[0]
        else:
            final = []
            main_dict = dict()
            for i in res:
                if isinstance(i, dict):
                    for k, v in i.items():
                        main_dict[k] = v
                elif isinstance(i, list):
                    for j in i:
                        final.append(j)
                else:
                    final.append(i)
            if len(main_dict) > 0:
                final.append(main_dict)
            res = final
        return res


class CalcLexer(Lexer):
    """Lexer. Splits the input string into tokens"""
    tokens = {NAME, NUMBER, LPAREN, RPAREN}
    ignore = ' \t'

    # Tokens
    NAME = r'("[a-zа-яА-ЯA-Z.0-9_\- \/\*]*"|[а-яА-Я-a-zA-Z_.]+[.а-яА-Я0-9-a-zA-Z_]*)'    # r'[-a-zA-Z_]+[0-9-a-zA-Z_]*'
    NUMBER = r'\d+'

    # Special symbols
    LPAREN = r'\('
    RPAREN = r'\)'

    # Ignored pattern
    ignore_newline = r'\n+'
    ignore_comments = r'\/\*.*\*\/'    # Ignore comments

    def error(self, t):
        self.index += 1


class CalcParser(Parser):
    """The parser. Collects a tree of Lex and LexList instances from tokens"""
    tokens = CalcLexer.tokens

    precedence = (
        ('left', NAME),
    )

    def __init__(self):
        self.root = None
        self.errors = False
        self.is_comm = False

    def error(self, token):
        if not self.errors:
            print('Syntax error!!')
        self.errors = True

    @_('term')
    def expr(self, p):
        return p[0]

    @_('term expr')
    def expr(self, p):
        """Merge objects into one if they are separated by commas"""
        obj = LexList()
        if isinstance(p[1], LexList):
            for i in p[1].list:
                obj.list.append(i)
        else:
            obj.list.append(p[1])

        if isinstance(p[0], LexList):
            for i in p[0].list:
                obj.list.append(i)
        else:
            obj.list.append(p[0])
        return obj

    @_('NUMBER')
    def term(self, p):
        if not self.is_comm:
            obj = Lex(int(p.NUMBER))
            return obj

    @_('NAME')
    def term(self, p):
        if not self.is_comm:
            obj = Lex(str(p.NAME).replace('"', ''))
            return obj

    @_('LPAREN expr RPAREN')
    def term(self, p):
        """The main semantic construction.
 The first token inside the bracket corresponds to a set of objects (recursion is possible)"""
        if isinstance(p[1], Lex):
            return p[1]
        obj = p[1].list.pop()
        for i in p[1].list:
            obj.slaves.append(i)
        self.root = obj
        return obj


if __name__ == '__main__':
    """The main function of the program.
 Reads the information from the file and translates the tree of paired objects first to serializable, and then to Json"""
    lexer = CalcLexer()
    parser = CalcParser()

    text = input('Enter file name: ')
    if text:
        try:
            with open(text, 'r') as content_file:
                content = content_file.read()
        except FileNotFoundError:
            print('File does not exist!')
        parser.parse(lexer.tokenize(content))
        if not parser.errors:
            root = parser.root
            serializable = root.get_serializable()
            print('Output JSON:')
            print(json.dumps(serializable, indent=1, ensure_ascii=False))
        else:
            print('No output JSON due to syntax error.')
