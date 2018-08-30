structure A = Absyn
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
    val value_env = S.enter(value_env, S.symbol "print",     Env.FunEntry{formals = [Types.STRING],                       result = Types.UNIT})
    val value_env = S.enter(value_env, S.symbol "flush",     Env.FunEntry{formals = nil,                                  result = Types.UNIT})
    val value_env = S.enter(value_env, S.symbol "getchar",   Env.FunEntry{formals = nil,                                  result = Types.STRING})
    val value_env = S.enter(value_env, S.symbol "ord",       Env.FunEntry{formals = [Types.STRING],                       result = Types.INT})
    val value_env = S.enter(value_env, S.symbol "chr",       Env.FunEntry{formals = [Types.INT],                          result = Types.STRING})
    val value_env = S.enter(value_env, S.symbol "size",      Env.FunEntry{formals = [Types.STRING],                       result = Types.INT})
    val value_env = S.enter(value_env, S.symbol "substring", Env.FunEntry{formals = [Types.STRING, Types.INT, Types.INT], result = Types.STRING})
    val value_env = S.enter(value_env, S.symbol "concat",    Env.FunEntry{formals = [Types.STRING, Types.STRING],         result = Types.STRING})
    val value_env = S.enter(value_env, S.symbol "not",       Env.FunEntry{formals = [Types.INT],                          result = Types.INT})
    val value_env = S.enter(value_env, S.symbol "exit",      Env.FunEntry{formals = [Types.INT],                          result = Types.UNIT})
    
    fun enterScope () = loop_depth := !loop_depth + 1
    fun exitScope () = loop_depth := !loop_depth - 1
    
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
    
    
    fun transTy (tenv, A.NameTy(id, pos)) = Types.NAME(id, ref (S.look(tenv, id)))
      | transTy (tenv, A.RecordTy(fields)) = Types.RECORD(recordTyHelper(tenv, fields), ref ())
      | transTy (tenv, A.ArrayTy(id, pos)) = Types.ARRAY(case S.look(tenv, id) of
                                                               SOME t => t
                                                             | NONE => (ErrorMsg.error pos ("undeclared array type " ^ S.name id); Types.UNIT),
                                                         ref ())
    
    and recordTyHelper (tenv, {name, escape, typ, pos} :: fields) = (name, case S.look(tenv, typ) of 
                                                                                 SOME t => t
                                                                               | NONE => (ErrorMsg.error pos ("undeclared type in record " ^ S.name name); Types.UNIT)
                                                                    )
                                                                    :: recordTyHelper(tenv, fields)
      | recordTyHelper (tenv, []) = []
    
    
    fun checkFieldExists (tenv, pos, (fieldname, ty) :: fields, field) = if S.name field = S.name fieldname
                                                                         then ty
                                                                         else checkFieldExists(tenv, pos, fields, field)
      | checkFieldExists (tenv, pos, [], field) = (ErrorMsg.error pos ("no field " ^ S.name field); Types.UNIT)
    
    
    fun actualType (Types.NAME (s, ref (SOME(t)))) = actualType t
      | actualType (t:Types.ty) = t
    
    fun transDecs (venv, tenv, A.FunctionDec(fdecs) :: decs) = 
          let 
              val {venv, tenv} = transFunDecs(venv, tenv, fdecs)
          in
              transDecs(venv, tenv, decs)
          end
      
      | transDecs (venv, tenv, A.VarDec{name, escape, typ = NONE, init, pos} :: decs) =
          let 
              val {exp, ty} = transExp(venv, tenv) init
          in
              transDecs(S.enter(venv, name, Env.VarEntry{ty = ty}), tenv, decs)
          end
      | transDecs (venv, tenv, A.VarDec{name, escape, typ = SOME((id, _)), init, pos} :: decs) =
          let 
              val {exp, ty} = transExp(venv, tenv) init
          in
              if not (isSome(S.look(tenv, id))) 
              then (ErrorMsg.error pos ("undeclared type " ^ S.name id); transDecs(S.enter(venv, name, Env.VarEntry{ty = ty}), tenv, decs))
              else
                  if valOf(S.look(tenv, id)) = ty 
                  then transDecs(S.enter(venv, name, Env.VarEntry{ty = ty}), tenv, decs)
                  else (ErrorMsg.error pos ("type mismatch"); transDecs(S.enter(venv, name, Env.VarEntry{ty = ty}), tenv, decs))
          end
      
      | transDecs (venv, tenv, A.TypeDec({name, ty, pos} :: tdecs) :: decs) = transDecs(venv, S.enter(tenv, name, transTy(tenv, ty)), A.TypeDec(tdecs) :: decs)
      | transDecs (venv, tenv, A.TypeDec([]) :: decs) = transDecs(venv, tenv, decs)
      
      | transDecs (venv, tenv, []) = {venv = venv, tenv = tenv}
    
    and transFunDecs (venv, tenv, {name, params, result = SOME(id, _), body, pos} :: fdecs) = 
        let 
            val result_ty = case S.look(tenv, id) of
                                  SOME t => t
                                | NONE => (ErrorMsg.error pos ("undeclated type" ^ S.name id); Types.UNIT)
            fun transparam{name, escape, typ, pos} = 
                case S.look(tenv, typ) of
                      SOME t => {name = name, ty = t}
                    | NONE => (ErrorMsg.error pos ("undeclared type " ^ S.name name); {name = name, ty = Types.UNIT})
            val params' = (map transparam) params
            val venv' = S.enter(venv, name, Env.FunEntry{formals = map #ty params', result = result_ty})
            fun enterparam({name, ty}, venv) = S.enter(venv, name, Env.VarEntry{ty = ty})
            val venv'' = foldr enterparam venv' params'
            val body' = transExp(venv'', tenv) body
        in 
            (if #ty body' <> result_ty 
             then ErrorMsg.error pos ("type mismatch of function result type") 
             else ();
            transFunDecs(venv', tenv, fdecs))
        end
      | transFunDecs (venv, tenv, {name, params, result = NONE, body, pos} :: fdecs) =
        let
          fun transparam{name, escape, typ, pos} = 
              case S.look(tenv, typ) of
                    SOME t => {name = name, ty = t}
                  | NONE => (ErrorMsg.error pos ("undeclared type " ^ S.name name); {name = name, ty = Types.UNIT})
          val params' = (map transparam) params
          val venv' = S.enter(venv, name, Env.FunEntry{formals = map #ty params', result = Types.UNIT})
          fun enterparam({name, ty}, venv) = S.enter(venv, name, Env.VarEntry{ty = ty})
          val venv'' = foldr enterparam venv' params'
          val body' = transExp(venv'', tenv) body
        in
            (if #ty body' <> Types.UNIT 
             then ErrorMsg.error pos ("procedure does not return unit") 
             else (); 
             transFunDecs(venv', tenv, fdecs)
            )
        end
      | transFunDecs (venv, tenv, []) = {venv = venv, tenv = tenv}
    
    and transExp(venv, tenv) = 
        let 
            fun trexp (A.VarExp(var)) = {exp = (), ty = #ty (trvar var)}
          
              | trexp (A.NilExp) = {exp = (), ty = Types.NIL}
          
              | trexp (A.IntExp(i)) = {exp = (), ty = Types.INT}
              
              | trexp (A.StringExp(s, pos)) = {exp = (), ty = Types.STRING}
              
              | trexp (A.CallExp{func, args, pos}) = (case S.look(venv, func) of
                                                           SOME(Env.FunEntry{formals, result}) => {exp = (), ty = result}
                                                         | _ => (ErrorMsg.error pos ("undeclared function " ^ S.name func); {exp = (), ty = Types.UNIT}))
              
              | trexp (A.OpExp{left, oper, right, pos}) =
                let
                    val l = trexp left
                    val r = trexp right
                in
                    case oper of
                          A.PlusOp =>   (checkInt(l, pos); checkInt(r, pos); {exp = (), ty = Types.INT})
                        | A.MinusOp =>  (checkInt(l, pos); checkInt(r, pos); {exp = (), ty = Types.INT})
                        | A.TimesOp =>  (checkInt(l, pos); checkInt(r, pos); {exp = (), ty = Types.INT})
                        | A.DivideOp => (checkInt(l, pos); checkInt(r, pos); {exp = (), ty = Types.INT})

                        | A.LtOp => (checkIntOrString(l, pos); checkIntOrString(r, pos); checkTypeEqual(l, r, pos); {exp = (), ty = #ty l})
                        | A.LeOp => (checkIntOrString(l, pos); checkIntOrString(r, pos); checkTypeEqual(l, r, pos); {exp = (), ty = #ty l})
                        | A.GtOp => (checkIntOrString(l, pos); checkIntOrString(r, pos); checkTypeEqual(l, r, pos); {exp = (), ty = #ty l})
                        | A.GeOp => (checkIntOrString(l, pos); checkIntOrString(r, pos); checkTypeEqual(l, r, pos); {exp = (), ty = #ty l})

                        | A.EqOp =>  (checkTypeEqual(l, r, pos); {exp = (), ty = #ty l})
                        | A.NeqOp => (checkTypeEqual(l, r, pos); {exp = (), ty = #ty l})
                end
              
              | trexp (A.RecordExp{fields, typ, pos}) = (case S.look(tenv, typ) of
                                                              SOME t => {exp = (), ty = t}
                                                            | NONE => (ErrorMsg.error pos ("undeclared record type " ^ S.name typ); {exp = (), ty = Types.UNIT}))
              
              | trexp (A.SeqExp(exps)) =
                  let
                      fun runexp ((exp, pos) :: exps) = if null exps 
                                                        then transExp(venv, tenv) exp
                                                        else (transExp(venv, tenv) exp; runexp(exps))
                        | runexp ([]) = {exp = (), ty = Types.UNIT}
                  in
                      runexp(exps)
                  end
              
              | trexp (A.AssignExp{var, exp, pos}) = 
                  let 
                      val tl = #ty (trvar var)
                      val tr = #ty (trexp exp)
                  in
                      if tl = tr 
                      then {exp = (), ty = tl} 
                      else (ErrorMsg.error pos ("type mismatch in assignment"); {exp = (), ty = Types.UNIT})
                  end
                  
              | trexp (A.IfExp{test, then', else', pos}) = 
                  let
                      val t = #ty (trexp then')
                  in 
                      case else' of
                            SOME e => if t = #ty (trexp e) 
                                      then {exp = (), ty = t} 
                                      else (ErrorMsg.error pos ("type mismatch between then and else"); {exp = (), ty = Types.UNIT})
                          | NONE => {exp = (), ty = t}
                  end
              
              | trexp (A.WhileExp{test, body, pos}) = 
                  let
                      val t_test = #ty (trexp test)
                      val t_body = (enterScope(); #ty (trexp body)) (* Not used, but still needs to be type-checked. *)
                  in
                      (exitScope();
                       if t_test = Types.INT
                       then {exp = (), ty = Types.UNIT}
                       else (ErrorMsg.error pos ("while loop condition must be an integer"); {exp = (), ty = Types.UNIT}))
                  end
              
              | trexp (A.ForExp{var, escape, lo, hi, body, pos}) = 
                  let
                      val venv' = S.enter(venv, var, Env.VarEntry{ty = Types.INT})
                      val t_lo = #ty (trexp lo)
                      val t_hi = #ty (trexp hi)
                      val t_body = (enterScope(); #ty (transExp(venv', tenv) body)) (* Not used, but still needs to be type-checked. *)
                  in
                      (exitScope();
                       if t_lo = Types.INT andalso t_hi = Types.INT
                       then {exp = (), ty = Types.UNIT}
                       else (ErrorMsg.error pos ("for loop bounds must be integers"); {exp = (), ty = Types.UNIT}))
                  end
              
              | trexp (A.BreakExp(pos)) = 
                  if !loop_depth = 0
                  then (ErrorMsg.error pos ("break not inside loop"); {exp = (), ty = Types.UNIT})
                  else {exp = (), ty = Types.UNIT}
              
              | trexp (A.LetExp{decs, body, pos}) =
                  let 
                      val {venv = venv', tenv = tenv'} = transDecs(venv, tenv, decs)
                  in
                      transExp(venv', tenv') body
                  end
                
              | trexp (A.ArrayExp{typ, size, init, pos}) =
                  let
                      val t_array = case S.look(tenv, typ) of
                                     SOME t => t
                                   | NONE => (ErrorMsg.error pos ("undeclared type " ^ S.name typ); Types.UNIT)
                      val t_size = #ty (trexp size)
                      val t_init = #ty (trexp init)
                  in
                      case t_array of
                            Types.ARRAY(ty, unique) => if t_size = Types.INT
                                                       then 
                                                           if t_init = ty
                                                           then {exp = (), ty = t_array}
                                                           else (ErrorMsg.error pos ("initialization value doesn't match array element type"); {exp = (), ty = t_array})
                                                       else (ErrorMsg.error pos ("array size must be an integer"); {exp = (), ty = t_array})
                          | _ => (ErrorMsg.error pos (S.name typ ^ " must be an array type"); {exp = (), ty = Types.UNIT})
                  end

            and trvar (A.SimpleVar(id, pos)) =
                (case S.look(venv, id) of
                      SOME(Env.VarEntry{ty}) => {exp = (), ty = actualType ty}
                    | _ => (ErrorMsg.error pos ("undefined variable " ^ S.name id); {exp = (), ty = Types.UNIT}))
              | trvar (A.FieldVar(var, symbol, pos)) = {exp = (), ty = case #ty (trvar var) of
                                                                             Types.RECORD(fieldlist, unique) => checkFieldExists(tenv, pos, fieldlist, symbol)
                                                                           | _ => (ErrorMsg.error pos (S.name symbol ^ " must be a record"); Types.UNIT)}
              | trvar (A.SubscriptVar(var, exp, pos)) = {exp = (), ty = case #ty (trvar var) of 
                                                                              Types.ARRAY(ty, unique) => ty
                                                                            | _ => (ErrorMsg.error pos ("subscripting non-array type"); Types.UNIT)}

        in 
            trexp
        end
    
    fun transProg e = transExp(value_env, type_env) e

end 