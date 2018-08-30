structure Codegen = struct
    val calldefs = x86Frame.RV :: map #temp x86Frame.callersaves
  
    fun codegen (frame) (stm: T.stm) =
        let
            val ilist = ref nil
            fun emit x = ilist := x :: !ilist
            fun result (gen) = 
                let
                    val t = Temp.newtemp()
                in
                    (gen t; t)
                end
            
            fun offset i = (if i < 0 then "" else "+") ^ Int.toString i
        
            fun munchStm (T.SEQ(a,b)) = (munchStm a; munchStm b)
              | munchStm(T.EXP(T.CALL(T.NAME l, args))) =
                  emit(Assem.OPER{assem = "call " ^ Symbol.name l ^ "\n",
                              src = munchArgs(0, args, x86Frame.argregs),
                              dst = calldefs,
                              jump = NONE})
              | munchStm(T.MOVE(T.TEMP t, T.CALL(T.NAME l, args))) =
                  (emit(Assem.OPER{assem = "call " ^ Symbol.name l ^ "\n",
                              src = munchArgs(0, args, x86Frame.argregs),
                              dst = calldefs,
                              jump = NONE});
                   emit(Assem.MOVE{assem = "mov `d0, `s0\n",
                                   src = x86Frame.RV,
                                   dst = t}))
              | munchStm(T.MOVE(T.MEM(e1),T.MEM(e2))) =
                  let
                      val r = Temp.newtemp()
                  in
                      emit(Assem.MOVE{assem = "mov `d0, [`s0] \n",
                                  src = munchExp e2,
                                  dst = r});
                      emit(Assem.MOVE{assem = "mov [`d0], `s0\n",
                                  src = r,
                                  dst = munchExp e1})
                  end
              | munchStm (T.MOVE(T.MEM(T.BINOP(T.PLUS, e1, T.CONST i)),e2)) =
                  emit(Assem.OPER{assem = "mov [`s0" ^ offset i ^ "], `s1 \n",
                              src = [munchExp e1, munchExp e2],
                              dst = [],
                              jump = NONE})
              | munchStm(T.MOVE(T.MEM(T.BINOP(T.PLUS, T.CONST i, e1)),e2)) =
                  emit(Assem.OPER{assem = "mov [`s0" ^ offset i ^ "], `s1 \n",
                              src = [munchExp e1, munchExp e2],
                              dst = [],
                              jump = NONE})
              | munchStm(T.MOVE(T.MEM(T.CONST i), e1)) =
                  emit(Assem.OPER{assem = "mov [" ^ offset i ^ "], `s0\n",
                              src = [munchExp e1],
                              dst = [],
                              jump = NONE})
              | munchStm(T.MOVE(T.MEM(e1),e2)) =
                  emit(Assem.OPER{assem = "mov [`s0], `s1\n",
                              src = [munchExp e1, munchExp e2],
                              dst = [],
                              jump = NONE}) 
              | munchStm(T.MOVE(T.TEMP i, e1)) =
                  emit(Assem.MOVE{assem = "mov `d0, `s0\n",
                              src = munchExp e1,
                              dst = i})
              | munchStm(T.LABEL l) =
                  emit(Assem.LABEL{assem = Symbol.name l ^ ":\n", lab = l})
              | munchStm(T.JUMP(T.NAME l, ls)) = 
                               emit(Assem.OPER{assem = "jmp " ^ Symbol.name l ^ "\n", 
                                           src = [],
                                           dst = [],
                                           jump = SOME(ls)})

              | munchStm(T.CJUMP(relop, e1, e2, t, f)) =
                  (emit(Assem.OPER{assem = "cmp `s0, `s1\n",
                              src = [munchExp e1, munchExp e2],
                              dst = [],
                              jump = NONE});
                  emit(Assem.OPER{assem = (case relop of
                                            T.EQ => "je "
                                          | T.NE => "jne "
                                          | T.LT => "jl "
                                          | T.LE => "jle "
                                          | T.GT => "jg "
                                          | T.GE => "jge "
                                          | _ => ErrorMsg.impossible "Undefined relative operator.") ^"`j0\njmp `j1\n",
                              src = [],
                              dst = [],
                              jump = SOME([t, f])}))
              | munchStm(T.EXP e1) = (munchExp(e1); ())
              | munchStm(s) = (Printtree.printtree (TextIO.stdOut, s); ErrorMsg.impossible "Unmatched statement tile.")

            and munchExp(T.MEM(T.BINOP(T.PLUS,e1,T.CONST i))) =         
                    result(fn r => emit(Assem.OPER
                         {assem="mov `d0, [`s0" ^ offset i ^ "]\n",
                          src=[munchExp e1], dst=[r], jump=NONE}))                
              | munchExp(T.MEM(T.BINOP(T.PLUS,T.CONST i,e1))) =         
                    result(fn r => emit(Assem.OPER
                         {assem="mov `d0, [`s0" ^ offset i ^ "]\n",
                          src=[munchExp e1], dst=[r], jump=NONE}))               
              | munchExp(T.MEM(T.CONST i)) = 
                    result(fn r => emit(Assem.OPER
                          {assem="mov `d0, [" ^ offset i ^ "]\n",
                           src=[], dst=[r], jump=NONE}))                 
              | munchExp(T.MEM(e1)) = 
                    result(fn r => emit(Assem.OPER
                          {assem="mov `d0, [`s0]\n",
                           src=[munchExp e1], dst = [r], jump=NONE}))      
              (* Arithmetic. *)          
              | munchExp(T.BINOP(T.PLUS, e1, T.CONST i)) = 
                     let 
                       val r = munchExp(e1)
                       val rt = Temp.newtemp()
                     in
                       (emit(Assem.MOVE
                        {assem="mov `d0 `s0\n",
                         src=r, dst=rt});
                       emit(Assem.OPER
                        {assem="add `d0, " ^ Int.toString i ^ "\n",
                         src=[rt], dst=[rt], jump=NONE}); rt) 
                     end
              | munchExp(T.BINOP(T.PLUS, T.CONST i, e1)) = 
                    let 
                      val r = munchExp(e1)
                      val rt = Temp.newtemp()
                    in
                      (emit(Assem.MOVE
                       {assem="mov `d0 `s0\n",
                        src=r, dst=rt});
                       emit(Assem.OPER
                       {assem="add `d0, " ^ Int.toString i ^ "\n",
                        src=[rt], dst=[rt], jump=NONE}); rt) 
                    end                        
              | munchExp(T.BINOP(T.PLUS,e1,e2)) = 
                    let 
                      val r1 = munchExp(e1)
                      val r2 = munchExp(e2)
                      val rt = Temp.newtemp()
                    in
                      (emit(Assem.MOVE
                       {assem="mov `d0, `s0\n",
                        src=r1, dst=rt});
                       emit(Assem.OPER
                       {assem="add `d0, `s1\n",
                       src=[rt, r2], dst=[rt], jump=NONE}); rt) 
                    end
              
              | munchExp(T.BINOP(T.MINUS, e1, T.CONST i)) = 
                     let 
                       val r = munchExp(e1)
                       val rt = Temp.newtemp()
                     in
                       (emit(Assem.MOVE
                        {assem="mov `d0, `s0\n",
                         src=r, dst=rt});
                        emit(Assem.OPER
                        {assem="sub `d0, " ^ Int.toString i ^ "\n",
                        src=[rt], dst=[rt], jump=NONE}); rt) 
                     end
              | munchExp(T.BINOP(T.MINUS, T.CONST i, e1)) = 
                    let 
                      val r = munchExp(e1)
                      val rt = Temp.newtemp()
                    in
                      (emit(Assem.MOVE
                       {assem="mov `d0, `s0\n",
                        src=r, dst=rt});
                       emit(Assem.OPER
                       {assem="sub `d0, " ^ Int.toString i ^ "\n",
                        src=[rt], dst=[rt], jump=NONE}); rt) 
                    end                        
              | munchExp(T.BINOP(T.MINUS,e1,e2)) = 
                    let 
                      val r1 = munchExp(e1)
                      val r2 = munchExp(e2)
                      val rt = Temp.newtemp()
                    in
                      (emit(Assem.MOVE
                       {assem="mov `d0, `s0\n",
                        src=r1, dst=rt});
                       emit(Assem.OPER
                       {assem="subq `d0, `s1\n",
                       src=[rt, r2], dst=[rt], jump=NONE}); rt)
                    end
              
              | munchExp(T.BINOP(T.MUL, e1, T.CONST i)) = 
                     let 
                       val r = munchExp(e1)
                       val rt = Temp.newtemp()
                     in
                       (emit(Assem.MOVE
                        {assem="mov `d0, `s0\n",
                         src=r, dst=rt});
                        emit(Assem.OPER
                        {assem="imul `d0, " ^ Int.toString i ^ "\n",
                         src=[rt], dst=[rt], jump=NONE}); rt) 
                     end
              | munchExp(T.BINOP(T.MUL, T.CONST i, e1)) = 
                    let 
                      val r = munchExp(e1)
                      val rt = Temp.newtemp()
                    in
                      (emit(Assem.MOVE
                       {assem="mov `d0, `s0\n",
                        src=r, dst=rt});
                       emit(Assem.OPER
                       {assem="imul `d0, " ^ Int.toString i ^ "\n",
                        src=[rt], dst=[rt], jump=NONE}); rt)
                    end                        
              | munchExp(T.BINOP(T.MUL,e1,e2)) = 
                    let 
                      val r1 = munchExp(e1)
                      val r2 = munchExp(e2)
                      val rt = Temp.newtemp()
                    in
                      (emit(Assem.MOVE
                       {assem="mov `d0, `s0\n",
                        src=r1, dst=rt});
                       emit(Assem.OPER
                       {assem="imul `d0, `s1\n",
                        src=[rt, r2], dst=[rt], jump=NONE}); rt) 
                    end
              | munchExp(T.BINOP(T.DIV,e1,e2)) = 
                    let 
                      val r1 = munchExp(e1)
                      val r2 = munchExp(e2)
                    in
                      (emit(Assem.OPER
                       {assem="mov `d0, `s0\n",
                        src=[r1], dst=[x86Frame.RV], jump=NONE});
                       emit(Assem.OPER
                       {assem="idivq `s1\n",
                        src=[x86Frame.RV, r2], dst=[x86Frame.RV, x86Frame.divoverflowreg], jump=NONE}); x86Frame.RV) 
                    end
              
              | munchExp(T.CONST i) = 
                     result(fn r => emit(Assem.OPER
                           {assem="mov `d0, " ^ Int.toString i ^ "\n",
                            src=[], dst=[r], jump=NONE}))
              | munchExp(T.TEMP t) = t
              | munchExp(T.NAME l) = result(fn r => emit(Assem.OPER
                                            {assem="mov `d0, [" ^ Symbol.name l ^ "]\n",
                                             src=[], dst=[r], jump=NONE}))
              | munchExp(e) = (Printtree.printtree (TextIO.stdOut, T.EXP(e)); ErrorMsg.impossible "Unmatched expression tile.")
            
            and munchArgs(_, [], _) = []
              | munchArgs(6, _, _) = ErrorMsg.impossible "Cannot pass more than 6 arguments to a function or procedure."
              | munchArgs(i, e :: es, {name = name, temp = temp} :: regs) = 
                  (emit(Assem.MOVE{assem = "mov `d0, `s0\n",
                                   src = munchExp e,
                                   dst = temp}); temp) :: munchArgs(i + 1, es, regs)
              | munchArgs(_, _, _) = ErrorMsg.impossible "Error while computing arguments."
        
        in
            (munchStm stm; rev (!ilist))
        end

    fun emitParamMoves(SOME(f)) = 
        let
            val ilist = ref nil
            fun emit x = ilist := x :: !ilist
            fun emitparams(p::ps, r::rs) = (emit(Assem.MOVE{assem = "mov `d0, `s0\n",
                                                            src = r,
                                                            dst = p}); emitparams(ps, rs))
              | emitparams([], _) = ()
              | emitparams(_, _) = ()
        in
            (emitparams(x86Frame.paramregs f, map #temp x86Frame.argregs); rev (!ilist))
        end
      | emitParamMoves(NONE) = []
end