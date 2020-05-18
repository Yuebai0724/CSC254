
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
      return "local["+@num_vars.to_s+"]"
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
