#! /usr/bin/env python
import sys
from typing import IO
import re
from sctoken import Token, TokenType

EOL = "\n"
TAB = "\t"
SPACE = " "

CHAR_NAMES = {
    "nul": "\0",
    "space": " ",
    "tab": "\t",
    "newline": "\n",
    "return": "\r",
}

RADIX_CHARS = {
    "b": 2,
    "o": 8,
    "d": 10,
    "x": 16,
}


class Scanner:

    def __init__(self, stream: IO[str] = sys.stdin):
        self.stream = stream
        self.pushback_tokens = []
        self.pushback_chars = []
        self.line_ends = []
        self.line = 1
        self.col = 1

    def _get_char(self) -> str:
        c = None
        if len(self.pushback_chars) > 0:
            c = self.pushback_chars.pop()
        else:
            c = self.stream.read(1)

        if c == EOL:
            if len(self.line_ends) == self.line - 1:
                self.line_ends.append(self.col)
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return c

    def pushback_token(self, token: Token):
        self.pushback_tokens.append(token)

    def _pushback_char(self, c: str):
        if c == EOL:
            self.line -= 1
            self.col = self.line_ends[self.line-1]
        else:
            self.col -= 1
        self.pushback_chars.append(c)

    def get_token(self) -> Token:

        if len(self.pushback_tokens) > 0:
            return self.pushback_tokens.pop()

        c = self._get_char()
        while c == SPACE or c == TAB or c == EOL:
            c = self._get_char()

        match c:
            case '':
                return self._create_token(TokenType.EOF)
            case '#':
                return self._dispatch_sharp()
            case '(':
                return self._create_token(TokenType.LPAREN)
            case ')':
                return self._create_token(TokenType.RPAREN)
            case "'":
                return self._create_token(TokenType.QUOTE)
            case "`":
                return self._create_token(TokenType.QUASIQUOTE)
            case ",":
                c = self._get_char()
                if c == "@":
                    return self._create_token(TokenType.UNQUOTE_SPLICING)
                else:
                    self._pushback_char(c)
                    return self._create_token(TokenType.UNQUOTE)
            case '.':
                c = self._get_char()
                if c == '.':
                    c2 = self._get_char()
                    if c2 == '.':
                        return self._create_token(TokenType.SYMBOL, '...')
                    self._pushback_char(c2)
                self._pushback_char(c)
                return self._create_token(TokenType.DOT)
            case '"':
                buf = ""
                while (c := self._get_char()) != '"':
                    if c == '':
                        raise Exception("unterminated string")
                    if c == '\\':
                        buf += self._escape_char()
                    else:
                        buf += c
                return self._create_token(TokenType.STRING, buf)
            case ';':
                while c != EOL and c != '':
                    c = self._get_char()
                return self.get_token()
            case _:
                buf = c
                while ((c := self._get_char())
                       and c != EOL
                       and c != SPACE and c != TAB
                       and c != ")" and c != "("):
                    buf += c
                self._pushback_char(c)

                if (self._number_token(buf)):
                    return self._create_token(TokenType.NUMBER, buf)
                elif (self._symbol_token(buf)):
                    return self._create_token(TokenType.SYMBOL, buf)
                else:
                    return self._create_token(TokenType.OTHER, buf)

    def _dispatch_sharp(self) -> Token:
        c = self._get_char()
        if c == 't':
            return self._create_token(TokenType.T)
        if c == 'f':
            return self._create_token(TokenType.F)
        if c == '\\':
            return self._read_char_token()
        if c == '(':
            return self._create_token(TokenType.VECTOR)
        if c == '|':
            self._skip_block_comment()
            return self.get_token()
        if c == 'u':
            nxt = self._get_char()
            if nxt == '8':
                nxt2 = self._get_char()
                if nxt2 == '(':
                    return self._create_token(TokenType.BYTEVECTOR)
            raise Exception("Invalid character after #u")
        return self._read_prefixed_number(c)

    def _skip_block_comment(self) -> None:
        while True:
            c = self._get_char()
            if c == '':
                raise Exception("unterminated block comment")
            if c == '|':
                c2 = self._get_char()
                if c2 == '#':
                    return

    def _read_prefixed_number(self, first: str) -> Token:
        exact: bool | None = None
        c = first
        if c == 'e':
            exact = True
            c = self._get_char()
        elif c == 'i':
            exact = False
            c = self._get_char()
        if c == '#':
            c2 = self._get_char()
            if c2 == 'e':
                exact = True
                c = self._get_char()
            elif c2 == 'i':
                exact = False
                c = self._get_char()
            else:
                self._pushback_char(c)
                c = c2
        if c not in RADIX_CHARS:
            if exact is None:
                raise Exception("Invalid character after #")
            self._pushback_char(c)
            buf = self._read_plain_number()
            if not buf:
                raise Exception("Invalid character after #")
            return self._create_number_token(buf, exact=exact, radix=10)
        radix = RADIX_CHARS[c]
        buf = self._read_radix_digits(radix)
        if not buf:
            raise Exception("Invalid character after #")
        return self._create_number_token(buf, exact=exact, radix=radix)

    def _read_radix_digits(self, radix: int) -> str:
        buf = ""
        while True:
            c = self._get_char()
            if c == '':
                break
            if c in (SPACE, TAB, EOL, '(', ')', '"', ';'):
                self._pushback_char(c)
                break
            buf += c
        return buf

    def _read_plain_number(self) -> str:
        buf = ""
        while True:
            c = self._get_char()
            if c == '':
                break
            if c in (SPACE, TAB, EOL, '(', ')', '"', ';'):
                self._pushback_char(c)
                break
            buf += c
        return buf

    def _create_number_token(self,
                             buf: str,
                             *,
                             exact: bool | None,
                             radix: int) -> Token:
        token = self._create_token(TokenType.NUMBER, buf)
        token.number_exact = exact
        token.number_radix = radix
        return token

    def _create_token(self,
                      token_type: TokenType,
                      buffer: str = None) -> Token:
        return Token(token_type=token_type,
                     buffer=buffer,
                     line=self.line,
                     col=self.col - len(buffer or " "))

    ESCAPE_CHARS = {
        'a': "\a",
        'b': "\b",
        't': "\t",
        'n': "\n",
        'r': "\r",
        '"': '"',
        '\\': '\\',
        '|': '|',
    }

    def _escape_char(self) -> str:
        c = self._get_char()
        if c in self.ESCAPE_CHARS:
            return self.ESCAPE_CHARS[c]
        if c == 'x':
            digits = ""
            while True:
                ch = self._get_char()
                if ch == '' or not re.match(r'[0-9a-fA-F]', ch):
                    self._pushback_char(ch)
                    break
                digits += ch
            if not digits:
                raise Exception("Invalid hex escape")
            return chr(int(digits, 16))
        if c in (SPACE, TAB):
            while c in (SPACE, TAB):
                c = self._get_char()
            if c != EOL and c != '':
                raise Exception("Invalid escape character")
            while c == EOL or c in (SPACE, TAB):
                if c == EOL:
                    c = self._get_char()
                    continue
                if c in (SPACE, TAB):
                    c = self._get_char()
                    continue
                break
            self._pushback_char(c)
            return self._escape_char()
        if c == EOL:
            c = self._get_char()
            while c in (SPACE, TAB):
                c = self._get_char()
            self._pushback_char(c)
            return self._escape_char()
        raise Exception("Invalid escape character")

    def _read_char_token(self) -> Token:
        c = self._get_char()
        if c == '':
            raise Exception("unexpected EOF in character literal")
        if c in (' ', EOL, TAB, ')', '('):
            return self._create_token(TokenType.CHAR, c)
        buf = c
        while True:
            c = self._get_char()
            if c in ('', SPACE, TAB, EOL, '(', ')'):
                self._pushback_char(c)
                break
            buf += c
        if buf in CHAR_NAMES:
            return self._create_token(TokenType.CHAR, CHAR_NAMES[buf])
        if len(buf) == 1:
            return self._create_token(TokenType.CHAR, buf)
        raise Exception(f"unknown character name: {buf}")

    def _number_token(self, buf: str) -> bool:
        return re.match(
            r'^[+\-]?(\d+(\.\d*)?|\.\d+)([eE][+\-]?\d+)?$',
            buf,
        ) is not None

    def _symbol_token(self, buf: str) -> bool:
        return re.match(r'^[a-zA-Z0-9!?+\-*/=<>]+$', buf) is not None
