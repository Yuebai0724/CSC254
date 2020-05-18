Asg 2
Yuebai Gao

The Grammar that I use is:
program → type_name identifier prog_next
prog_next → data_prog type_name identifier func_prog | func_prog
data_prog → id_list_end ; 
id_list_end → ε | , identifier id_list_end
data_decls → ε | type_name id_list ; data_decls
id_list → identifier id_list_end

func_prog → ε | (parameter_list) func_end func_list
func_list → ε | func func_list
func → func_decl func_end
func_end → ;| {data_decls statements}func_decl → type_name identifier ( parameter_list )
type_name → int | voidparameter_list → ε | void void_end | int identifier non_empty_end
void_end → ε | identifier non_empty_end
non_empty_end → ε | , type_name identifier non_empty_end

identifier → id id_end
id_end → ε | [expression] id_end
block_statements → { statements }statements → ε | statement statementsstatement → identifier id_follow | print_func_call | scanf_func_call | if_statement | while_statement | return_statement | break_statement | continue_statementid_follow → = expression; | (expr_list);
print_func_call → printf ( string print_func_call_end
print_func_call_end → ); | ,expression);
scanf_func_call → scanf ( string , &expression ) ;expr_list → ε | non_empty_expr_listnon_empty_expr_list → expression non_empty_expr_end
non_empty_expr_end → ε | ,expression non_empty_expr_end
if_statement → if ( condition_expression ) block_statements if_end
if_end → ε | else block_statements
condition_expression → condition cond_end
cond_end → ε | conditon_op conditioncondition_op → && | ||condition → expression comparison_op expressioncomparison_op → == | != | > | >= | < | <=while_statement → while ( condition_expression ) block_statementsreturn_statement → return return_end
return_end → expression;|;break_statement → break;continue_statement → continue;expression → term expr_end
expr_end → ε | addop term expr_end
addop → + | -term → factor term_end
term_end → ε | mulop factor term_endmulop → * | /
factor → id id_fac | number | -number |(expression)
id_fac → ε |[expression]|(expr_list)

—————————————————————————————————————————————————————————————————

To run the program, type “python parser.py filename.c” in terminal.
Besides Pass/Error, variables, functions and statements, I also print out a list with all function names, just for my own convenience, and you could just ignore it. Thank you so much.


