_key =['int', 'void', 'if', 'while','return', 'continue', 'break', 'scanf', 'main','printf','read','write','else']
symbol = ['(', ')', '{', '}', '[', ']', ',',';', '+', '-', '*',
          '/']

class Token:
    def __init__(self, type, name):
        self.type=type
        self.name=name

class Scanner:
    def __init__(self, file_name):
        self.filename=file_name
        f=open(file_name,"r")
        self._content=f.read()
        self._syn = ''  #token type
        self._p = 0  #index
        self._mstate = 0 #string state
        self._cstate = 0 #character state
        self._dstate = 0 #digit state

        self._mysymbol = []
        self._tokens=[] #to store all tokens

    def analysis(self,mystr):
        _value = ''
        ch = mystr[self._p]
        self._p += 1
        while ch == ' ':
            ch = mystr[self._p]
            self._p += 1
        if ch.isalpha() or ch == '_':    # letter(letter|digit)*
            while ch.isdigit() or ch.isalpha() or ch == '_':
                _value += ch
                ch = mystr[self._p]
                self._p += 1
            self._p -= 1
            self._syn = 'identifier'
            for s in _key:
                if cmp(s,_value) == 0:
                    self._syn='reserved_word'
                    t=Token(self._syn,_value)
                    self._tokens.append(t)
                    break
            if self._syn == 'identifier':
                _value+='_cs254'
                t=Token('identifier', _value)
                self._tokens.append(t)

        elif ch=='#': # deal with #include
            while True:
                _value+=ch
                if mystr[self._p] == "\n":
                    break
                ch=mystr[self._p]
                self._p+=1
            t=Token('meta_statement',_value)
            self._tokens.append(t)

        elif ch == '\"':        # string
            while True :
                if self._mstate==2:
                    break
                _value += ch
                if self._mstate == 0:
                    if ch == '\"':
                        self._mstate = 1
                elif self._mstate == 1:
                    if ch == '\"':
                        self._mstate = 2
                ch = mystr[self._p]
                self._p += 1

            if self._mstate == 2:
                self._mstate = 0
            t=Token('string',_value)
            self._tokens.append(t)
            self._p -= 1

        elif ch.isdigit():
            while ch.isdigit():
                _value+= ch
                if self._dstate == 0:
                    self._dstate = 1
                elif self._dstate == 1:
                    self._dstate = 1
                ch = mystr[self._p]
                self._p += 1
            if mystr[self._p].isalpha():   ## deal with illegal token e.g.2010i
                illegal=_value+mystr[self._p]
                print("illegal token: "+illegal)
            t=Token('number',_value)
            self._tokens.append(t)
            self._p -= 1

        elif ch == '<':
            _value = ch
            ch = mystr[self._p]
            if ch == '=':           # '<='
                _value += ch
                self._p += 1
            t=Token('symbol',_value)
            self._tokens.append(t)

        elif ch == '>':
            _value = ch
            ch = mystr[self._p]
            if ch == '=':           # '>='
                _value += ch
                self._p += 1
            t=Token('symbol',_value)
            self._tokens.append(t)

        elif ch == '!':
            _value = ch
            ch = mystr[self._p]
            if ch == '=':           # '!='
                _value += ch
                self._p += 1
            t=Token('symbol',_value)
            self._tokens.append(t)
        elif ch == '/':
            _value = ch
            ch=mystr[self._p]
            if ch =='/':
                while ch!='\n':    # get rid of comments
                    self._p+=1
                    ch=mystr[self._p]
            else:
                t=Token('symbol',_value)
                self._tokens.append(t)

        elif ch in symbol:
            _value = ch
            ch = mystr[self._p]
            t=Token('symbol',_value)
            self._tokens.append(t)

        elif ch == '=':
            _value = ch
            ch = mystr[self._p]
            if ch =='=':            # '=='
                _value += ch
                self._p += 1
            t=Token('symbol',_value)
            self._tokens.append(t)

        elif ch == '&':
            _value = ch
            ch = mystr[self._p]
            if ch == '&':           # '&&'
                _value += ch
                self._p += 1
            t=Token('symbol',_value)
            self._tokens.append(t)

        elif ch == '|':
            _value = ch
            ch = mystr[self._p]
            if ch == '|':           # '||'
                _value += ch
                self._p += 1
            t=Token('symbol',_value)
            self._tokens.append(t)

class main():
    s=Scanner("automaton.c")
    while s._p != len(s._content):
        if s._p==len(s._content):
            break
        s.analysis(s._content)

    file=open("automaton_254.c",'w+')
    for token in s._tokens:
        print token.name
        if '#' in token.name:
            file.write('\n')
            file.write(token.name)
            file.write('\n')
        elif token.name=='read' or token.name=='write':
            file.write(token.name)
        elif ';' in token.name:
            file.write(token.name)
            file.write('\n')
        else:
            file.write(token.name+' ')
