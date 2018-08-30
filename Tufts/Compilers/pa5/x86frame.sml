structure x86Frame : FRAME =
struct
    datatype access = InFrame of int | InRegister of Temp.temp
    datatype frame = Frame of Temp.label * access list
    
    datatype frag = PROC of {body: Tree.stm, frame: frame}
                  | STRING of Temp.label * string
    
    val FP = Temp.newtemp()
    val RV = Temp.newtemp()
    val wordSize = 4
    
    fun exp (access) = 
        case access of 
              InFrame(i) => (fn T.TEMP(fp) => T.MEM(T.BINOP(T.PLUS, T.CONST i, T.TEMP fp))
                              | _ => ErrorMsg.impossible "exp expects frame pointer inside a TEMP")
            | InRegister(t) => (fn T.TEMP(fp) => T.MEM(T.TEMP t)
                                 | _ => ErrorMsg.impossible "exp expects frame pointer inside a TEMP")
    
    fun newFrame {name, formals} = 
        let 
            fun formalToAccess (x::xs) = 
                let
                    val fs = formalToAccess xs
                in
                    InFrame(case (hd fs) of 
                                  InFrame(i) => i + 4
                                | InRegister(_) => ErrorMsg.impossible "parameters don't live in registers"
                            ) :: fs
                end
              | formalToAccess [] = [InFrame(4)]
        in
            Frame(name, tl (rev (formalToAccess (rev formals))))
        end
    
    fun name (Frame(l, _)) = l
    fun formals (Frame(_, a)) = a
    fun allocLocal (Frame(_, _)) = fn (_) => InRegister(Temp.newtemp())
    fun procEntryExit1 (frame, body) = body
end

(* 
CM.make "sources.cm";
*)