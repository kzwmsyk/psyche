#! /usr/bin/env python
import sys
from typing import IO
import re
from sctoken import Token, TokenType

EOL = "\n"
TAB = "\t"
SPACE = " "


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
                c = self._get_char()
                if c == 't':
                    return self._create_token(TokenType.T)
                elif c == 'f':
                    return self._create_token(TokenType.F)
                else:
                    raise Exception("Invalid character after #")
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
                return self._create_token(TokenType.DOT)
            case '"':
                buf = ""
                while (c := self._get_char()) != '"':
                    if c == '\\':
                        buf += self._escape_char()
                    else:
                        buf += c
                return self._create_token(TokenType.STRING, buf)
            case ';':
                while c != EOL:
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
        # TODO:
        # "<intraline whitespace>*<line ending>"
        # "x<hex scalar value>"
    }

    def _escape_char(self) -> str:
        c = self._get_char()
        if c in self.ESCAPE_CHARS:
            return self.ESCAPE_CHARS[c]
        else:
            raise Exception("Invalid escape character")

    def _number_token(self, buf: str) -> bool:
        return re.match(r'^[+\-]?\d+$', buf) is not None

    def _symbol_token(self, buf: str) -> bool:
        return re.match(r'^[a-zA-Z0-9!?+\-*/=<>]+$', buf) is not None
