import tokenizer1
tokens=tokenizer1.main().s._tokens
expr_end_list=[';','==','!=','>=', '>', '<', '<=', '&&', '||', ',', ')', ']']
data_decls_list=['int', 'void', 'printf', 'scanf', 'if', 'while', 'return', 'break', 'continue']
id_fac_list=['*', '/', '+', '-', ';', ')', '<', '>', '=', ']', '==', '!=', '>', '>=', '<', '<=', '&&', '||', ',']
term_end_list=['+', '-', ';', ')', '>', '<', '=', ']','==', '>=', '<=','!=','&&','||', ',']
id_end_list=['(', ',' ,'=', ';', ')']
terminals=['(', ')', '{', '}', '[', ']', ';', ',', '=']

list1=['printf', 'scanf', 'if', 'while', 'return', 'break', 'continue']
if_end_list=['printf', 'scanf', 'if', 'while', 'return', 'break', 'continue','}']
key =['int', 'void', 'if', 'while','return', 'continue', 'break', 'scanf', 'main','printf','read','write','else']

variable_num=0
function_num=0
functions=[]
statements=0
flag=True

class Stack:
     def __init__(self):
         self.items = []
     def push(self, item):
         self.items.append(item)
     def pop(self):
         return self.items.pop()
     def peek(self):
         return self.items[len(self.items)-1]
     def size(self):
         return len(self.items)
     def print_s(self):
         for i in self.items:
             print i
def remove_dup(list):
    final_list = []
    for num in list:
        if num not in final_list:
            final_list.append(num)
    return final_list

s=Stack()
s.push("$$")
s.push("program")

def peek_first(token):
    return token.name[0];
def peek(token):
    return token.name;
def match(str1,str2):
    if str1==str2:
        return True;
    else:
        return False;

token_len=len(tokens)
current_index=0

while current_index<token_len:
    if current_index>=token_len:
        break
    if peek_first(tokens[current_index])=='#':
        current_index+=1
    elif s.peek()=="program":
        if peek(tokens[current_index])=='int' or peek(tokens[current_index])=='void':
            s.pop()
            s.push("prog_next")
            s.push("identifier")
            s.push("type_name")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="prog_next":
        ##print ("prog_next: "+peek(tokens[current_index]))
        if peek(tokens[current_index])=='(':
            s.pop()
            s.push("func_prog")
        elif peek(tokens[current_index])==',' or peek(tokens[current_index])==';':
            s.pop()
            s.push("func_prog")
            s.push("identifier")
            s.push("type_name")
            s.push("data_prog")
        else:
            flag=False
            break
    elif s.peek()=="data_prog":
        if peek(tokens[current_index])==',' or peek(tokens[current_index])==';':
            s.pop()
            s.push(";")
            s.push("id_list_end")
            ##s.print_s()
            variable_num+=1
        else:
            flag=False
            break

    elif s.peek()=="id_list_end":
        if peek(tokens[current_index])==',':
            s.pop()
            s.push("id_list_end")
            s.push("identifier")
            s.push(",")
            ##s.print_s()
            variable_num+=1
        elif peek(tokens[current_index])==';':
            s.pop()
        else:
            flag=False
            break
    elif s.peek()=="data_decls":
        if peek(tokens[current_index])=='int' or peek(tokens[current_index])=='void':
            s.pop()
            s.push("data_decls")
            s.push(";")
            s.push("id_list")
            s.push("type_name")
            ##s.print_s()
        elif tokens[current_index].type=='identifier' or peek(tokens[current_index]) in data_decls_list:
            s.pop()
        else:
            flag=False
            break
    elif s.peek()=="id_list":
        ##print("---id_list")
        if tokens[current_index].type=='identifier' or tokens[current_index].name=='main':    ###############
            s.pop()
            s.push("id_list_end")
            s.push("identifier")
            ##s.print_s()
            variable_num+=1
        else:
            flag=False
            break
    elif s.peek()=="func_prog":
        if peek(tokens[current_index])=='(':
            s.pop()
            s.push("func_list")
            s.push("func_end")
            s.push(")")
            s.push("parameter_list")
            s.push("(")
            ##s.print_s()
            function_num+=1
            functions.append(tokens[current_index-1].name)
        else:
            flag=False
            break
    elif s.peek()=="func_list":
        ##print("---func_list")
        if peek(tokens[current_index])=='int' or peek(tokens[current_index])=='void':
            s.pop()
            s.push("func_list")
            s.push("func")
        else:
            flag=False
            break
    elif s.peek()=="func":
        if peek(tokens[current_index])=='int' or peek(tokens[current_index])=='void':
            s.pop()
            s.push("func_end")
            s.push("func_decl")
            ##s.print_s()
        else:
            flag=False
            break

    elif s.peek()=="func_decl":
        if peek(tokens[current_index])=='int' or peek(tokens[current_index])=='void':
            s.pop()
            s.push(")")
            s.push("parameter_list")
            s.push("(")
            s.push("identifier")
            s.push("type_name")
            ##s.print_s()
            function_num+=1
            functions.append(tokens[current_index+1].name)
        else:
            flag=False
            break
    elif s.peek()=="func_end":
        if peek(tokens[current_index])==';':
            if match(peek(tokens[current_index]),';'):
                current_index+=1
                s.pop()
        elif peek(tokens[current_index])=='{':
            s.pop()
            s.push("}")
            s.push("statements")
            s.push("data_decls")
            s.push("{")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()== "type_name" :
        if peek(tokens[current_index])=='int':
            if match(peek(tokens[current_index]),'int'):
                current_index+=1
                s.pop()
        elif peek(tokens[current_index])=='void':
            if match(peek(tokens[current_index]),'void'):
                current_index+=1
                s.pop()
        else:
            flag=False
            break

    elif s.peek()=="parameter_list":
        if peek(tokens[current_index])=='void':
            s.pop()
            s.push("void_end")
            s.push("void")
            ##s.print_s()
        elif peek(tokens[current_index])=='int':
            s.pop()
            s.push("non_empty_end")
            s.push("identifier")
            s.push("int")
            ##s.print_s()
            variable_num+=1
        elif peek(tokens[current_index])==')':  ##epsilon
            s.pop()
        else:
            flag=False
            break

    elif s.peek()=="void_end":
        if peek(tokens[current_index])=='identifier':
            s.pop()
            s.push("non_empty_end")
            s.push("identifier")
            ##s.print_s()
            variable_num+=1
        elif peek(tokens[current_index])==')':  ##epsilon
            s.pop()
        else:
            flag=False
            break
    elif s.peek()=="non_empty_end":
        if peek(tokens[current_index])==',':
            s.pop()
            s.push("non_empty_end")
            s.push("identifier")
            s.push("type_name")
            s.push(",")
            ##s.print_s()
            variable_num+=1
        elif peek(tokens[current_index])==')':  ##epsilon
            s.pop()
        else:
            flag=False
            break

    elif s.peek()=="identifier":
        if tokens[current_index].type=='identifier'or tokens[current_index].name=='main':
            s.pop()
            s.push("id_end")
            s.push("id")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="id":
        if match(tokens[current_index].type, 'identifier') or tokens[current_index].name=='main':
            ##print ("matched id: "+tokens[current_index].name)
            current_index+=1
            s.pop()
        else:
            flag=False
            break
    elif s.peek()=="string":
        if match(tokens[current_index].type, 'string'):
            current_index+=1
            s.pop()
        else:
            flag=False
            break
    elif s.peek()=="id_end":
        if peek(tokens[current_index])=='[':
            s.pop()
            s.push("id_end")
            s.push("]")
            s.push("expression")
            s.push("[")
            ##s.print_s()
        elif peek(tokens[current_index]) in id_end_list:  #####epsilon######################
            ##print("---id_end")
            s.pop()
        else:
            flag=False
            break

    elif s.peek()=="block_statements":
        if peek(tokens[current_index])=='{':
            s.pop()
            s.push("}")
            s.push("statements")
            s.push("{")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="statements":
        if tokens[current_index].type=='identifier' or peek(tokens[current_index]) in list1: #########################
            s.pop()
            s.push("statements")
            s.push("statement")
            ##s.print_s()
        elif peek(tokens[current_index])=='}':
            s.pop()
        else:
            flag=False
            break
    elif s.peek()=="statement":
        if tokens[current_index].type=='identifier':
            s.pop()
            statements+=1
            s.push("id_follow")
            s.push("identifier")
            ##s.print_s()
        elif peek(tokens[current_index])=='printf':
            s.pop()
            statements+=1
            s.push("print_func_call")
            ##s.print_s()
        elif peek(tokens[current_index])=='scanf':
            s.pop()
            statements+=1
            s.push("scanf_func_call")
            ##s.print_s()
        elif peek(tokens[current_index])=='if':
            s.pop()
            statements+=1
            s.push("if_statement")
            ##s.print_s()
        elif peek(tokens[current_index])=='while':
            s.pop()
            statements+=1
            s.push("while_statement")
            ##s.print_s()
        elif peek(tokens[current_index])=='return':
            s.pop()
            statements+=1
            s.push("return_statement")
            ##s.print_s()
        elif peek(tokens[current_index])=='break':
            s.pop()
            statements+=1
            s.push("break_statement")
            ##s.print_s()
        elif peek(tokens[current_index])=='continue':
            s.pop()
            statements+=1
            s.push("continue_statement")
            ##s.print_s()
        else:
            flag=False
            break

    elif s.peek()=="id_follow":
        if peek(tokens[current_index])=='=':
            s.pop()
            s.push(";")
            s.push("expression")
            s.push("=")
            ##s.print_s()
        elif peek(tokens[current_index])=='(':
            s.pop()
            s.push(";")
            s.push(")")
            s.push("expr_list")
            s.push("(")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="print_func_call":
        if peek(tokens[current_index])=='printf':
            s.pop()
            s.push("print_func_call_end")
            s.push("string")
            s.push("(")
            s.push("printf")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="print_func_call_end":
        if peek(tokens[current_index])==')':
            s.pop()
            s.push(";")
            s.push(")")
            ##s.print_s()
        elif peek(tokens[current_index])==',':
            s.pop()
            s.push(";")
            s.push(")")
            s.push("expression")
            s.push(",")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="scanf_func_call":
        if peek(tokens[current_index])=='scanf':
            s.pop()
            s.push(";")
            s.push(")")
            s.push("expression")
            s.push("&")
            s.push(",")
            s.push("string")
            s.push("(")
            s.push("scanf")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="expr_list":
        if tokens[current_index].type=='identifier' or tokens[current_index].type=='number' or peek(tokens[current_index])=='-' or peek(tokens[current_index])=='(':
            s.pop()
            s.push("non_empty_expr_list")
            ##s.print_s()
        elif peek(tokens[current_index])==')':
            s.pop()
        else:
            flag=False
            break
    elif s.peek()=="non_empty_expr_list":
        if tokens[current_index].type=='identifier' or tokens[current_index].type=='number' or peek(tokens[current_index])=='-' or peek(tokens[current_index])=='(':
            s.pop()
            s.push("non_empty_expr_end")
            s.push("expression")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="non_empty_expr_end":
        if peek(tokens[current_index])==',':
            s.pop()
            s.push("non_empty_expr_end")
            s.push("expression")
            s.push(",")
            ##s.print_s()
        elif peek(tokens[current_index])==')':
            s.pop()
        else:
            flag=False
            break

    elif s.peek()=="if_statement":
        if peek(tokens[current_index])=='if':
            s.pop()
            s.push("if_end")
            s.push("block_statements")
            s.push(")")
            s.push("condition_expression")
            s.push("(")
            s.push("if")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="if_end":
        if peek(tokens[current_index])=='else':
            s.pop()
            s.push("block_statements")
            s.push("else")
            ##s.print_s()
        elif tokens[current_index].type=='identifier' or peek(tokens[current_index]) in if_end_list:
            s.pop()
        else:
            flag=False
            break
    elif s.peek()=="condition_expression":
        if tokens[current_index].type=='identifier' or tokens[current_index].type=='number' or peek(tokens[current_index])=='-' or peek(tokens[current_index])=='(':
            s.pop()
            s.push("cond_end")
            s.push("condition")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="cond_end":
        if peek(tokens[current_index])=='&&' or peek(tokens[current_index])=='||':
            s.pop()
            s.push("condition")
            s.push("condition_op")
            ##s.print_s()
        elif peek(tokens[current_index])==')':
            s.pop()
        else:
            flag=False
            break
    elif s.peek()=="condition_op":
        if peek(tokens[current_index])=='&&':
            if match(peek(tokens[current_index]),'&&'):
                current_index+=1
                s.pop()
        elif peek(tokens[current_index])=='||':
            if match(peek(tokens[current_index]),'||'):
                current_index+=1
                s.pop()
        else:
            flag=False
            break

    elif s.peek()=="condition":
        if tokens[current_index].type=='identifier' or tokens[current_index].type=='number' or peek(tokens[current_index])=='-' or peek(tokens[current_index])=='(':
            s.pop()
            s.push("expression")
            s.push("comparison_op")
            s.push("expression")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="comparison_op":
        if peek(tokens[current_index])=='==':
            if match(peek(tokens[current_index]),'=='):
                current_index+=1
                s.pop()
        elif peek(tokens[current_index])=='!=':
            if match(peek(tokens[current_index]),'!='):
                current_index+=1
                s.pop()
        elif peek(tokens[current_index])=='>':
            if match(peek(tokens[current_index]),'>'):
                current_index+=1
                s.pop()
        elif peek(tokens[current_index])=='>=':
            if match(peek(tokens[current_index]),'>='):
                current_index+=1
                s.pop()
        elif peek(tokens[current_index])=='<':
            if match(peek(tokens[current_index]),'<'):
                current_index+=1
                s.pop()
        elif peek(tokens[current_index])=='<=':
            if match(peek(tokens[current_index]),'<='):
                current_index+=1
                s.pop()
        else:
            flag=False
            break
    elif s.peek()=="while_statement":
        if peek(tokens[current_index])=='while':
            s.pop()
            s.push("block_statements")
            s.push(")")
            s.push("condition_expression")
            s.push("(")
            s.push("while")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="return_statement":
        if peek(tokens[current_index])=='return':
            s.pop()
            s.push("return_end")
            s.push("return")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="return_end":
        if tokens[current_index].type=='identifier' or tokens[current_index].type=='number' or peek(tokens[current_index])=='-' or peek(tokens[current_index])=='(':
            s.pop()
            s.push(";")
            s.push("expression")
            ##s.print_s()
        elif peek(tokens[current_index])==';':
            if match(peek(tokens[current_index]),';'):
                current_index+=1
                s.pop()
        else:
            flag=False
            break
    elif s.peek()=="break_statement":
        if peek(tokens[current_index])=='break':
            if match(peek(tokens[current_index]),'break') and match(peek(tokens[current_index+1]),';'):
                current_index+=2
                s.pop()
        else:
            flag=False
            break

    elif s.peek()=="continue_statement":
        if peek(tokens[current_index])=='continue':
            if match(peek(tokens[current_index]),'continue') and match(peek(tokens[current_index+1]),';'):
                current_index+=2
                s.pop()
        else:
            flag=False
            break
    elif s.peek()=="expression":
        if tokens[current_index].type=='identifier' or tokens[current_index].type=='number' or peek(tokens[current_index])=='-' or peek(tokens[current_index])=='(':
            s.pop()
            s.push("expr_end")
            s.push("term")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="expr_end":
        if peek(tokens[current_index])=='+' or peek(tokens[current_index])=='-':
            s.pop()
            s.push("expr_end")
            s.push("term")
            s.push("addop")
            ##s.print_s()
        elif peek(tokens[current_index]) in expr_end_list :
            s.pop()
        else:
            flag=False
            break
    elif s.peek()=="addop":
        if peek(tokens[current_index])=='+':
            if match(peek(tokens[current_index]),'+'):
                current_index+=1
                s.pop()
        elif peek(tokens[current_index])=='-':
            if match(peek(tokens[current_index]),'-'):
                current_index+=1
                s.pop()
        else:
            flag=False
            break
    elif s.peek()=="term":
        if tokens[current_index].type=='identifier' or tokens[current_index].type=='number' or peek(tokens[current_index])=='-' or peek(tokens[current_index])=='(':
            s.pop()
            s.push("term_end")
            s.push("factor")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="term_end":
        if peek(tokens[current_index])=='*' or peek(tokens[current_index])=='/':
            s.pop()
            s.push("term_end")
            s.push("factor")
            s.push("mulop")
            ##s.print_s()
        elif peek(tokens[current_index]) in term_end_list:
            s.pop()
        else:
            flag=False
            break
    elif s.peek()=="mulop":
        if peek(tokens[current_index])=='*':
            if match(peek(tokens[current_index]),'*'):
                 current_index+=1
                 s.pop()
        elif peek(tokens[current_index])=='/':
            if match(peek(tokens[current_index]),'/'):
                current_index+=1
                s.pop()
        else:
            flag=False
            break
    elif s.peek()=="factor":
        if tokens[current_index].type=='identifier':
            s.pop()
            s.push("id_fac")
            s.push("id")
            ##s.print_s()
        elif tokens[current_index].type=='number':
            if match(tokens[current_index].type,'number'):
                current_index+=1
                s.pop()
        elif peek(tokens[current_index])=='-':
            if match(peek(tokens[current_index]),'-') and match(tokens[current_index+1].type,'number'):
                current_index+=2
                s.pop()
        elif peek(tokens[current_index])=='(':
            s.pop()
            s.push(")")
            s.push("expression")
            s.push("(")
            ##s.print_s()
        else:
            flag=False
            break
    elif s.peek()=="id_fac":
        if peek(tokens[current_index])=='[':
            s.pop()
            s.push("]")
            s.push("expression")
            s.push("[")
            ##s.print_s()
        elif peek(tokens[current_index])=='(':
            s.pop()
            s.push(")")
            s.push("expr_list")
            s.push("(")
            ##s.print_s()
        elif peek(tokens[current_index]) in id_fac_list:
            ##print("id_fac empty")
            s.pop()
        else:
            flag=False
            break
    elif s.peek() in terminals:
        ##print("---find (")
        ##print peek(tokens[current_index])
        if match(s.peek(), peek(tokens[current_index])):
            s.pop()
            current_index+=1
        else:
            flag=False
            break
    elif s.peek() in key:
        if match(s.peek(),peek(tokens[current_index])):
            s.pop()
            ##print("printf ffffff")
            current_index+=1
        else:
            flag=False
            break

function1=remove_dup(functions)
if flag==True:
    print("Pass")
if flag==False:
    print("Error")

print("Variables: "+ str(variable_num))
print ("Functions: "+ str(len(function1)))
print function1
print ("Statements: "+str(statements))
