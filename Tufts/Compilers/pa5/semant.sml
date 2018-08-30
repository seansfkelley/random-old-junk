structure S = Symbol

structure Semant =
struct
    type expty = {exp: Translate.exp, ty: Types.ty}

    type venv = Env.enventry S.table
    type tenv = Types.ty S.table

    val value_env = S.empty
    val type_env = S.empty

    val loop_depth = ref 0

    (* Standard types. *)
    val type_env = S.enter(type_env, S.symbol "int", Types.INT)
    val type_env = S.enter(type_env, S.symbol "string", Types.STRING)

    (* Standard library functions. *)
    val value_env = S.enter(value_env, S.symbol "print",     Env.FunEntry{level = Translate.outermost, label = Temp.namedlabel("print"),     formals = [Types.STRING],                       result = Types.UNIT})
    val value_env = S.enter(value_env, S.symbol "flush",     Env.FunEntry{level = Translate.outermost, label = Temp.namedlabel("flush"),     formals = nil,                                  result = Types.UNIT})
    val value_env = S.enter(value_env, S.symbol "getchar",   Env.FunEntry{level = Translate.outermost, label = Temp.namedlabel("getchar"),   formals = nil,                                  result = Types.STRING})
    val value_env = S.enter(value_env, S.symbol "ord",       Env.FunEntry{level = Translate.outermost, label = Temp.namedlabel("ord"),       formals = [Types.STRING],                       result = Types.INT})
    val value_env = S.enter(value_env, S.symbol "chr",       Env.FunEntry{level = Translate.outermost, label = Temp.namedlabel("chr"),       formals = [Types.INT],                          result = Types.STRING})
    val value_env = S.enter(value_env, S.symbol "size",      Env.FunEntry{level = Translate.outermost, label = Temp.namedlabel("size"),      formals = [Types.STRING],                       result = Types.INT})
    val value_env = S.enter(value_env, S.symbol "substring", Env.FunEntry{level = Translate.outermost, label = Temp.namedlabel("substring"), formals = [Types.STRING, Types.INT, Types.INT], result = Types.STRING})
    val value_env = S.enter(value_env, S.symbol "concat",    Env.FunEntry{level = Translate.outermost, label = Temp.namedlabel("concat"),    formals = [Types.STRING, Types.STRING],         result = Types.STRING})
    val value_env = S.enter(value_env, S.symbol "not",       Env.FunEntry{level = Translate.outermost, label = Temp.namedlabel("not"),       formals = [Types.INT],                          result = Types.INT})
    val value_env = S.enter(value_env, S.symbol "exit",      Env.FunEntry{level = Translate.outermost, label = Temp.namedlabel("exit"),      formals = [Types.INT],                          result = Types.UNIT})
    
    fun enterScope () = loop_depth := !loop_depth + 1
    fun exitScope () = loop_depth := !loop_depth - 1
    
    fun actualType (Types.NAME (s, ref (SOME t))) = actualType t
      | actualType (t) = t
    
    fun checkInt ({exp, ty}, pos) = if ty = Types.INT then true else (ErrorMsg.error pos ("integer expected"); false)
    fun checkIntOrString ({exp, ty}, pos) = if ty = Types.INT orelse ty = Types.STRING then true else (ErrorMsg.error pos ("integer or string expected"); false)
    fun checkTypeEqual (e1, e2, pos) =
        let 
            fun gettype {exp, ty} = ty
        in
            if gettype(e1) = gettype(e2) 
            then true 
            else (ErrorMsg.error pos ("type mismatch"); false)
        end
    
    fun isTypeEquivalent (Types.RECORD(_, _), Types.NIL) = true 
      | isTypeEquivalent (Types.NIL, Types.RECORD(_, _)) = true
      | isTypeEquivalent (t1, t2) = t1 = t2
    
    fun transTy (tenv, A.NameTy(id, pos)) = Types.NAME(id, ref (SOME(case S.look(tenv, id) of
                                                                          SOME t => actualType t
                                                                        | NONE => (ErrorMsg.error pos ("undeclared type " ^ S.name id); Types.UNIT))))
      | transTy (tenv, A.RecordTy(fields)) = Types.RECORD(recordTyHelper(tenv, fields), ref ())
      | transTy (tenv, A.ArrayTy(id, pos)) = Types.ARRAY(case S.look(tenv, id) of
                                                               SOME t => actualType t
                                                             | NONE => (ErrorMsg.error pos ("undeclared array type " ^ S.name id); Types.UNIT),
                                                         ref ())
    
    and recordTyHelper (tenv, {name, escape, typ, pos} :: fields) = (name, case S.look(tenv, typ) of 
                                                                                 SOME t => actualType t
                                                                               | NONE => (ErrorMsg.error pos ("undeclared type in record: " ^ S.name name); Types.UNIT)
                                                                    )
                                                                    :: recordTyHelper(tenv, fields)
      | recordTyHelper (tenv, []) = []
    
    
    fun checkFieldExists (tenv, pos, (fieldname, ty) :: fields, field) = if S.name field = S.name fieldname
                                                                         then ty
                                                                         else checkFieldExists(tenv, pos, fields, field)
      | checkFieldExists (tenv, pos, [], field) = (ErrorMsg.error pos ("no field " ^ S.name field); Types.UNIT)
    
    fun transDecs (level, venv, tenv, A.FunctionDec(fdecs) :: decs, inits, break) = 
          let 
              val {venv, tenv} = transFunDecs(level, venv, tenv, fdecs, break)
          in
              transDecs(level, venv, tenv, decs, inits, break)
          end
      
      | transDecs (level, venv, tenv, A.VarDec{name, escape, typ = NONE, init, pos} :: decs, inits, break) =
          let 
              val init' = transExp(level, venv, tenv, break) init
              val v = Trans.allocLocal(level)(true)
          in
              transDecs(level, S.enter(venv, name, Env.VarEntry{access = v, ty = #ty init'}), tenv, decs, Trans.assignExpAccess(v, #exp init') :: inits, break)
          end

      | transDecs (level, venv, tenv, A.VarDec{name, escape, typ = SOME((id, _)), init, pos} :: decs, inits, break) =
          let 
              val init' = transExp(level, venv, tenv, break) init
              val v = Trans.allocLocal(level)(true)
          in
              if not (isSome(S.look(tenv, id))) 
              then (ErrorMsg.error pos ("undeclared type " ^ S.name id); transDecs(level, venv, tenv, decs, inits, break))
              else
                  if isTypeEquivalent(actualType(valOf(S.look(tenv, id))), #ty init') 
                  then transDecs(level, S.enter(venv, name, Env.VarEntry{access = v, ty = #ty init'}), tenv, decs, Trans.assignExpAccess(v, #exp init') :: inits, break)
                  else (ErrorMsg.error pos ("type mismatch"); transDecs(level, venv, tenv, decs, inits, break))
          end
      
      | transDecs (level, venv, tenv, A.TypeDec(tydecs) :: decs, inits, break) = 
            let
                fun addTyStubs({name, ty, pos}::ts, tenv') = addTyStubs(ts, S.enter(tenv', name, Types.NAME(name, ref NONE)))
                  | addTyStubs([], tenv') = tenv'
                fun transAllTys({name, ty, pos}::ts, tenv', venv') =
                    ((case S.look(tenv', name) of
                          SOME(Types.NAME(_, ty_option)) => ty_option := SOME(transTy(tenv', ty))
                        | SOME(t) => ErrorMsg.impossible "recursive type stubbed to incompatible type" 
                        | NONE =>    ErrorMsg.impossible "recursive type not stubbed"); transAllTys(ts, tenv', venv'))
                  | transAllTys([], tenv', venv') = {tenv = tenv', venv = venv'}
                val {venv, tenv} = transAllTys(tydecs, addTyStubs(tydecs, tenv), venv)
            in 
                transDecs(level, venv, tenv, decs, inits, break)
            end
      
      | transDecs (_, venv, tenv, [], inits, _) = {venv = venv, tenv = tenv, inits = inits}
    
    and transFunDecs (level, venv, tenv, {name, params, result = SOME(id, _), body, pos} :: fdecs, break) = 
        let 
            val result_ty = case S.look(tenv, id) of
                                  SOME t => actualType t
                                | NONE => (ErrorMsg.error pos ("undeclated type" ^ S.name id); Types.UNIT)
            fun transparam{name, escape, typ, pos} = 
                case S.look(tenv, typ) of
                      SOME t => {name = name, ty = actualType t}
                    | NONE => (ErrorMsg.error pos ("undeclared type " ^ S.name name); {name = name, ty = Types.UNIT})
            val params' = (map transparam) params
            val label = Temp.newlabel()
            val level' = Translate.newLevel{parent = level, name = label, formals = map (fn _ => true) params'}
            val venv' = S.enter(venv, name, Env.FunEntry{level = level', label = label, formals = map #ty params', result = result_ty})
            fun enterparam({name, ty}, venv) = S.enter(venv, name, Env.VarEntry{access = Translate.allocLocal(level')(true), ty = ty})
            val venv'' = foldr enterparam venv' params'
            val body' = transExp(level', venv'', tenv, break) body
        in 
            (if isTypeEquivalent(#ty body', result_ty)
                then Trans.procEntryExit{level = level', body = #exp body'}
                else ErrorMsg.error pos ("type mismatch of function result type")
            );
            transFunDecs(level, venv', tenv, fdecs, break)
        end
      | transFunDecs (level, venv, tenv, {name, params, result = NONE, body, pos} :: fdecs, break) =
        let
          fun transparam{name, escape, typ, pos} = 
              case S.look(tenv, typ) of
                    SOME t => {name = name, ty = actualType t}
                  | NONE => (ErrorMsg.error pos ("undeclared type " ^ S.name name); {name = name, ty = Types.UNIT})
          val params' = (map transparam) params
          val label = Temp.newlabel()
          val level' = Translate.newLevel{parent = level, name = label, formals = map (fn _ => true) params'}
          val venv' = S.enter(venv, name, Env.FunEntry{level = level', label = label, formals = map #ty params', result = Types.UNIT})
          fun enterparam({name, ty}, venv) = S.enter(venv, name, Env.VarEntry{access = Translate.allocLocal(level')(true), ty = ty})
          val venv'' = foldr enterparam venv' params'
          val body' = transExp(level', venv'', tenv, break) body
        in
            (if #ty body' = Types.UNIT 
                then Trans.procEntryExit{level = level', body = #exp body'}
                else ErrorMsg.error pos ("procedure does not return unit") 
            );
            transFunDecs(level, venv', tenv, fdecs, break)
        end
      | transFunDecs (level, venv, tenv, [], _) = {venv = venv, tenv = tenv}
    
    and transExp(level, venv, tenv, break) = 
        let 
            fun trexp (A.VarExp(var)) = trvar var
          
              | trexp (A.NilExp) = {exp = Trans.nilExp(), ty = Types.NIL}
          
              | trexp (A.IntExp(i)) = {exp = Trans.intExp i, ty = Types.INT}
              
              | trexp (A.StringExp(s, pos)) = {exp = Trans.stringExp s, ty = Types.STRING}
              
              | trexp (A.CallExp{func, args, pos}) = (case S.look(venv, func) of
                                                           SOME(Env.FunEntry{level, label, formals, result}) => {exp = Trans.callExp(label, map (fn a => #exp (trexp a)) args), ty = result}
                                                         | _ => (ErrorMsg.error pos ("undeclared function " ^ S.name func); {exp = Trans.noOpExp(), ty = Types.UNIT}))
              
              | trexp (A.OpExp{left, oper, right, pos}) =
                let
                    val l = trexp left
                    val r = trexp right
                in
                    (case oper of
                          A.PlusOp =>   (checkInt(l, pos); checkInt(r, pos))
                        | A.MinusOp =>  (checkInt(l, pos); checkInt(r, pos))
                        | A.TimesOp =>  (checkInt(l, pos); checkInt(r, pos))
                        | A.DivideOp => (checkInt(l, pos); checkInt(r, pos))

                        | A.LtOp => (checkIntOrString(l, pos); checkIntOrString(r, pos); checkTypeEqual(l, r, pos))
                        | A.LeOp => (checkIntOrString(l, pos); checkIntOrString(r, pos); checkTypeEqual(l, r, pos))
                        | A.GtOp => (checkIntOrString(l, pos); checkIntOrString(r, pos); checkTypeEqual(l, r, pos))
                        | A.GeOp => (checkIntOrString(l, pos); checkIntOrString(r, pos); checkTypeEqual(l, r, pos))

                        | A.EqOp =>  checkTypeEqual(l, r, pos)
                        | A.NeqOp => checkTypeEqual(l, r, pos)
                    ;
                    {exp = Trans.opExp(#exp l, oper, #exp r), ty = Types.INT})
                end
              
              | trexp (A.RecordExp{fields, typ, pos}) = (case S.look(tenv, typ) of
                                                              SOME t => {exp = Trans.recordExp (map (fn (_, e, _) => #exp (trexp e)) fields), ty = actualType t}
                                                            | NONE => (ErrorMsg.error pos ("undeclared record type " ^ S.name typ); {exp = Trans.noOpExp(), ty = Types.UNIT}))
              
              | trexp (A.SeqExp(exps)) =
                  let
                      fun runexp ((e, _) :: es) = trexp e :: runexp(es)
                        | runexp ([]) = []
                      val exps' = runexp exps
                      val ty' = #ty (hd (rev exps'))
                  in
                      {exp = Trans.seqExp(map (fn e => #exp e) exps'), ty = ty'}
                  end
              
              | trexp (A.AssignExp{var, exp, pos}) = 
                  let 
                      val var' = trvar var
                      val exp' = trexp exp
                  in
                      if isTypeEquivalent(#ty var', #ty exp')
                      then {exp = Trans.assignExp(#exp var', #exp exp'), ty = #ty var'}
                      else (ErrorMsg.error pos ("type mismatch in assignment"); {exp = Trans.noOpExp(), ty = Types.UNIT})
                  end
                  
              | trexp (A.IfExp{test, then', else', pos}) = 
                  let
                      val then'' = trexp then'
                      val test' = trexp test
                  in 
                      case else' of
                            SOME e => let
                                    val else'' = trexp e 
                                    in
                                      if isTypeEquivalent(#ty then'', #ty else'')
                                      then {exp = Trans.ifElseExp(#exp test', #exp then'', #exp else''), ty = #ty then''}
                                      else (ErrorMsg.error pos ("type mismatch between then and else"); {exp = Trans.noOpExp(), ty = Types.UNIT})
                                    end
                          | NONE => {exp = Trans.ifExp(#exp test', #exp then''), ty = Types.UNIT}
                  end
              
              | trexp (A.WhileExp{test, body, pos}) = 
                  let
                      val test' = trexp test
                      val done = Temp.newlabel() 
                      val body' = (enterScope(); transExp (level, venv, tenv, done) body) 
                  in
                      (exitScope();
                       if #ty test' = Types.INT
                       then {exp = Trans.whileExp(#exp test', #exp body', done), ty = Types.UNIT}
                       else (ErrorMsg.error pos ("while loop condition must be an integer"); {exp = Trans.noOpExp(), ty = Types.UNIT}))
                  end
              
              | trexp (A.ForExp{var, escape, lo, hi, body, pos}) = 
                  let
                      val iter_dec = A.VarDec{name = var, escape = ref true, typ = SOME(S.symbol "int", pos), init = lo, pos = pos}
                      val limit_dec = A.VarDec{name = S.symbol ("_" ^ S.name var), escape = ref true, typ = SOME(S.symbol "int", pos), init = hi, pos = pos}
                      val iter_var = A.SimpleVar(var, pos)
                      val limit_var = A.SimpleVar(S.symbol ("_" ^ S.name var), pos) 
                  in
                       trexp (A.LetExp{decs = [iter_dec, limit_dec], 
                                       body = A.WhileExp{test = A.OpExp{left = A.VarExp iter_var, 
                                                                        oper = A.LeOp, 
                                                                        right = A.VarExp limit_var, 
                                                                        pos = pos}, 
                                                         body = A.SeqExp([(body, pos), 
                                                                          (A.AssignExp{var = iter_var,
                                                                                       exp = A.OpExp{left = A.VarExp iter_var,
                                                                                                     oper = A.PlusOp, 
                                                                                                     right = A.IntExp 1,
                                                                                                     pos = pos},
                                                                                       pos = pos}, pos)
                                                                         ]),
                                                         pos = pos},
                                       pos = pos}
                             )
                  end
              
              | trexp (A.BreakExp(pos)) = 
                  if !loop_depth = 0
                  then (ErrorMsg.error pos ("break not inside loop"); {exp = Trans.noOpExp(), ty = Types.UNIT})
                  else {exp = Trans.breakExp(break), ty = Types.UNIT}
              
              | trexp (A.LetExp{decs, body, pos}) =
                  let 
                      val {venv = venv', tenv = tenv', inits = inits'} = transDecs(level, venv, tenv, decs, [], break)
                      val body' = transExp(level, venv', tenv', break) body
                  in
                      {exp = Trans.letExp(inits', #exp body'), ty = #ty body'}
                  end
                
              | trexp (A.ArrayExp{typ, size, init, pos}) =
                  let
                      val t_array = case S.look(tenv, typ) of
                                     SOME t => actualType t
                                   | NONE => (ErrorMsg.error pos ("undeclared type " ^ S.name typ); Types.UNIT)
                      val size' = trexp size
                      val init' = trexp init
                  in
                      case t_array of
                            Types.ARRAY(ty, unique) => if #ty size' = Types.INT
                                                       then 
                                                           if #ty init' = ty
                                                           then {exp = Trans.arrayExp(#exp init', #exp size'), ty = t_array}
                                                           else (ErrorMsg.error pos ("initialization value doesn't match array element type"); {exp = Trans.noOpExp(), ty = t_array})
                                                       else (ErrorMsg.error pos ("array size must be an integer"); {exp = Trans.noOpExp(), ty = t_array})
                          | _ => (ErrorMsg.error pos (S.name typ ^ " must be an array type"); {exp = Trans.noOpExp(), ty = Types.UNIT})
                  end

            and trvar (A.SimpleVar(id, pos)) =
                (case S.look(venv, id) of
                      SOME(Env.VarEntry{access, ty}) => {exp = Trans.simpleVar(access, level), ty = actualType ty}
                    | _ => (ErrorMsg.error pos ("undefined variable " ^ S.name id); {exp = Trans.noOpExp(), ty = Types.UNIT}))
              | trvar (A.FieldVar(var, symbol, pos)) = 
                  let
                      val {exp = base, ty = base_ty} = trvar var
                  in
                      case base_ty of
                            Types.RECORD(fieldlist, unique) => {exp = Trans.fieldVar(base, symbol, fieldlist, 0), ty = checkFieldExists(tenv, pos, fieldlist, symbol)}
                          | _ => (ErrorMsg.error pos (S.name symbol ^ " must be a record"); {exp = Trans.noOpExp(), ty = Types.UNIT})
                  end
              | trvar (A.SubscriptVar(var, exp, pos)) = 
                  let 
                      val {exp = base, ty = base_ty} = trvar var
                      val {exp = offset, ty = offset_ty} = trexp exp
                  in 
                      case base_ty of 
                            Types.ARRAY(base_ty, unique) => (checkInt({exp = offset, ty = offset_ty}, pos); {exp = Trans.subscriptVar(base, offset), ty = base_ty})
                          | _ => (ErrorMsg.error pos ("subscripting non-array type"); {exp = Trans.noOpExp(), ty = Types.UNIT})
                  end
        in 
            trexp
        end
    
    fun transProg e = (Printtree.printtree (TextIO.stdOut, Trans.unNx (#exp (transExp(Translate.newLevel{parent = Translate.outermost, name = Temp.newlabel(), formals = []}, value_env, type_env, Temp.newlabel()) e))); Trans.getFragments())

end 
