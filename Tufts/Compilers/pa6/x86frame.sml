structure x86Frame : FRAME =
struct
    type register = {name: string, temp: Temp.temp}

    datatype access = InFrame of int | InRegister of Temp.temp
    datatype frame = Frame of Temp.label * access list * Temp.temp list
    
    datatype frag = PROC of {body: Tree.stm, frame: frame}
                  | STRING of Temp.label * string
    
    val FP = Temp.newtemp()
    val RV = Temp.newtemp()
    val wordSize = 4
    
    val divoverflowreg = Temp.newtemp()
    
    val specialregs = [{name = "rbp", temp = FP}, 
                       {name = "rax", temp = RV},
                       {name = "rsp", temp = Temp.newtemp()}]
    val argregs = [{name = "rdi", temp = Temp.newtemp()},
                   {name = "rsi", temp = Temp.newtemp()},
                   {name = "rdx", temp = divoverflowreg},
                   {name = "rcx", temp = Temp.newtemp()},
                   {name = "r8",  temp = Temp.newtemp()},
                   {name = "r9",  temp = Temp.newtemp()}]
    val calleesaves = [{name = "rbx", temp = Temp.newtemp()},
                       {name = "r12", temp = Temp.newtemp()},
                       {name = "r13", temp = Temp.newtemp()},
                       {name = "r14", temp = Temp.newtemp()},
                       {name = "r15", temp = Temp.newtemp()}]
    val callersaves = [{name = "r10", temp = Temp.newtemp()},
                       {name = "r11", temp = Temp.newtemp()}]
    
    val tempMap = 
        let
            fun f({name, temp} :: rs) = Temp.Table.enter(f rs, temp, {name = name, temp = temp})
              | f([]) = Temp.Table.empty
        in
            f (specialregs @ argregs @ calleesaves @ callersaves)
        end
    
    fun exp (access) = 
        case access of 
              InFrame(i) => (fn T.TEMP(fp) => T.MEM(T.BINOP(T.PLUS, T.CONST i, T.TEMP fp))
                              | _ => ErrorMsg.impossible "exp expects frame pointer inside a TEMP")
            | InRegister(t) => (fn T.TEMP(fp) => T.TEMP t
                                 | _ => ErrorMsg.impossible "exp expects frame pointer inside a TEMP")
    
    fun newFrame {name, formals} = 
        let 
            fun formalToAccess (x::xs, {name, temp}::ps) = InRegister(temp) :: formalToAccess(xs, ps)
              | formalToAccess (x::xs, []) = ErrorMsg.impossible "too many parameters defined for function"
              | formalToAccess ([], _) = []
        in
            Frame(name, formalToAccess(formals, argregs), List.tabulate(length formals, fn _ => Temp.newtemp()))
        end
    
    fun name (Frame(l, _, _)) = l
    fun formals (Frame(_, a, _)) = a
    fun paramregs (Frame(_, _, p)) = p
    fun allocLocal (Frame(_, _, _)) = fn (_) => InRegister(Temp.newtemp())
    fun allocParam (Frame(_, _, params), i) = fn(_) => InRegister(List.nth(params, i))
    
    fun procEntryExit1 (frame, body) = body
    fun procEntryExit3 (Frame(l, _, _), body) = {prolog = ";PROCEDURE " ^ Symbol.name l ^ "\n" ^ Symbol.name l ^ ":\nenter 0, 0\n",
                                                 body = body,
                                                 epilog = "leave\nret\n;END " ^ Symbol.name l ^ "\n"}
end

(* 
CM.make "sources.cm";
*)