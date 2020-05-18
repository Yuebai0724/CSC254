#!/usr/bin/ruby

require_relative 'scanner.rb'

class Function
    attr_accessor :code, :num_vars, :num_labels, :symtab
    def initialize
       @code= ""
       @num_vars= 0
       @num_labels= 0
       @symtab= {}
    end

    def new_var
      @num_vars+=1
      return "local["+ (@num_vars-1).to_s+ "]"
    end

    def new_label
      @num_labels+=1
      return "L"+@num_labels.to_s
    end

    def sym_tab
      @symtab
    end

    def append_code(str)
      @code=@code+str
    end

    def add_param(name)
      @symtab[name] = new_var
      str=@symtab[name] + " = " + name + ";\n"
      append_code (str)
    end
end


class Parser
  class ParseError < StandardError
  end

  attr_reader :type_count

  def initialize(input_file)
    @scanner = Scanner.new(input_file)
    @type_count = {
      variable: 0,
      function: 0,
      statement: 0
    }
    @num_global_vars = 0
    @global_vars = []
    @global_sym_tab = {}
    @functions = {}
    @prog_code = ""
    @output_file = File.new("output.c", "w")
    @loop_exit_label = ""
    @loop_begin_label = ""
  end
  def write(str)
    @output_file.syswrite(str)
  end

  def parse
    return false if skip_meta_statements
    program
    match(:eof)
    write("int global[#{@num_global_vars}];\n") unless @num_global_vars == 0
    write(@prog_code)
    @output_file.close
    true
  end

  def new_global_var
    @num_global_vars += 1;
    @global_vars << "global[#{@num_global_vars-1}]"
    return "global[#{@num_global_vars-1}]"
  end

  def tokArrayIncl?(arr, tok)
    for t in arr
      if t.type == tok.type and t.value == tok.value
        return true
      end
    end
    return false
  end

  def match(tokens)
    fail ParseError, "Unexpected token #{@scanner.peek}, expected #{tokens}" unless
      case tokens
      when Symbol
        tokens == @scanner.peek.type
      when Token
	      tokens.type == @scanner.peek.type and tokens.value == @scanner.peek.value
      when Array
        tokArrayIncl?(tokens, @scanner.peek)
      else
        fail ArgumentError, 'Not a symbol or array'
      end

    @scanner.next
    skip_meta_statements
  end

  # Skip meta statements as they are not part of the grammar
  def skip_meta_statements
    while @scanner.peek.type == :comment
	    write("#{@scanner.peek.value}\n")
	    @scanner.next
    end
  rescue StopIteration
    false
  end

  def semicolon
    match(Token.new(:symbol, ';'))
  end


  def comma
    match(Token.new(:symbol, ','))
  end

  # <program> --> void ID ( <parameter_list> ) <func_tail> <func_list>
  #             | int ID <program_tail>
  #             | epsilon
  def program
    case @scanner.peek.value
    when 'void'
      @prog_code << "#{@scanner.next.value} "
      fn_name = "#{@scanner.next.value}"
      @prog_code << "#{fn_name}"
      @functions[fn_name] = Function.new unless @functions[fn_name] != nil
      @global_sym_tab[fn_name] = fn_name
      fn = @functions[fn_name]
      @prog_code << "#{@scanner.next.value}"
      parameter_list(fn)
      @prog_code << "#{@scanner.next.value}"
      func_tail(fn)
      func_list

    when 'int'
      @scanner.next
      name = "#{@scanner.next.value}"
      program_tail(name)

    end
  end

  # <program_tail> --> ( <parameter_list> ) <func_tail> <func_list>
  #                  | <program_decl_tail>
  def program_tail(name)
    if @scanner.peek.value == '('
      @prog_code << "int #{name}"
      @functions[name] = Function.new unless @functions[name] != nil
      @global_sym_tab[name] = name
      fn = @functions[name]
      @prog_code << "#{@scanner.next.value}"
      parameter_list(fn)
      @prog_code << "#{@scanner.next.value}"

      func_tail(fn)
      func_list
    else
      program_decl_tail(name)
    end
  end

  # <program_decl_tail> --> , <id_list> ; <program>
  #                       | ; <program>
  def program_decl_tail(name)
    @global_sym_tab[name] = new_global_var
    case @scanner.peek.value
    when ','
      comma
      global_id_list
      semicolon
      program
    when ';'
      semicolon
      program
    else
      fail ParseError, "Expected , or ;, found #{@scanner.peek.value}"
    end
    @type_count[:variable] += 1
  end

  # <func_list> --> <func> <func_list>
  #               | epsilon
  def func_list
    if %w(int void).include? @scanner.peek.value
      func
      func_list
    end
  end

  # <func> --> <func_decl> <func_tail>
  def func
    fn = func_decl
    func_tail(fn)
  end

  # <func_tail> --> ;
  #               | { <data_decls> <statements> }
  def func_tail(fn)
    case @scanner.peek.value
    when ';'
      semicolon
      @prog_code << ";\n"
    when '{'

      match(Token.new(:symbol, '{'))
      @prog_code << "{\n"
      @type_count[:function] += 1
      data_decls(fn)
      statements(fn)
      match(Token.new(:symbol, '}'))
      @prog_code << "int local[#{fn.num_vars}];\n" unless fn.num_vars == 0
      @prog_code << fn.code
      @prog_code << "}\n"
    else
      fail ParseError, "Expected ; or {, found #{@scanner.peek.value}"
    end
  end

  # <func_decl> --> <type_name> ID ( <parameter_list> )
  def func_decl
    @prog_code << "#{type_name} "

    fn_name = @scanner.next.value unless @scanner.peek.type != :identifier

    @prog_code << "#{fn_name}"
    @functions[fn_name] = Function.new unless @functions[fn_name] != nil
    @global_sym_tab[fn_name] = fn_name
    fn = @functions[fn_name]
    @prog_code << "#{@scanner.next.value}"
    parameter_list(fn)
    @prog_code << "#{@scanner.next.value}"

    return @functions[fn_name]
  end

  # <type_name> --> int
  #               | void
  def type_name
    if @scanner.peek.value == 'int'
	    t = 'int'
    elsif @scanner.peek.value == 'void'
	    t = 'void'

    end
    match(Token.new(:reserved, t))
    t
  end

  # <parameter_list> --> void
  #                    | int ID <parameter_list_tail>
  #                    | epsilon
  def parameter_list(fn)
    case @scanner.peek.value
    when 'void'
      match(Token.new(:reserved, 'void'))
      @prog_code << "void"
    when 'int'
      match(Token.new(:reserved, 'int'))
      @prog_code << "int "
      name = @scanner.next.value
      fn.add_param(name)
      @prog_code << name
      parameter_list_tail(fn)
    end
  end

  # <parameter_list_tail> --> , int ID <parameter_list_tail>
  #                         | epsilon
  def parameter_list_tail(fn)
    if @scanner.peek.value == ','
      comma
      @prog_code << ','
      match(Token.new(:reserved, 'int'))
      @prog_code << "int "
      name = @scanner.next.value
      fn.add_param(name)
      @prog_code << name
      parameter_list_tail(fn)
    end
  end

  # <data_decls> --> int <id_list> ; <data_decls>
  #                | epsilon
  def data_decls(fn)
    if @scanner.peek.value == 'int'
      match(Token.new(:reserved, 'int'))
      id_list(fn)
      semicolon
      data_decls(fn)
    end
  end

  # <id_list> --> ID  <id_list_tail>
  def id_list(fn)
    @type_count[:variable] += 1
    fn.sym_tab[@scanner.next.value] = fn.new_var
    id_list_tail(fn)
  end

  # <id_list_tail> --> , <id_list>
  #                  | epsilon
  def id_list_tail(fn)
    if @scanner.peek.value == ','
      comma
      id_list(fn)
    end
  end

  def global_id_list
    @global_sym_tab[@scanner.next.value] = new_global_var
    global_id_list_tail
  end
  def global_id_list_tail
    if @scanner.peek.value == ','
      comma
      global_id_list
    end
  end
  # <block_statements> --> { <statements> }
  def block_statements(fn)
    match(Token.new(:symbol, '{'))
    #fn.code << "#{statements(fn)}"
    statements(fn)
    match(Token.new(:symbol, '}'))
  end

  # <statements> --> <statement> <statements>
  #                | epsilon
  def statements(fn)
    if %i(identifier reserved).include? @scanner.peek.type
      @type_count[:statement] += 1
      statement(fn)
      statements(fn)
    end
  end

  # <statement> --> <break_statement>
  #               | <continue_statement>
  #               | <if_statement>
  #               | <printf_func_call>
  #               | <return_statement>
  #               | <scanf_func_call>
  #               | <while_statement>
  #               | ID <statement_tail>
  def statement(fn)
    case @scanner.peek.value
    when 'break'
      break_statement(fn)
    when 'continue'
      continue_statement(fn)
    when 'if'
      if_statement(fn)
    when 'printf'
      printf_func_call(fn)
    when 'return'
      return_statement(fn)
    when 'scanf'
      scanf_func_call(fn)
    when 'while'
      while_statement(fn)
    else
      name = @scanner.next.value
      st_left = fn.sym_tab[name]
      if st_left == nil
	      st_left = @global_sym_tab[name]
      end
      if st_left == nil
	      st_left = name
      end
      code = "#{st_left}#{statement_tail(fn, st_left)}"
      fn.code << code
      code

    end
  end

  # <statement_tail> --> <general_func_call>
  #                    | <assignment>
  def statement_tail(fn, st_left)
    if @scanner.peek.value == '('
      "#{general_func_call(fn)}"
    else
      "#{assignment(fn)}"
    end
  end

  # <general_func_call> --> ( <expr_list> ) ;
  def general_func_call(fn)
    "#{@scanner.next.value} #{expr_list(fn)} #{@scanner.next.value}#{@scanner.next.value}\n"

  end

  # <assignment> -->  = <expression> ;
  def assignment(fn)
    "#{@scanner.next.value} #{expression(fn)}#{@scanner.next.value}\n"
  end

  # <printf_func_call> --> printf ( string <print_func_call_tail>
  def printf_func_call(fn)

    fn.code << "#{@scanner.next.value}#{@scanner.next.value}#{@scanner.next.value}#{printf_func_call_tail(fn)}"
  end

  # <printf_func_call_tail> --> ) ;
  #                           | , <expression> ) ;
  def printf_func_call_tail(fn)
    case @scanner.peek.value
    when ','
      "#{@scanner.next.value} #{expression(fn)} #{@scanner.next.value} #{@scanner.next.value}\n"

    when ')'
      "#{@scanner.next.value}#{@scanner.next.value}\n"
    else
      fail ParseError, "Expected ',' or ')'. Found #{@scanner.peek}"
    end
  end

  # <scanf_func_call> --> scanf ( string , & <expression> ) ;
  def scanf_func_call(fn)
    text = "scanf("
    match(Token.new(:reserved, 'scanf'))
    match(Token.new(:symbol, '('))
    text << "#{@scanner.next.value}, &"
    comma
    match(Token.new(:symbol, '&'))
    #match(Token.new(:symbol, '&'))
    text << "#{expression(fn)});\n"
    match(Token.new(:symbol, ')'))
    semicolon
    fn.code << text
  end

  def in_first_of_expression
    case @scanner.peek.type
    when :identifier, :number
      true
    when :symbol
      ['(', '-'].include? @scanner.peek.value
    else
      false
    end
  end

  # <expr_list> --> <expression> <expr_list_tail>
  #               | epsilon
  def expr_list(fn)
    if in_first_of_expression
      "#{expression(fn)} #{expr_list_tail(fn)}"

    else
      ""
    end
  end

  # <expr_list_tail> --> , <expression> <expr_list_tail>
  #                    | epsilon
  def expr_list_tail(fn)
    if @scanner.peek.value == ','
      "#{@scanner.next.value} #{expression(fn)} #{expr_list_tail(fn)}"
    else
      ""
    end
  end

  # <if_statement> --> if ( <condition_expression> ) <block_statements>
  #                       <else_statement>
  def if_statement(fn)
    match(Token.new(:reserved, 'if'))
    match(Token.new(:symbol, '('))
    tf = condition_expression(fn)
    match(Token.new(:symbol, ')'))
    is_nxt = fn.new_label
    is_else = tf[1]
    fn.code << "#{tf[0]}:;\n"
    #fn.code << block_statements(fn)
    block_statements(fn)
    fn.code << "goto #{is_nxt};\n"
    else_statement(fn, tf[1], is_nxt)

  end

  # <else_statement> --> else <block_statements>
  #                    | epsilon
  def else_statement(fn, ce_false, is_nxt)
    if @scanner.peek.value == 'else'
      match(Token.new(:identifier, 'else'))
      fn.code << "#{ce_false}:;\n"
      block_statements(fn)
      fn.code << "#{is_nxt}:;\n"

    else
      fn.code << "#{is_nxt}:;\n"
      fn.code << "#{ce_false}:;\n"
    end
  end

  # <condition_expression> --> <condition> <condition_expression_tail>
  def condition_expression(fn, true_label = fn.new_label, false_label = fn.new_label)
    condition_expression_tail(fn, condition(fn), true_label, false_label)
    [true_label, false_label]

  end

  # <condition_expression_tail> --> <condition_op> <condition>
  #                               | epsilon
  def condition_expression_tail(fn, cond1, label_true, label_false)
    case @scanner.peek.value
    when "||"
      @scanner.next
      fn.code << "if (#{cond1}) goto #{label_true};\n"
      fn.code << "if (#{condition(fn)}) goto #{label_true};\n"
      fn.code << "goto #{label_false};\n"
    when "&&"
      @scanner.next
      lbl = fn.new_label
      fn.code << "if (#{cond1}) goto #{lbl};\n"
      fn.code << "goto #{label_false};\n"
      fn.code << "#{lbl}:;\n"
      fn.code << "if (#{condition(fn)}) goto #{label_true};\n"
      fn.code << "goto #{label_false};\n"

    else
      fn.code << "if (#{cond1}) goto #{label_true};\n"
      fn.code << "goto #{label_false};\n"
    end
  end

  # <condition_op> --> &&
  #                  | ||
  def condition_op
    match(%w(&& ||).map { |t| Token.new(:symbol, t) })
  end

  # <condition> --> <expression> <comparison_op> <expression>
  def condition(fn)
    exp1 = expression(fn)
    unless %w(== != > >= < <=).include?(@scanner.peek.value)
	    raise "Improperly formed condition. (peek = #{@scanner.peek.value})"
    end
    comp = @scanner.next.value
    exp2 = expression(fn)
    return "#{exp1} #{comp} #{exp2}"

  end

  # <comparison_op> --> == | != | > | >=| <| <=
  def comparison_op
    match(%w(== != > >= < <=).map { |t| Token.new(:symbol, t) })
  end

  # <while_statement> --> while ( <condition_expression> ) <block_statements>
  def while_statement(fn)
    bgn = fn.new_label
    @loop_begin_label = bgn
    match(Token.new(:reserved, 'while'))
    match(Token.new(:symbol, '('))
    fn.code << "#{bgn}:;\n"
    tf = condition_expression(fn)
    @loop_exit_label = tf[1]
    match(Token.new(:symbol, ')'))
    fn.code << "#{tf[0]}:;\n"
    block_statements(fn)
    fn.code << "goto #{bgn};\n"
    fn.code << "#{tf[1]}:;\n"

  end

  # <return_statement> --> return <return_statement_tail>
  def return_statement(fn)
    unless @scanner.peek.value != 'return'
      fn.code << "#{@scanner.next.value} #{return_statement_tail(fn)}"
    end
  end

  # <return_statement_tail> --> <expression> ;
  #                           | ;
  def return_statement_tail(fn)
    if @scanner.peek.value != ';'
      "#{expression(fn)} #{@scanner.next.value}"
    else
      "#{@scanner.next.value}"
    end
  end

  # <break_statement> ---> break ;
  def break_statement(fn)
    match(Token.new(:reserved, 'break'))
    semicolon
    fn.code << "goto #{@loop_exit_label};\n"
  end

  # <continue_statement> ---> continue ;
  def continue_statement(fn)
    match(Token.new(:reserved, 'continue'))
    semicolon
    fn.code << "goto #{@loop_begin_label};\n"
  end

  # <expression> --> <term> <expression_tail>
  def expression(fn)
    expression_tail(fn, term(fn))
  end

  # <expression_tail> --> <addop> <term> <expression_tail>
  #                     | epsilon
  def expression_tail(fn, e1_left)
    if %w(+ -).include? @scanner.peek.value
      e1_place = fn.new_var
      fn.code << "#{e1_place} = #{e1_left} #{@scanner.next.value} #{term(fn)};\n"
      expression_tail(fn, e1_place)
    else
      e1_left
    end
  end

  # <addop> --> +
  #           | -
  def addop
    match(%w(+ -).map { |t| Token.new(:symbol, t) })
  end

  # <term> --> <factor> <term_tail>
  def term(fn)
    term_tail(fn, factor(fn))
  end

  # <term_tail> --> <mulop> <factor> <term_tail>
  #               | epsilon
  def term_tail(fn, t1_left)
    if %w(* /).include? @scanner.peek.value
      t1_place = fn.new_var
      fn.code << "#{t1_place} = #{t1_left} #{@scanner.next.value} #{term(fn)};\n"
      term_tail(fn, t1_place)
    else
      t1_left
    end
  end

  # <mulop> --> *
  #           | /
  def mulop
    match(%w(* /).map { |t| Token.new(:symbol, t) })
  end

  # <factor> --> ID <factor_tail>
  #            | NUMBER
  #            | - NUMBER
  #            | ( <expression> )
  def factor(fn)
    case @scanner.peek.type
    when :number
      f_place = fn.new_var
      fn.code << "#{f_place} = #{@scanner.next.value};\n"
      f_place
    when :symbol
      case @scanner.peek.value
      when '('
	f_place = fn.new_var
        match(Token.new(:symbol, '('))
        fn.code << "#{f_place} = #{expression(fn)};\n"
	match(Token.new(:symbol, ')'))
	f_place
      when '-'
	f_place = fn.new_var
	fn.code << "#{f_place} = #{@scanner.next.value}#{@scanner.next.value};\n"
        f_place
      else
        fail ParseError, "Unexpected token #{@scanner.peek}"
      end
    when :identifier
      name = @scanner.next.value
      if fn.sym_tab[name] != nil
	      return "#{fn.sym_tab[name]}#{factor_tail(fn)}"
      else
	      return "#{@global_sym_tab[name]}#{factor_tail(fn)}"
      end
    else
      fail ParseError, "Unexpected token #{@scanner.peek}"
    end
  end

  # <factor_tail> --> ( <expr_list> )
  #                 | epsilon
  def factor_tail(fn)
    if @scanner.peek.type == :symbol
      if @scanner.peek.value == '('
        match(Token.new(:symbol, '('))
        ft_place = expr_list(fn)
        match(Token.new(:symbol, ')'))
	return "(#{ft_place})"
      else
	return ""
      endi
    end
  end
end

p = Parser.new(ARGV[0])
p.parse
end
