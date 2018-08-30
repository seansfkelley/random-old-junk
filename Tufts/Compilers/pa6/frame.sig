signature FRAME =
sig 
    type frame
    type access
    
    type register = {name: string, temp: Temp.temp}
        
    datatype frag = PROC of {body: Tree.stm, frame: frame}
                  | STRING of Temp.label * string
    

    
    val FP : Temp.temp 
    val RV : Temp.temp
    val wordSize : int
    
    val divoverflowreg : Temp.temp
    
    val specialregs : register list
    val argregs : register list
    val calleesaves : register list
    val callersaves : register list
    
    val tempMap : register Temp.Table.table
    
    
    val exp : access -> Tree.exp -> Tree.exp
    val newFrame : {name: Temp.label, formals: bool list} -> frame
    val name : frame -> Temp.label
    val formals : frame -> access list
    val paramregs : frame -> Temp.temp list
    val allocLocal : frame -> bool -> access
    val allocParam : frame * int -> bool -> access
    val procEntryExit1 : frame * Tree.stm -> Tree.stm
    val procEntryExit3 : frame * Assem.instr list -> {prolog : string, body : Assem.instr list, epilog : string}
end

