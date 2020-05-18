# identifier, number, reservedword, symbol, string, and meta statement
#coding=utf-8
TYPES_STRING = ['IDENTIFIER', 'NUMBER', 'RESERVED_WORD',
                'SYMBOL', 'STRING', 'META_STATEMENT', 'OPERATOR']
RESERVED_WORD = {'int', 'void', 'if', 'while',
                 'return', 'continue', 'break', 'scanf', 'main','printf'}
SYMBOL = ['(', ')', '{', '}', '[', ']', ',', ';', '+', '-', '*',
          '/', '==', '!=', '<', '<=', '>', '>=', '=', '&&', '||', '&', '|']
SEPERATOR = [ ';','(', ')', '{', '}', '[', ']' ]
SHORT_OPS = ['+', '-', '*', '/', '<',  '>',  '=', '&', '|']
LONG_OPS = ['==', '!=', '<=', '>=', '&&', '||']

SUFFIX = '_csc254'


class Token:
    def __init__(self, typ=None, value=None):
        self.typ = typ
        self.value = value

    def __str__(self):
        return 'TYPE:{0} , VAL:{1}'.format(self.typ, self.value)
class Scanner:
    def __init__(self, file_name):
        # parse c file to string
        self.file_name = file_name
        f = open(self.file_name, 'r')
        self.content = f.read()
        # programmer counter
        self.pc = 0
        self.tokens = []
        self.contentLen = len(self.content)

    def is_blank(self, index):
        if index>=self.contentLen:
            print('at the end of file')
            return False
        blank_character = [' ', '\t', '\n']
        return self.content[index] in blank_character

    def skip_blank(self):
        while self.pc < len(self.content) and self.is_blank(self.pc):
            self.pc += 1

    def next_token(self):
        """
        Args:

        Returns:
        return the next token or EOF

        """
        token = self.match()
        if not token:
            print('END OF THE FILE')
            return None
        self.tokens.append(token)
        return token

    def match(self):
        if self.pc < self.contentLen:
            # If Beginning with a letter
            beginning = self.content[self.pc]
            tokenStringTemp = ''
            tokenObjTemp = None



            if beginning.isalpha() or beginning == '_':

                while not self.is_blank(self.pc) and self.content[self.pc].isalpha():  # 1截取这一段token 并判断它是什么
                    tokenStringTemp += self.content[self.pc]
                    self.pc += 1
                if tokenStringTemp in RESERVED_WORD:  # 2.可能是关键字 e.g. int, float
                    tokenObjTemp = Token(
                        typ='RESERVED_WORD', value=tokenStringTemp)

                else:   # 3.可能是变量名 eg. _name, age 如果是旧加上 _csc254, eg int i ->int i_csc254
                    tokenObjTemp = Token(
                        typ='IDENTIFIER', value=tokenStringTemp+SUFFIX)
            elif beginning.isdigit():  # is number
                while self.content[self.pc].isdigit():
                    tokenStringTemp += self.content[self.pc]
                    self.pc += 1
                tokenObjTemp = Token(typ='NUMBER', value=tokenStringTemp)
            elif beginning in SEPERATOR:  # 分隔符都是一个char
                tokenStringTemp = self.content[self.pc]
                tokenObjTemp = Token(typ='SAPERATOR', value=tokenStringTemp)
                self.pc += 1

            # todo: check if self.content[self.pc+1] valid
            elif beginning+self.content[self.pc+1] in LONG_OPS:
                tokenStringTemp = beginning+self.content[self.pc+1]
                tokenObjTemp = Token(typ='OPERATOR', value=tokenStringTemp)

            elif beginning in SHORT_OPS:
                tokenStringTemp = beginning
                tokenObjTemp = Token(typ='OPERATOR', value=tokenStringTemp)
                self.pc += 1
            elif beginning=='"':#是字符串
                while self.pc<self.contentLen:
                    if tokenStringTemp.endswith('"'):
                        break
                    tokenStringTemp+=self.content[self.pc]
                    self.pc+=1
                tokenStringTemp+='"'
                tokenObjTemp = Token(typ='STRING', value=tokenStringTemp)
            # else:  # invalid token e.g '[@', 3a ....
            while self.is_blank(self.pc):
                self.skip_blank()

            return tokenObjTemp


scanner = Scanner("test.txt")
while True:
    token = scanner.next_token()
    if not token:
        break
    print(token)

print(scanner.content[scanner.pc])
