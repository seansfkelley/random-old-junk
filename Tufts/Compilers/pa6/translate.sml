structure Translate = 
struct 
  
    structure F = x86Frame
    
    datatype level = TopLevel | Level of level * F.frame
    type access = F.access
    
    datatype exp = Ex of T.exp
                 | Nx of T.stm
                 | Cx of Temp.label * Temp.label -> T.stm
    
    val fragmentList : F.frag list ref = ref []
    
    val outermost = TopLevel
    
    fun make_seq (s::[]) = s
       | make_seq (s::stms) = T.SEQ(s, make_seq(stms))
       | make_seq ([]) = ErrorMsg.impossible "making sequence tree from empty list"
    
    fun getFragments () = !fragmentList
    
    fun newLevel {parent, name, formals} = Level(parent, F.newFrame{name = name, formals = formals})
    fun formals (TopLevel) = []
      | formals (Level(_, f)) = F.formals(f)
    fun allocLocal (TopLevel) = ErrorMsg.impossible "cannot allocate local in top level scope"
      | allocLocal (Level(_, f)) = F.allocLocal(f)
    fun allocParam (TopLevel, _) = ErrorMsg.impossible "cannot allocate local in top level scope"
      | allocParam (Level(_, f), i) = F.allocParam(f, i) 
      
    fun noOpExp () = Nx(T.EXP(T.CONST 0))
    
    fun unEx (Ex e) = e
      | unEx (Nx s) = T.ESEQ(s, T.CONST 0)
      | unEx (Cx genstm) = 
           let 
               val r = Temp.newtemp()
               val t = Temp.newlabel()
               val f = Temp.newlabel()
               
           in 
               T.ESEQ(make_seq [T.MOVE(T.TEMP r, T.CONST 1),
                           genstm(t, f),
                           T.LABEL f,
                           T.MOVE(T.TEMP r, T.CONST 0),
                           T.LABEL t],
                      T.TEMP r)
           end
    
    fun unNx (Nx s) = s
      | unNx (Ex e) = T.EXP(e)
      | unNx (Cx genstm) = 
          let
              val l = Temp.newlabel()
          in 
              T.SEQ(genstm(l, l), T.LABEL l)
          end
          
    fun unCx (Cx genstm) = genstm
      (* Error condition Nx. Emit code that does nothing. These will only occur when an error exists elsewhere.*)
      | unCx (Nx(T.EXP(T.CONST 0))) = (fn (_, _) => let 
                                                        val l = Temp.newlabel() 
                                                    in 
                                                        T.SEQ(T.JUMP(T.NAME l, [l]), T.LABEL l)
                                                    end)
      | unCx (Nx _) = ErrorMsg.impossible "cannot convert Nx into Cx"
      | unCx (Ex e) =
          case e of 
                T.CONST 0 => (fn (_, f) => T.JUMP(T.NAME f, [f]))
              | T.CONST 1 => (fn (t, _) => T.JUMP(T.NAME t, [t]))
              | _ => (fn (t, f) => T.CJUMP(T.NE, e, T.CONST 0, t, f))

    fun nilExp () = 
        let
            val r = Temp.newtemp()
        in
            Ex(T.ESEQ(T.MOVE(T.TEMP r, T.CONST 0), T.TEMP r))
        end
    
    fun intExp (i) = Ex(T.CONST i)
    
    fun stringExp (s) = 
        let
            val l = Temp.newlabel()
        in
            (fragmentList := F.STRING(l, s) :: !fragmentList; Ex(T.NAME l))
        end
    
    fun callExp (label, exps) = Ex(T.CALL(T.NAME label, map (fn e => unEx e) exps))
    
    fun procEntryExit {level: level, body: exp} =  
          (case level of
              TopLevel => ErrorMsg.impossible "can not declare functions in top level scope"          
            | Level (level, frame) =>
                let 
                  val stm =  F.procEntryExit1(frame, T.MOVE(T.TEMP F.RV, unEx (body)))
                in
                  fragmentList := F.PROC{body = stm, frame = frame} :: !fragmentList
                end
            ) 
           
    fun opExp (l, oper, r) =
        let 
            val l' = unEx l
            val r' = unEx r
        in  
            case oper of
                 A.PlusOp =>   Ex(T.BINOP(T.PLUS,  l', r'))
               | A.MinusOp =>  Ex(T.BINOP(T.MINUS, l', r'))
               | A.TimesOp =>  Ex(T.BINOP(T.MUL,   l', r'))
               | A.DivideOp => Ex(T.BINOP(T.DIV,   l', r'))
               
               | A.GtOp => Cx(fn (t, f) => T.CJUMP(T.GT, l', r', t, f))  
               | A.GeOp => Cx(fn (t, f) => T.CJUMP(T.GE, l', r', t, f))
               | A.LtOp => Cx(fn (t, f) => T.CJUMP(T.LT, l', r', t, f))
               | A.LeOp => Cx(fn (t, f) => T.CJUMP(T.LE, l', r', t, f))
        
               | A.EqOp =>  Cx(fn (t, f) => T.CJUMP(T.EQ, l', r', t, f))
               | A.NeqOp => Cx(fn (t, f) => T.CJUMP(T.NE, l', r', t, f))
        end                         
  
    fun recordExp (exps) = 
        let 
            val r = Temp.newtemp()
            fun recordExpHelper([e], i) = T.MOVE(T.MEM(T.BINOP(T.PLUS, T.TEMP r, T.CONST (i * F.wordSize))), unEx e)
              | recordExpHelper(e :: es, i) = T.SEQ(T.MOVE(T.MEM(T.BINOP(T.PLUS, T.TEMP r, T.CONST (i * F.wordSize))), unEx e), recordExpHelper (es, i + 1))
              | recordExpHelper([], _) = (ErrorMsg.impossible "allocating memory for empty record"; unNx (noOpExp()))
        in
            Ex(T.ESEQ(T.SEQ(T.MOVE(T.TEMP r, T.CALL(T.NAME (Temp.namedlabel("malloc")), [T.CONST ((length exps) * F.wordSize)])), recordExpHelper(exps, 0)), T.TEMP r))
        end
        
    fun seqExp (exps) = 
        let
            val beginning = rev (tl (rev exps))
            val last = hd (rev exps)
            fun seqExpHelper (e :: es) = if null es
                                         then unNx e
                                         else T.SEQ(unNx e, seqExpHelper es)
              | seqExpHelper ([]) = (ErrorMsg.impossible "sequences must be at least one item long"; unNx (noOpExp()))
        in  
            if length exps = 1
            then Ex(unEx(last))
            else Ex(T.ESEQ(seqExpHelper(beginning), unEx last))
        end
        
    fun assignExp (var, exp) = Nx(T.MOVE(unEx var, unEx exp))
    
    fun assignExpAccess (access, exp) = Nx(T.MOVE((F.exp(access) (T.TEMP F.FP)), unEx exp))
    
    fun ifElseExp (test, Nx(then'), Nx(else')) = 
        let 
            val t = Temp.newlabel()
            val f = Temp.newlabel()
            val join = Temp.newlabel()
        in 
            Nx(make_seq [unCx(test) (t, f),
                        T.LABEL t,
                        then',
                        T.JUMP (T.NAME join, [join]),
                        T.LABEL f,
                        else',
                        T.LABEL join]
               )
        end
      | ifElseExp (test, then', else') = 
        let 
            val r = Temp.newtemp()
            val t = Temp.newlabel()
            val f = Temp.newlabel()
            val join = Temp.newlabel()
        in 
            Ex(T.ESEQ(make_seq [unCx(test) (t, f),
                        T.LABEL t,
                        T.MOVE(T.TEMP r, unEx then'),
                        T.JUMP (T.NAME join, [join]),
                        T.LABEL f,
                        T.MOVE(T.TEMP r, unEx else'),
                        T.LABEL join],
                   T.TEMP r)
               )
        end
        
    fun ifExp (test, then') = 
        let 
            val t = Temp.newlabel()
            val f = Temp.newlabel()
        in 
            Nx(make_seq [unCx(test) (t, f),
                        T.LABEL t,
                        unNx then',
                        T.LABEL f]
               )
        end
        
    fun whileExp(test, exp, done) = 
        let
            val body = Temp.newlabel()
        in
            Nx(make_seq [unCx(test) (body, done),
                         T.LABEL body,
                         unNx exp,
                         unCx(test) (body, done),
                         T.LABEL done]
              )
            
        end
    
    fun breakExp (done) = Nx(T.JUMP (T.NAME done, [done]))

    fun letExp (inits, exp) = Ex(T.ESEQ(make_seq (map (fn i => unNx i) inits), unEx exp))
    
    fun arrayExp(init, size) = 
        let 
            val r = Temp.newtemp()
        in
            Ex(T.ESEQ(T.MOVE(T.TEMP r, T.CALL(T.NAME (Temp.namedlabel("arrayInit")), [unEx init, unEx size])), T.TEMP r))
        end
    
    fun simpleVar (access, level) =
        case level of
              TopLevel => ErrorMsg.impossible "cannot have local variables in top level scope"
            | Level(l, f) => Ex(F.exp(access) (T.TEMP F.FP))

    fun fieldVar (Ex(T.MEM e), n, (fname, fty)::fs, offset) = if Symbol.name n = Symbol.name fname
                                                              then Ex(T.MEM(T.BINOP(T.PLUS, e, T.CONST offset)))
                                                              else fieldVar(Ex(T.MEM(e)), n, fs, offset + F.wordSize)
      | fieldVar (Ex(T.TEMP t), n, (fname, fty)::fs, offset) = if Symbol.name n = Symbol.name fname
                                                               then Ex(T.MEM(T.BINOP(T.PLUS, T.TEMP t, T.CONST offset)))
                                                               else fieldVar(Ex(T.TEMP t), n, fs, offset + F.wordSize)
      | fieldVar (_, _, [], _) = ErrorMsg.impossible "could not locate field in record"
      | fieldVar (_, _, _, _) = ErrorMsg.impossible "field expects ([MEM or TEMP], symbol, fields, offset)"

    fun subscriptVar (Ex(T.MEM e), offset) =  Ex(T.MEM(T.BINOP(T.PLUS, e, T.BINOP(T.MUL, T.CONST F.wordSize, unEx offset))))
      | subscriptVar (Ex(T.TEMP t), offset) = Ex(T.MEM(T.BINOP(T.PLUS, T.TEMP t, T.BINOP(T.MUL, T.CONST F.wordSize, unEx offset))))  
      | subscriptVar (_, _) = ErrorMsg.impossible "subscript expects ([MEM or TEMP], Ex)"
    
end

structure Trans = Translate

(*
CM.make "sources.cm";
*)
