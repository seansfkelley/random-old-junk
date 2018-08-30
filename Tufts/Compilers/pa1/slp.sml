type id = string;

datatype binop = Plus | Minus | Times | Div;

datatype stm = CompoundStm of stm * stm
	        | AssignStm of id * exp
	        | PrintStm of exp list
     and exp = IdExp of id
	        | NumExp of int
            | OpExp of exp * binop * exp
            | EseqExp of stm * exp
            ;

(* Nonexhaustive: no environment = nil case. *)
fun   lookup (id, (name, value)::vars) = if id = name 
                                         then value 
                                         else lookup (id, vars)
    ;

fun   update (id, value', nil) = [(id, value')]
    | update (id, value', (name, value)::vars) = if id = name 
                                                 then (name, value') :: vars 
                                                 else (name, value) :: update(id, value', vars)
    ;

fun   interpExp (IdExp(id), env) = lookup(id, env)
    | interpExp (NumExp(i), _) = i
    | interpExp (OpExp(l, oper, r), env) = let
                                               val l' = interpExp(l, env)
                                               val r' = interpExp(r, env)
                                           in
                                               case oper of
                                                     Plus => l' + r'
                                                   | Minus => l' - r'
                                                   | Times => l' * r'
                                                   | Div => l' div r'
                                           end
    | interpExp(EseqExp(s, e), env) = interpExp(e, interpStm(s, env))

and   interpStm (CompoundStm(s1, s2), env) = interpStm(s2, interpStm(s1, env))
    | interpStm (AssignStm(id, e), env) = update(id, interpExp(e, env), env)
    | interpStm (PrintStm(nil), env) = (print "\n"; env)
    | interpStm (PrintStm(e::es), env) = (print (Int.toString (interpExp(e, env)) ^ " "); interpStm(PrintStm(es), env))
    ;

fun   interp stm = (interpStm(stm, nil); ());

(*
8 7
80
*)
val prog = 
    CompoundStm(AssignStm("a",OpExp(NumExp 5, Plus, NumExp 3)),
    CompoundStm(AssignStm("b",
        EseqExp(PrintStm[IdExp"a",OpExp(IdExp"a", Minus,NumExp 1)],
            OpExp(NumExp 10, Times, IdExp"a"))),
    PrintStm[IdExp "b"]));

(*
36
129
*)
val prog1 = 
    CompoundStm(AssignStm("a", NumExp 6),
    CompoundStm(AssignStm("a", OpExp(IdExp "a", Times, IdExp "a")),
    CompoundStm(AssignStm("b",
        EseqExp(PrintStm [IdExp "a"], OpExp(IdExp "a", Times, IdExp "a"))),
    PrintStm [OpExp(IdExp "b", Div, NumExp 10)])));

(*
1
*)
val prog2 =
    PrintStm [OpExp(OpExp(OpExp(NumExp 9, Div, NumExp 10), Plus, OpExp(NumExp 5, Times, NumExp 6)), Minus, NumExp 29)];

(*
6
120
*)
val prog3 =
    CompoundStm(AssignStm("a", NumExp 1),
    CompoundStm(AssignStm("b", NumExp 2),
    CompoundStm(AssignStm("c", NumExp 3),
    CompoundStm(PrintStm [OpExp(IdExp "a", Times, OpExp(IdExp "b", Times, IdExp "c"))],
    CompoundStm(AssignStm("a", NumExp 4),
    CompoundStm(AssignStm("b", NumExp 5),
    CompoundStm(AssignStm("c", NumExp 6),
    PrintStm [OpExp(IdExp "a", Times, OpExp(IdExp "b", Times, IdExp "c"))])))))));
