functor TigerLrValsFun(structure Token : TOKEN)
 : sig structure ParserData : PARSER_DATA
       structure Tokens : Tiger_TOKENS
   end
 = 
struct
structure ParserData=
struct
structure Header = 
struct
(* Sean Kelley and Walker Holahan *)

(* Shift/reduce conflicts were resolved in two ways:
        1. Setting precedence. This was useful for operators and the like, but it was also handy
           in resolving conflicts related to if/then/elses, declarations, and other types of
           expressions. We decided the control flow statements should have low precedence so that
           expressions such as 'if (boolean) then a + b else c + d' operate as the programmer
           would expect: grouping 'else (c + d)' rather than '(if...) + d'.
        2. We also tweaked the grammar in the case of lvalues. This is described in a comment
           below.
*)

structure A = Absyn

(* Extract the lists from their respective expression/declaration types so they can be appended to.
   There must be a proper-ML way to do this, but I do not know it and this works. These are used
   by the semantic actions to build these lists.
   
   Note: these functions cause the compiler to warn about nonexhaustive matches. That's not a problem,
   as we can guarantee that they will only be called with the corresponding type.
*)
   
fun getexplist (A.SeqExp e) = e
fun gettydeclist (A.TypeDec t) = t
fun getfundeclist (A.FunctionDec f) = f


end
structure LrTable = Token.LrTable
structure Token = Token
local open LrTable in 
val table=let val actionRows =
"\
\\001\000\001\000\000\000\000\000\
\\001\000\001\000\195\000\005\000\195\000\007\000\195\000\009\000\195\000\
\\011\000\195\000\013\000\195\000\015\000\031\000\016\000\030\000\
\\017\000\029\000\018\000\028\000\025\000\195\000\026\000\195\000\
\\030\000\195\000\031\000\195\000\034\000\195\000\035\000\195\000\
\\037\000\195\000\038\000\195\000\042\000\195\000\043\000\195\000\
\\044\000\195\000\000\000\
\\001\000\001\000\196\000\005\000\196\000\007\000\196\000\009\000\196\000\
\\011\000\196\000\013\000\196\000\015\000\031\000\016\000\030\000\
\\017\000\029\000\018\000\028\000\025\000\196\000\026\000\196\000\
\\030\000\196\000\031\000\196\000\034\000\196\000\035\000\196\000\
\\037\000\196\000\038\000\196\000\042\000\196\000\043\000\196\000\
\\044\000\196\000\000\000\
\\001\000\001\000\197\000\005\000\197\000\007\000\197\000\009\000\197\000\
\\011\000\197\000\013\000\197\000\015\000\031\000\016\000\030\000\
\\017\000\029\000\018\000\028\000\025\000\197\000\026\000\197\000\
\\030\000\197\000\031\000\197\000\034\000\197\000\035\000\197\000\
\\037\000\197\000\038\000\197\000\042\000\197\000\043\000\197\000\
\\044\000\197\000\000\000\
\\001\000\001\000\198\000\005\000\198\000\007\000\198\000\009\000\198\000\
\\011\000\198\000\013\000\198\000\015\000\031\000\016\000\030\000\
\\017\000\029\000\018\000\028\000\025\000\198\000\026\000\198\000\
\\030\000\198\000\031\000\198\000\034\000\198\000\035\000\198\000\
\\037\000\198\000\038\000\198\000\042\000\198\000\043\000\198\000\
\\044\000\198\000\000\000\
\\001\000\001\000\199\000\005\000\199\000\007\000\199\000\009\000\199\000\
\\011\000\199\000\013\000\199\000\015\000\031\000\016\000\030\000\
\\017\000\029\000\018\000\028\000\025\000\199\000\026\000\199\000\
\\030\000\199\000\031\000\199\000\034\000\199\000\035\000\199\000\
\\037\000\199\000\038\000\199\000\042\000\199\000\043\000\199\000\
\\044\000\199\000\000\000\
\\001\000\001\000\200\000\005\000\200\000\007\000\200\000\009\000\200\000\
\\011\000\200\000\013\000\200\000\015\000\031\000\016\000\030\000\
\\017\000\029\000\018\000\028\000\025\000\200\000\026\000\200\000\
\\030\000\200\000\031\000\200\000\034\000\200\000\035\000\200\000\
\\037\000\200\000\038\000\200\000\042\000\200\000\043\000\200\000\
\\044\000\200\000\000\000\
\\001\000\002\000\016\000\003\000\015\000\004\000\014\000\008\000\013\000\
\\016\000\012\000\029\000\011\000\032\000\010\000\033\000\009\000\
\\036\000\008\000\040\000\007\000\041\000\006\000\000\000\
\\001\000\002\000\040\000\000\000\
\\001\000\002\000\051\000\000\000\
\\001\000\002\000\069\000\000\000\
\\001\000\002\000\070\000\000\000\
\\001\000\002\000\071\000\000\000\
\\001\000\002\000\103\000\012\000\102\000\028\000\101\000\000\000\
\\001\000\002\000\105\000\000\000\
\\001\000\002\000\124\000\000\000\
\\001\000\002\000\129\000\000\000\
\\001\000\002\000\133\000\000\000\
\\001\000\006\000\088\000\027\000\087\000\000\000\
\\001\000\006\000\119\000\000\000\
\\001\000\006\000\128\000\019\000\127\000\000\000\
\\001\000\008\000\089\000\000\000\
\\001\000\009\000\075\000\000\000\
\\001\000\009\000\097\000\000\000\
\\001\000\009\000\118\000\000\000\
\\001\000\011\000\084\000\015\000\031\000\016\000\030\000\017\000\029\000\
\\018\000\028\000\019\000\027\000\020\000\026\000\021\000\025\000\
\\022\000\024\000\023\000\023\000\024\000\022\000\025\000\021\000\
\\026\000\020\000\000\000\
\\001\000\011\000\096\000\015\000\031\000\016\000\030\000\017\000\029\000\
\\018\000\028\000\019\000\027\000\020\000\026\000\021\000\025\000\
\\022\000\024\000\023\000\023\000\024\000\022\000\025\000\021\000\
\\026\000\020\000\000\000\
\\001\000\013\000\094\000\000\000\
\\001\000\013\000\125\000\000\000\
\\001\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\
\\030\000\074\000\000\000\
\\001\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\
\\034\000\109\000\000\000\
\\001\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\
\\035\000\073\000\000\000\
\\001\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\
\\035\000\130\000\000\000\
\\001\000\019\000\086\000\000\000\
\\001\000\019\000\095\000\000\000\
\\001\000\019\000\137\000\000\000\
\\001\000\027\000\072\000\000\000\
\\001\000\027\000\117\000\000\000\
\\001\000\037\000\068\000\000\000\
\\001\000\038\000\099\000\000\000\
\\001\000\039\000\115\000\000\000\
\\142\000\002\000\016\000\003\000\015\000\004\000\014\000\008\000\013\000\
\\016\000\012\000\029\000\011\000\032\000\010\000\033\000\009\000\
\\036\000\008\000\040\000\007\000\041\000\006\000\000\000\
\\142\000\002\000\079\000\000\000\
\\142\000\002\000\108\000\000\000\
\\142\000\042\000\039\000\043\000\038\000\044\000\037\000\000\000\
\\143\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\000\000\
\\144\000\000\000\
\\145\000\000\000\
\\146\000\000\000\
\\147\000\000\000\
\\148\000\000\000\
\\149\000\044\000\037\000\000\000\
\\150\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\000\000\
\\151\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\000\000\
\\152\000\000\000\
\\153\000\000\000\
\\154\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\
\\042\000\039\000\000\000\
\\155\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\
\\042\000\039\000\000\000\
\\156\000\000\000\
\\157\000\000\000\
\\158\000\000\000\
\\159\000\005\000\134\000\000\000\
\\160\000\000\000\
\\161\000\000\000\
\\162\000\010\000\019\000\014\000\018\000\027\000\017\000\000\000\
\\163\000\000\000\
\\164\000\000\000\
\\165\000\000\000\
\\166\000\000\000\
\\167\000\000\000\
\\168\000\000\000\
\\169\000\000\000\
\\170\000\000\000\
\\171\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\000\000\
\\172\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\000\000\
\\173\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\000\000\
\\174\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\
\\031\000\110\000\000\000\
\\175\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\000\000\
\\176\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\026\000\020\000\000\000\
\\177\000\000\000\
\\178\000\000\000\
\\179\000\008\000\049\000\010\000\048\000\012\000\047\000\000\000\
\\180\000\000\000\
\\181\000\000\000\
\\182\000\039\000\112\000\000\000\
\\183\000\007\000\076\000\015\000\031\000\016\000\030\000\017\000\029\000\
\\018\000\028\000\019\000\027\000\020\000\026\000\021\000\025\000\
\\022\000\024\000\023\000\023\000\024\000\022\000\025\000\021\000\
\\026\000\020\000\000\000\
\\184\000\000\000\
\\185\000\000\000\
\\186\000\005\000\098\000\015\000\031\000\016\000\030\000\017\000\029\000\
\\018\000\028\000\019\000\027\000\020\000\026\000\021\000\025\000\
\\022\000\024\000\023\000\023\000\024\000\022\000\025\000\021\000\
\\026\000\020\000\000\000\
\\187\000\000\000\
\\188\000\000\000\
\\189\000\017\000\029\000\018\000\028\000\000\000\
\\190\000\017\000\029\000\018\000\028\000\000\000\
\\191\000\000\000\
\\192\000\000\000\
\\193\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\000\000\
\\194\000\015\000\031\000\016\000\030\000\017\000\029\000\018\000\028\000\
\\019\000\027\000\020\000\026\000\021\000\025\000\022\000\024\000\
\\023\000\023\000\024\000\022\000\025\000\021\000\000\000\
\\201\000\005\000\122\000\015\000\031\000\016\000\030\000\017\000\029\000\
\\018\000\028\000\019\000\027\000\020\000\026\000\021\000\025\000\
\\022\000\024\000\023\000\023\000\024\000\022\000\025\000\021\000\
\\026\000\020\000\000\000\
\\202\000\000\000\
\\203\000\000\000\
\"
val actionRowNumbers =
"\007\000\069\000\064\000\045\000\
\\065\000\079\000\044\000\008\000\
\\007\000\007\000\007\000\041\000\
\\068\000\067\000\081\000\007\000\
\\009\000\007\000\007\000\007\000\
\\007\000\007\000\007\000\007\000\
\\007\000\007\000\007\000\007\000\
\\007\000\007\000\049\000\044\000\
\\044\000\044\000\038\000\010\000\
\\011\000\012\000\036\000\031\000\
\\029\000\070\000\087\000\022\000\
\\085\000\042\000\007\000\041\000\
\\074\000\082\000\025\000\096\000\
\\095\000\006\000\004\000\005\000\
\\003\000\002\000\001\000\094\000\
\\093\000\092\000\091\000\048\000\
\\047\000\046\000\041\000\033\000\
\\018\000\021\000\007\000\007\000\
\\007\000\066\000\041\000\099\000\
\\027\000\034\000\026\000\090\000\
\\023\000\088\000\083\000\039\000\
\\013\000\007\000\014\000\043\000\
\\030\000\077\000\076\000\086\000\
\\072\000\007\000\084\000\071\000\
\\041\000\080\000\051\000\040\000\
\\043\000\058\000\052\000\037\000\
\\063\000\024\000\019\000\007\000\
\\007\000\097\000\007\000\089\000\
\\050\000\015\000\028\000\007\000\
\\020\000\016\000\032\000\075\000\
\\042\000\073\000\060\000\059\000\
\\053\000\007\000\017\000\061\000\
\\007\000\098\000\056\000\035\000\
\\043\000\078\000\054\000\007\000\
\\062\000\057\000\055\000\000\000"
val gotoT =
"\
\\001\000\139\000\008\000\003\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\002\000\034\000\003\000\033\000\006\000\032\000\007\000\031\000\
\\014\000\030\000\000\000\
\\000\000\
\\008\000\039\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\040\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\041\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\044\000\009\000\002\000\010\000\043\000\012\000\001\000\
\\014\000\042\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\008\000\048\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\008\000\050\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\051\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\052\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\053\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\054\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\055\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\056\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\057\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\058\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\059\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\060\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\061\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\062\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\002\000\063\000\003\000\033\000\006\000\032\000\007\000\031\000\
\\014\000\030\000\000\000\
\\002\000\064\000\003\000\033\000\006\000\032\000\007\000\031\000\
\\014\000\030\000\000\000\
\\002\000\065\000\003\000\033\000\006\000\032\000\007\000\031\000\
\\014\000\030\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\013\000\076\000\014\000\075\000\000\000\
\\008\000\078\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\081\000\009\000\002\000\011\000\080\000\012\000\001\000\
\\014\000\079\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\008\000\044\000\009\000\002\000\010\000\083\000\012\000\001\000\
\\014\000\042\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\008\000\088\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\089\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\090\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\008\000\044\000\009\000\002\000\010\000\091\000\012\000\001\000\
\\014\000\042\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\004\000\098\000\000\000\
\\008\000\102\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\005\000\105\000\014\000\104\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\008\000\109\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\000\000\
\\008\000\081\000\009\000\002\000\011\000\111\000\012\000\001\000\
\\014\000\079\000\000\000\
\\000\000\
\\003\000\112\000\000\000\
\\000\000\
\\005\000\114\000\014\000\104\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\008\000\118\000\009\000\002\000\012\000\001\000\000\000\
\\008\000\119\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\008\000\121\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\008\000\124\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\013\000\129\000\014\000\075\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\008\000\130\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\000\000\
\\008\000\133\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\007\000\134\000\000\000\
\\000\000\
\\005\000\136\000\014\000\104\000\000\000\
\\000\000\
\\000\000\
\\008\000\137\000\009\000\002\000\012\000\001\000\000\000\
\\000\000\
\\007\000\138\000\000\000\
\\000\000\
\\000\000\
\"
val numstates = 140
val numrules = 62
val s = ref "" and index = ref 0
val string_to_int = fn () => 
let val i = !index
in index := i+2; Char.ord(String.sub(!s,i)) + Char.ord(String.sub(!s,i+1)) * 256
end
val string_to_list = fn s' =>
    let val len = String.size s'
        fun f () =
           if !index < len then string_to_int() :: f()
           else nil
   in index := 0; s := s'; f ()
   end
val string_to_pairlist = fn (conv_key,conv_entry) =>
     let fun f () =
         case string_to_int()
         of 0 => EMPTY
          | n => PAIR(conv_key (n-1),conv_entry (string_to_int()),f())
     in f
     end
val string_to_pairlist_default = fn (conv_key,conv_entry) =>
    let val conv_row = string_to_pairlist(conv_key,conv_entry)
    in fn () =>
       let val default = conv_entry(string_to_int())
           val row = conv_row()
       in (row,default)
       end
   end
val string_to_table = fn (convert_row,s') =>
    let val len = String.size s'
        fun f ()=
           if !index < len then convert_row() :: f()
           else nil
     in (s := s'; index := 0; f ())
     end
local
  val memo = Array.array(numstates+numrules,ERROR)
  val _ =let fun g i=(Array.update(memo,i,REDUCE(i-numstates)); g(i+1))
       fun f i =
            if i=numstates then g i
            else (Array.update(memo,i,SHIFT (STATE i)); f (i+1))
          in f 0 handle Subscript => ()
          end
in
val entry_to_action = fn 0 => ACCEPT | 1 => ERROR | j => Array.sub(memo,(j-2))
end
val gotoT=Array.fromList(string_to_table(string_to_pairlist(NT,STATE),gotoT))
val actionRows=string_to_table(string_to_pairlist_default(T,entry_to_action),actionRows)
val actionRowNumbers = string_to_list actionRowNumbers
val actionT = let val actionRowLookUp=
let val a=Array.fromList(actionRows) in fn i=>Array.sub(a,i) end
in Array.fromList(map actionRowLookUp actionRowNumbers)
end
in LrTable.mkLrTable {actions=actionT,gotos=gotoT,numRules=numrules,
numStates=numstates,initialState=STATE 0}
end
end
local open Header in
type pos = int
type arg = unit
structure MlyValue = 
struct
datatype svalue = VOID | ntVOID of unit ->  unit
 | STRING of unit ->  (string) | INT of unit ->  (int)
 | ID of unit ->  (string)
 | reclist of unit ->  ( ( Symbol.symbol * A.exp * pos )  list)
 | arith of unit ->  (A.exp) | explist of unit ->  (A.exp list)
 | expseq of unit ->  (A.exp) | lvalue of unit ->  (A.var)
 | exp of unit ->  (A.exp) | fundec of unit ->  (A.dec)
 | vardec of unit ->  (A.dec) | tyfields of unit ->  (A.field list)
 | ty of unit ->  (A.ty) | tydec of unit ->  (A.dec)
 | decs of unit ->  (A.dec list) | program of unit ->  (A.exp)
end
type svalue = MlyValue.svalue
type result = A.exp
end
structure EC=
struct
open LrTable
infix 5 $$
fun x $$ y = y::x
val is_keyword =
fn (T 31) => true | (T 32) => true | (T 33) => true | (T 39) => true
 | (T 35) => true | (T 36) => true | (T 37) => true | (T 41) => true
 | (T 42) => true | (T 43) => true | (T 27) => true | (T 28) => true
 | (T 29) => true | (T 30) => true | (T 34) => true | (T 38) => true
 | (T 40) => true | _ => false
val preferred_change : (term list * term list) list = 
(nil
,nil
 $$ (T 29))::
(nil
,nil
 $$ (T 30))::
(nil
,nil
 $$ (T 7))::
nil
val noShift = 
fn (T 0) => true | _ => false
val showTerminal =
fn (T 0) => "EOF"
  | (T 1) => "ID"
  | (T 2) => "INT"
  | (T 3) => "STRING"
  | (T 4) => "COMMA"
  | (T 5) => "COLON"
  | (T 6) => "SEMICOLON"
  | (T 7) => "LPAREN"
  | (T 8) => "RPAREN"
  | (T 9) => "LBRACK"
  | (T 10) => "RBRACK"
  | (T 11) => "LBRACE"
  | (T 12) => "RBRACE"
  | (T 13) => "DOT"
  | (T 14) => "PLUS"
  | (T 15) => "MINUS"
  | (T 16) => "TIMES"
  | (T 17) => "DIVIDE"
  | (T 18) => "EQ"
  | (T 19) => "NEQ"
  | (T 20) => "LT"
  | (T 21) => "LE"
  | (T 22) => "GT"
  | (T 23) => "GE"
  | (T 24) => "AND"
  | (T 25) => "OR"
  | (T 26) => "ASSIGN"
  | (T 27) => "ARRAY"
  | (T 28) => "IF"
  | (T 29) => "THEN"
  | (T 30) => "ELSE"
  | (T 31) => "WHILE"
  | (T 32) => "FOR"
  | (T 33) => "TO"
  | (T 34) => "DO"
  | (T 35) => "LET"
  | (T 36) => "IN"
  | (T 37) => "END"
  | (T 38) => "OF"
  | (T 39) => "BREAK"
  | (T 40) => "NIL"
  | (T 41) => "FUNCTION"
  | (T 42) => "VAR"
  | (T 43) => "TYPE"
  | (T 44) => "UMINUS"
  | _ => "bogus-term"
local open Header in
val errtermvalue=
fn _ => MlyValue.VOID
end
val terms : term list = nil
 $$ (T 44) $$ (T 43) $$ (T 42) $$ (T 41) $$ (T 40) $$ (T 39) $$ (T 38)
 $$ (T 37) $$ (T 36) $$ (T 35) $$ (T 34) $$ (T 33) $$ (T 32) $$ (T 31)
 $$ (T 30) $$ (T 29) $$ (T 28) $$ (T 27) $$ (T 26) $$ (T 25) $$ (T 24)
 $$ (T 23) $$ (T 22) $$ (T 21) $$ (T 20) $$ (T 19) $$ (T 18) $$ (T 17)
 $$ (T 16) $$ (T 15) $$ (T 14) $$ (T 13) $$ (T 12) $$ (T 11) $$ (T 10)
 $$ (T 9) $$ (T 8) $$ (T 7) $$ (T 6) $$ (T 5) $$ (T 4) $$ (T 0)end
structure Actions =
struct 
exception mlyAction of int
local open Header in
val actions = 
fn (i392,defaultPos,stack,
    (()):arg) =>
case (i392,stack)
of  ( 0, ( rest671)) => let val  result = MlyValue.ntVOID (fn _ => ())
 in ( LrTable.NT 13, ( result, defaultPos, defaultPos), rest671)
end
|  ( 1, ( ( _, ( MlyValue.exp exp1, exp1left, exp1right)) :: rest671))
 => let val  result = MlyValue.program (fn _ => let val  (exp as exp1)
 = exp1 ()
 in (exp)
end)
 in ( LrTable.NT 0, ( result, exp1left, exp1right), rest671)
end
|  ( 2, ( ( _, ( MlyValue.decs decs1, _, decs1right)) :: ( _, ( 
MlyValue.tydec tydec1, tydec1left, _)) :: rest671)) => let val  result
 = MlyValue.decs (fn _ => let val  (tydec as tydec1) = tydec1 ()
 val  (decs as decs1) = decs1 ()
 in (tydec :: decs)
end)
 in ( LrTable.NT 1, ( result, tydec1left, decs1right), rest671)
end
|  ( 3, ( ( _, ( MlyValue.decs decs1, _, decs1right)) :: ( _, ( 
MlyValue.vardec vardec1, vardec1left, _)) :: rest671)) => let val  
result = MlyValue.decs (fn _ => let val  (vardec as vardec1) = vardec1
 ()
 val  (decs as decs1) = decs1 ()
 in (vardec :: decs)
end)
 in ( LrTable.NT 1, ( result, vardec1left, decs1right), rest671)
end
|  ( 4, ( ( _, ( MlyValue.decs decs1, _, decs1right)) :: ( _, ( 
MlyValue.fundec fundec1, fundec1left, _)) :: rest671)) => let val  
result = MlyValue.decs (fn _ => let val  (fundec as fundec1) = fundec1
 ()
 val  (decs as decs1) = decs1 ()
 in (fundec :: decs)
end)
 in ( LrTable.NT 1, ( result, fundec1left, decs1right), rest671)
end
|  ( 5, ( ( _, ( MlyValue.ntVOID empty1, empty1left, empty1right)) :: 
rest671)) => let val  result = MlyValue.decs (fn _ => let val  empty1
 = empty1 ()
 in ([])
end)
 in ( LrTable.NT 1, ( result, empty1left, empty1right), rest671)
end
|  ( 6, ( ( _, ( MlyValue.tydec tydec1, _, tydec1right)) :: ( _, ( 
MlyValue.ty ty1, _, _)) :: _ :: ( _, ( MlyValue.ID ID1, _, _)) :: ( _,
 ( _, (TYPEleft as TYPE1left), _)) :: rest671)) => let val  result = 
MlyValue.tydec (fn _ => let val  (ID as ID1) = ID1 ()
 val  (ty as ty1) = ty1 ()
 val  (tydec as tydec1) = tydec1 ()
 in (
A.TypeDec({name=Symbol.symbol ID,ty=ty,pos=TYPEleft} :: gettydeclist tydec)
)
end)
 in ( LrTable.NT 2, ( result, TYPE1left, tydec1right), rest671)
end
|  ( 7, ( ( _, ( MlyValue.ty ty1, _, ty1right)) :: _ :: ( _, ( 
MlyValue.ID ID1, _, _)) :: ( _, ( _, (TYPEleft as TYPE1left), _)) :: 
rest671)) => let val  result = MlyValue.tydec (fn _ => let val  (ID
 as ID1) = ID1 ()
 val  (ty as ty1) = ty1 ()
 in (A.TypeDec([{name=Symbol.symbol ID,ty=ty,pos=TYPEleft}]))
end)
 in ( LrTable.NT 2, ( result, TYPE1left, ty1right), rest671)
end
|  ( 8, ( ( _, ( MlyValue.exp exp1, _, exp1right)) :: _ :: ( _, ( 
MlyValue.ID ID1, _, _)) :: ( _, ( _, (VARleft as VAR1left), _)) :: 
rest671)) => let val  result = MlyValue.vardec (fn _ => let val  (ID
 as ID1) = ID1 ()
 val  (exp as exp1) = exp1 ()
 in (
A.VarDec({name=Symbol.symbol ID,escape=ref true,typ=NONE,init=exp,pos=VARleft})
)
end)
 in ( LrTable.NT 5, ( result, VAR1left, exp1right), rest671)
end
|  ( 9, ( ( _, ( MlyValue.exp exp1, _, exp1right)) :: _ :: ( _, ( 
MlyValue.ID ID2, ID2left, _)) :: _ :: ( _, ( MlyValue.ID ID1, _, _))
 :: ( _, ( _, (VARleft as VAR1left), _)) :: rest671)) => let val  
result = MlyValue.vardec (fn _ => let val  ID1 = ID1 ()
 val  ID2 = ID2 ()
 val  (exp as exp1) = exp1 ()
 in (
A.VarDec({name=Symbol.symbol ID1,escape=ref true,typ=SOME (Symbol.symbol ID2,ID2left),init=exp,pos=VARleft})
)
end)
 in ( LrTable.NT 5, ( result, VAR1left, exp1right), rest671)
end
|  ( 10, ( ( _, ( MlyValue.fundec fundec1, _, fundec1right)) :: ( _, (
 MlyValue.exp exp1, _, _)) :: _ :: _ :: ( _, ( MlyValue.tyfields 
tyfields1, _, _)) :: _ :: ( _, ( MlyValue.ID ID1, _, _)) :: ( _, ( _,
 (FUNCTIONleft as FUNCTION1left), _)) :: rest671)) => let val  result
 = MlyValue.fundec (fn _ => let val  (ID as ID1) = ID1 ()
 val  (tyfields as tyfields1) = tyfields1 ()
 val  (exp as exp1) = exp1 ()
 val  (fundec as fundec1) = fundec1 ()
 in (
A.FunctionDec({name=Symbol.symbol ID,params=tyfields,result=NONE,body=exp,pos=FUNCTIONleft} :: getfundeclist fundec)
)
end)
 in ( LrTable.NT 6, ( result, FUNCTION1left, fundec1right), rest671)

end
|  ( 11, ( ( _, ( MlyValue.fundec fundec1, _, fundec1right)) :: ( _, (
 MlyValue.exp exp1, _, _)) :: _ :: ( _, ( MlyValue.ID ID2, ID2left, _)
) :: _ :: _ :: ( _, ( MlyValue.tyfields tyfields1, _, _)) :: _ :: ( _,
 ( MlyValue.ID ID1, _, _)) :: ( _, ( _, (FUNCTIONleft as FUNCTION1left
), _)) :: rest671)) => let val  result = MlyValue.fundec (fn _ => let
 val  ID1 = ID1 ()
 val  (tyfields as tyfields1) = tyfields1 ()
 val  ID2 = ID2 ()
 val  (exp as exp1) = exp1 ()
 val  (fundec as fundec1) = fundec1 ()
 in (
A.FunctionDec({name=Symbol.symbol ID1,params=tyfields,result=SOME (Symbol.symbol ID2, ID2left),body=exp,pos=FUNCTIONleft} :: getfundeclist fundec)
)
end)
 in ( LrTable.NT 6, ( result, FUNCTION1left, fundec1right), rest671)

end
|  ( 12, ( ( _, ( MlyValue.exp exp1, _, exp1right)) :: _ :: _ :: ( _, 
( MlyValue.tyfields tyfields1, _, _)) :: _ :: ( _, ( MlyValue.ID ID1,
 _, _)) :: ( _, ( _, (FUNCTIONleft as FUNCTION1left), _)) :: rest671))
 => let val  result = MlyValue.fundec (fn _ => let val  (ID as ID1) = 
ID1 ()
 val  (tyfields as tyfields1) = tyfields1 ()
 val  (exp as exp1) = exp1 ()
 in (
A.FunctionDec([{name=Symbol.symbol ID,params=tyfields,result=NONE,body=exp,pos=FUNCTIONleft}])
)
end)
 in ( LrTable.NT 6, ( result, FUNCTION1left, exp1right), rest671)
end
|  ( 13, ( ( _, ( MlyValue.exp exp1, _, exp1right)) :: _ :: ( _, ( 
MlyValue.ID ID2, ID2left, _)) :: _ :: _ :: ( _, ( MlyValue.tyfields 
tyfields1, _, _)) :: _ :: ( _, ( MlyValue.ID ID1, _, _)) :: ( _, ( _,
 (FUNCTIONleft as FUNCTION1left), _)) :: rest671)) => let val  result
 = MlyValue.fundec (fn _ => let val  ID1 = ID1 ()
 val  (tyfields as tyfields1) = tyfields1 ()
 val  ID2 = ID2 ()
 val  (exp as exp1) = exp1 ()
 in (
A.FunctionDec([{name=Symbol.symbol ID1,params=tyfields,result=SOME (Symbol.symbol ID2, ID2left),body=exp,pos=FUNCTIONleft}])
)
end)
 in ( LrTable.NT 6, ( result, FUNCTION1left, exp1right), rest671)
end
|  ( 14, ( ( _, ( MlyValue.ID ID1, (IDleft as ID1left), ID1right)) :: 
rest671)) => let val  result = MlyValue.ty (fn _ => let val  (ID as 
ID1) = ID1 ()
 in (A.NameTy(Symbol.symbol ID,IDleft))
end)
 in ( LrTable.NT 3, ( result, ID1left, ID1right), rest671)
end
|  ( 15, ( ( _, ( _, _, RBRACE1right)) :: ( _, ( MlyValue.tyfields 
tyfields1, _, _)) :: ( _, ( _, LBRACE1left, _)) :: rest671)) => let
 val  result = MlyValue.ty (fn _ => let val  (tyfields as tyfields1) =
 tyfields1 ()
 in (A.RecordTy(tyfields))
end)
 in ( LrTable.NT 3, ( result, LBRACE1left, RBRACE1right), rest671)
end
|  ( 16, ( ( _, ( MlyValue.ID ID1, _, ID1right)) :: _ :: ( _, ( _, (
ARRAYleft as ARRAY1left), _)) :: rest671)) => let val  result = 
MlyValue.ty (fn _ => let val  (ID as ID1) = ID1 ()
 in (A.ArrayTy(Symbol.symbol ID,ARRAYleft))
end)
 in ( LrTable.NT 3, ( result, ARRAY1left, ID1right), rest671)
end
|  ( 17, ( ( _, ( MlyValue.ID ID2, _, ID2right)) :: _ :: ( _, ( 
MlyValue.ID ID1, ID1left, _)) :: rest671)) => let val  result = 
MlyValue.tyfields (fn _ => let val  ID1 = ID1 ()
 val  ID2 = ID2 ()
 in (
[{name=Symbol.symbol ID1,escape=ref true,typ=Symbol.symbol ID2,pos=ID1left}]
)
end)
 in ( LrTable.NT 4, ( result, ID1left, ID2right), rest671)
end
|  ( 18, ( ( _, ( MlyValue.tyfields tyfields1, _, tyfields1right)) ::
 _ :: ( _, ( MlyValue.ID ID2, _, _)) :: _ :: ( _, ( MlyValue.ID ID1, 
ID1left, _)) :: rest671)) => let val  result = MlyValue.tyfields (fn _
 => let val  ID1 = ID1 ()
 val  ID2 = ID2 ()
 val  (tyfields as tyfields1) = tyfields1 ()
 in (
{name=Symbol.symbol ID1,escape=ref true,typ=Symbol.symbol ID2,pos=ID1left} :: tyfields
)
end)
 in ( LrTable.NT 4, ( result, ID1left, tyfields1right), rest671)
end
|  ( 19, ( ( _, ( MlyValue.ntVOID empty1, empty1left, empty1right)) ::
 rest671)) => let val  result = MlyValue.tyfields (fn _ => let val  
empty1 = empty1 ()
 in ([])
end)
 in ( LrTable.NT 4, ( result, empty1left, empty1right), rest671)
end
|  ( 20, ( ( _, ( MlyValue.lvalue lvalue1, lvalue1left, lvalue1right))
 :: rest671)) => let val  result = MlyValue.exp (fn _ => let val  (
lvalue as lvalue1) = lvalue1 ()
 in (A.VarExp(lvalue))
end)
 in ( LrTable.NT 7, ( result, lvalue1left, lvalue1right), rest671)
end
|  ( 21, ( ( _, ( _, NIL1left, NIL1right)) :: rest671)) => let val  
result = MlyValue.exp (fn _ => (A.NilExp))
 in ( LrTable.NT 7, ( result, NIL1left, NIL1right), rest671)
end
|  ( 22, ( ( _, ( _, _, RPAREN1right)) :: ( _, ( MlyValue.expseq 
expseq1, _, _)) :: ( _, ( _, LPAREN1left, _)) :: rest671)) => let val 
 result = MlyValue.exp (fn _ => let val  (expseq as expseq1) = expseq1
 ()
 in (expseq)
end)
 in ( LrTable.NT 7, ( result, LPAREN1left, RPAREN1right), rest671)
end
|  ( 23, ( ( _, ( MlyValue.INT INT1, INT1left, INT1right)) :: rest671)
) => let val  result = MlyValue.exp (fn _ => let val  (INT as INT1) = 
INT1 ()
 in (A.IntExp(INT))
end)
 in ( LrTable.NT 7, ( result, INT1left, INT1right), rest671)
end
|  ( 24, ( ( _, ( MlyValue.STRING STRING1, (STRINGleft as STRING1left)
, STRING1right)) :: rest671)) => let val  result = MlyValue.exp (fn _
 => let val  (STRING as STRING1) = STRING1 ()
 in (A.StringExp(STRING, STRINGleft))
end)
 in ( LrTable.NT 7, ( result, STRING1left, STRING1right), rest671)
end
|  ( 25, ( ( _, ( MlyValue.arith arith1, arith1left, arith1right)) :: 
rest671)) => let val  result = MlyValue.exp (fn _ => let val  (arith
 as arith1) = arith1 ()
 in (arith)
end)
 in ( LrTable.NT 7, ( result, arith1left, arith1right), rest671)
end
|  ( 26, ( ( _, ( MlyValue.exp exp1, _, exp1right)) :: ( _, ( _, (
MINUSleft as MINUS1left), _)) :: rest671)) => let val  result = 
MlyValue.exp (fn _ => let val  (exp as exp1) = exp1 ()
 in (
A.OpExp({left=A.IntExp(0),oper=A.MinusOp,right=exp,pos=MINUSleft}))

end)
 in ( LrTable.NT 7, ( result, MINUS1left, exp1right), rest671)
end
|  ( 27, ( ( _, ( _, _, RPAREN1right)) :: ( _, ( MlyValue.explist 
explist1, _, _)) :: _ :: ( _, ( MlyValue.ID ID1, (IDleft as ID1left),
 _)) :: rest671)) => let val  result = MlyValue.exp (fn _ => let val 
 (ID as ID1) = ID1 ()
 val  (explist as explist1) = explist1 ()
 in (A.CallExp({func=Symbol.symbol ID,args=explist,pos=IDleft}))
end)
 in ( LrTable.NT 7, ( result, ID1left, RPAREN1right), rest671)
end
|  ( 28, ( ( _, ( _, _, RBRACE1right)) :: ( _, ( MlyValue.reclist 
reclist1, _, _)) :: _ :: ( _, ( MlyValue.ID ID1, (IDleft as ID1left),
 _)) :: rest671)) => let val  result = MlyValue.exp (fn _ => let val 
 (ID as ID1) = ID1 ()
 val  (reclist as reclist1) = reclist1 ()
 in (A.RecordExp({fields=reclist,typ=Symbol.symbol ID,pos=IDleft}))

end)
 in ( LrTable.NT 7, ( result, ID1left, RBRACE1right), rest671)
end
|  ( 29, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: _ :: _ :: ( _, 
( MlyValue.exp exp1, _, _)) :: _ :: ( _, ( MlyValue.ID ID1, (IDleft
 as ID1left), _)) :: rest671)) => let val  result = MlyValue.exp (fn _
 => let val  (ID as ID1) = ID1 ()
 val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (A.ArrayExp({typ=Symbol.symbol ID,size=exp1,init=exp2,pos=IDleft})
)
end)
 in ( LrTable.NT 7, ( result, ID1left, exp2right), rest671)
end
|  ( 30, ( ( _, ( MlyValue.exp exp1, _, exp1right)) :: ( _, ( _, 
ASSIGNleft, _)) :: ( _, ( MlyValue.lvalue lvalue1, lvalue1left, _)) ::
 rest671)) => let val  result = MlyValue.exp (fn _ => let val  (lvalue
 as lvalue1) = lvalue1 ()
 val  (exp as exp1) = exp1 ()
 in (A.AssignExp({var=lvalue,exp=exp,pos=ASSIGNleft}))
end)
 in ( LrTable.NT 7, ( result, lvalue1left, exp1right), rest671)
end
|  ( 31, ( ( _, ( MlyValue.exp exp3, _, exp3right)) :: _ :: ( _, ( 
MlyValue.exp exp2, _, _)) :: _ :: ( _, ( MlyValue.exp exp1, _, _)) :: 
( _, ( _, (IFleft as IF1left), _)) :: rest671)) => let val  result = 
MlyValue.exp (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 val  exp3 = exp3 ()
 in (A.IfExp({test=exp1,then'=exp2,else'=SOME exp3,pos=IFleft}))
end)
 in ( LrTable.NT 7, ( result, IF1left, exp3right), rest671)
end
|  ( 32, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: _ :: ( _, ( 
MlyValue.exp exp1, _, _)) :: ( _, ( _, (IFleft as IF1left), _)) :: 
rest671)) => let val  result = MlyValue.exp (fn _ => let val  exp1 = 
exp1 ()
 val  exp2 = exp2 ()
 in (A.IfExp({test=exp1,then'=exp2,else'=NONE,pos=IFleft}))
end)
 in ( LrTable.NT 7, ( result, IF1left, exp2right), rest671)
end
|  ( 33, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: _ :: ( _, ( 
MlyValue.exp exp1, _, _)) :: ( _, ( _, (WHILEleft as WHILE1left), _))
 :: rest671)) => let val  result = MlyValue.exp (fn _ => let val  exp1
 = exp1 ()
 val  exp2 = exp2 ()
 in (A.WhileExp({test=exp1,body=exp2,pos=WHILEleft}))
end)
 in ( LrTable.NT 7, ( result, WHILE1left, exp2right), rest671)
end
|  ( 34, ( ( _, ( MlyValue.exp exp3, _, exp3right)) :: _ :: ( _, ( 
MlyValue.exp exp2, _, _)) :: _ :: ( _, ( MlyValue.exp exp1, _, _)) ::
 _ :: ( _, ( MlyValue.ID ID1, _, _)) :: ( _, ( _, (FORleft as FOR1left
), _)) :: rest671)) => let val  result = MlyValue.exp (fn _ => let
 val  (ID as ID1) = ID1 ()
 val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 val  exp3 = exp3 ()
 in (
A.ForExp({var=Symbol.symbol ID,escape=ref true,lo=exp1,hi=exp2,body=exp3,pos=FORleft})
)
end)
 in ( LrTable.NT 7, ( result, FOR1left, exp3right), rest671)
end
|  ( 35, ( ( _, ( _, (BREAKleft as BREAK1left), BREAK1right)) :: 
rest671)) => let val  result = MlyValue.exp (fn _ => (
A.BreakExp(BREAKleft)))
 in ( LrTable.NT 7, ( result, BREAK1left, BREAK1right), rest671)
end
|  ( 36, ( ( _, ( _, _, END1right)) :: ( _, ( MlyValue.expseq expseq1,
 _, _)) :: _ :: ( _, ( MlyValue.decs decs1, _, _)) :: ( _, ( _, (
LETleft as LET1left), _)) :: rest671)) => let val  result = 
MlyValue.exp (fn _ => let val  (decs as decs1) = decs1 ()
 val  (expseq as expseq1) = expseq1 ()
 in (A.LetExp({decs=decs,body=expseq,pos=LETleft}))
end)
 in ( LrTable.NT 7, ( result, LET1left, END1right), rest671)
end
|  ( 37, ( ( _, ( MlyValue.ID ID1, (IDleft as ID1left), ID1right)) :: 
rest671)) => let val  result = MlyValue.lvalue (fn _ => let val  (ID
 as ID1) = ID1 ()
 in (A.SimpleVar(Symbol.symbol ID,IDleft))
end)
 in ( LrTable.NT 8, ( result, ID1left, ID1right), rest671)
end
|  ( 38, ( ( _, ( MlyValue.ID ID1, IDleft, ID1right)) :: _ :: ( _, ( 
MlyValue.lvalue lvalue1, lvalue1left, _)) :: rest671)) => let val  
result = MlyValue.lvalue (fn _ => let val  (lvalue as lvalue1) = 
lvalue1 ()
 val  (ID as ID1) = ID1 ()
 in (A.FieldVar(lvalue, Symbol.symbol ID, IDleft))
end)
 in ( LrTable.NT 8, ( result, lvalue1left, ID1right), rest671)
end
|  ( 39, ( ( _, ( _, _, RBRACK1right)) :: ( _, ( MlyValue.exp exp1, _,
 _)) :: ( _, ( _, LBRACKleft, _)) :: ( _, ( MlyValue.lvalue lvalue1, 
lvalue1left, _)) :: rest671)) => let val  result = MlyValue.lvalue (fn
 _ => let val  (lvalue as lvalue1) = lvalue1 ()
 val  (exp as exp1) = exp1 ()
 in (A.SubscriptVar(lvalue, exp, LBRACKleft))
end)
 in ( LrTable.NT 8, ( result, lvalue1left, RBRACK1right), rest671)
end
|  ( 40, ( ( _, ( _, _, RBRACK1right)) :: ( _, ( MlyValue.exp exp1, 
expleft, _)) :: _ :: ( _, ( MlyValue.ID ID1, (IDleft as ID1left), _))
 :: rest671)) => let val  result = MlyValue.lvalue (fn _ => let val  (
ID as ID1) = ID1 ()
 val  (exp as exp1) = exp1 ()
 in (
A.SubscriptVar(A.SimpleVar(Symbol.symbol ID, IDleft), exp, expleft))

end)
 in ( LrTable.NT 8, ( result, ID1left, RBRACK1right), rest671)
end
|  ( 41, ( ( _, ( MlyValue.exp exp1, (expleft as exp1left), exp1right)
) :: rest671)) => let val  result = MlyValue.expseq (fn _ => let val 
 (exp as exp1) = exp1 ()
 in (A.SeqExp([(exp, expleft)]))
end)
 in ( LrTable.NT 9, ( result, exp1left, exp1right), rest671)
end
|  ( 42, ( ( _, ( MlyValue.expseq expseq1, _, expseq1right)) :: _ :: (
 _, ( MlyValue.exp exp1, (expleft as exp1left), _)) :: rest671)) =>
 let val  result = MlyValue.expseq (fn _ => let val  (exp as exp1) = 
exp1 ()
 val  (expseq as expseq1) = expseq1 ()
 in (A.SeqExp((exp, expleft) :: getexplist expseq))
end)
 in ( LrTable.NT 9, ( result, exp1left, expseq1right), rest671)
end
|  ( 43, ( ( _, ( MlyValue.ntVOID empty1, empty1left, empty1right)) ::
 rest671)) => let val  result = MlyValue.expseq (fn _ => let val  
empty1 = empty1 ()
 in (A.SeqExp([]))
end)
 in ( LrTable.NT 9, ( result, empty1left, empty1right), rest671)
end
|  ( 44, ( ( _, ( MlyValue.exp exp1, exp1left, exp1right)) :: rest671)
) => let val  result = MlyValue.explist (fn _ => let val  (exp as exp1
) = exp1 ()
 in ([exp])
end)
 in ( LrTable.NT 10, ( result, exp1left, exp1right), rest671)
end
|  ( 45, ( ( _, ( MlyValue.explist explist1, _, explist1right)) :: _
 :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671)) => let val  
result = MlyValue.explist (fn _ => let val  (exp as exp1) = exp1 ()
 val  (explist as explist1) = explist1 ()
 in (exp :: explist)
end)
 in ( LrTable.NT 10, ( result, exp1left, explist1right), rest671)
end
|  ( 46, ( ( _, ( MlyValue.ntVOID empty1, empty1left, empty1right)) ::
 rest671)) => let val  result = MlyValue.explist (fn _ => let val  
empty1 = empty1 ()
 in ([])
end)
 in ( LrTable.NT 10, ( result, empty1left, empty1right), rest671)
end
|  ( 47, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
PLUSleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671))
 => let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (A.OpExp({left=exp1,oper=A.PlusOp,right=exp2,pos=PLUSleft}))
end)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 48, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
MINUSleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671))
 => let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (A.OpExp({left=exp1,oper=A.MinusOp,right=exp2,pos=MINUSleft}))
end
)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 49, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
TIMESleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671))
 => let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (A.OpExp({left=exp1,oper=A.TimesOp,right=exp2,pos=TIMESleft}))
end
)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 50, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
DIVIDEleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671)
) => let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (A.OpExp({left=exp1,oper=A.DivideOp,right=exp2,pos=DIVIDEleft}))

end)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 51, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
ANDleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671))
 => let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (
A.OpExp({left=A.OpExp({left=exp1,oper=A.PlusOp,right=exp2,pos=ANDleft}),oper=A.EqOp,right=A.IntExp(2),pos=ANDleft})
)
end)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 52, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
ORleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671)) =>
 let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (
A.OpExp({left=A.OpExp({left=exp1,oper=A.PlusOp,right=exp2,pos=ORleft}),oper=A.GeOp,right=A.IntExp(1),pos=ORleft})
)
end)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 53, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
EQleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671)) =>
 let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (A.OpExp({left=exp1,oper=A.EqOp,right=exp2,pos=EQleft}))
end)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 54, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
NEQleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671))
 => let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (A.OpExp({left=exp1,oper=A.NeqOp,right=exp2,pos=NEQleft}))
end)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 55, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
LTleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671)) =>
 let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (A.OpExp({left=exp1,oper=A.LtOp,right=exp2,pos=LTleft}))
end)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 56, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
GTleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671)) =>
 let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (A.OpExp({left=exp1,oper=A.GtOp,right=exp2,pos=GTleft}))
end)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 57, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
LEleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671)) =>
 let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (A.OpExp({left=exp1,oper=A.LeOp,right=exp2,pos=LEleft}))
end)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 58, ( ( _, ( MlyValue.exp exp2, _, exp2right)) :: ( _, ( _, 
GEleft, _)) :: ( _, ( MlyValue.exp exp1, exp1left, _)) :: rest671)) =>
 let val  result = MlyValue.arith (fn _ => let val  exp1 = exp1 ()
 val  exp2 = exp2 ()
 in (A.OpExp({left=exp1,oper=A.GeOp,right=exp2,pos=GEleft}))
end)
 in ( LrTable.NT 11, ( result, exp1left, exp2right), rest671)
end
|  ( 59, ( ( _, ( MlyValue.exp exp1, _, exp1right)) :: _ :: ( _, ( 
MlyValue.ID ID1, (IDleft as ID1left), _)) :: rest671)) => let val  
result = MlyValue.reclist (fn _ => let val  (ID as ID1) = ID1 ()
 val  (exp as exp1) = exp1 ()
 in ([(Symbol.symbol ID,exp,IDleft)])
end)
 in ( LrTable.NT 12, ( result, ID1left, exp1right), rest671)
end
|  ( 60, ( ( _, ( MlyValue.reclist reclist1, _, reclist1right)) :: _
 :: ( _, ( MlyValue.exp exp1, _, _)) :: _ :: ( _, ( MlyValue.ID ID1, (
IDleft as ID1left), _)) :: rest671)) => let val  result = 
MlyValue.reclist (fn _ => let val  (ID as ID1) = ID1 ()
 val  (exp as exp1) = exp1 ()
 val  (reclist as reclist1) = reclist1 ()
 in ((Symbol.symbol ID,exp,IDleft) :: reclist)
end)
 in ( LrTable.NT 12, ( result, ID1left, reclist1right), rest671)
end
|  ( 61, ( ( _, ( MlyValue.ntVOID empty1, empty1left, empty1right)) ::
 rest671)) => let val  result = MlyValue.reclist (fn _ => let val  
empty1 = empty1 ()
 in ([])
end)
 in ( LrTable.NT 12, ( result, empty1left, empty1right), rest671)
end
| _ => raise (mlyAction i392)
end
val void = MlyValue.VOID
val extract = fn a => (fn MlyValue.program x => x
| _ => let exception ParseInternal
	in raise ParseInternal end) a ()
end
end
structure Tokens : Tiger_TOKENS =
struct
type svalue = ParserData.svalue
type ('a,'b) token = ('a,'b) Token.token
fun EOF (p1,p2) = Token.TOKEN (ParserData.LrTable.T 0,(
ParserData.MlyValue.VOID,p1,p2))
fun ID (i,p1,p2) = Token.TOKEN (ParserData.LrTable.T 1,(
ParserData.MlyValue.ID (fn () => i),p1,p2))
fun INT (i,p1,p2) = Token.TOKEN (ParserData.LrTable.T 2,(
ParserData.MlyValue.INT (fn () => i),p1,p2))
fun STRING (i,p1,p2) = Token.TOKEN (ParserData.LrTable.T 3,(
ParserData.MlyValue.STRING (fn () => i),p1,p2))
fun COMMA (p1,p2) = Token.TOKEN (ParserData.LrTable.T 4,(
ParserData.MlyValue.VOID,p1,p2))
fun COLON (p1,p2) = Token.TOKEN (ParserData.LrTable.T 5,(
ParserData.MlyValue.VOID,p1,p2))
fun SEMICOLON (p1,p2) = Token.TOKEN (ParserData.LrTable.T 6,(
ParserData.MlyValue.VOID,p1,p2))
fun LPAREN (p1,p2) = Token.TOKEN (ParserData.LrTable.T 7,(
ParserData.MlyValue.VOID,p1,p2))
fun RPAREN (p1,p2) = Token.TOKEN (ParserData.LrTable.T 8,(
ParserData.MlyValue.VOID,p1,p2))
fun LBRACK (p1,p2) = Token.TOKEN (ParserData.LrTable.T 9,(
ParserData.MlyValue.VOID,p1,p2))
fun RBRACK (p1,p2) = Token.TOKEN (ParserData.LrTable.T 10,(
ParserData.MlyValue.VOID,p1,p2))
fun LBRACE (p1,p2) = Token.TOKEN (ParserData.LrTable.T 11,(
ParserData.MlyValue.VOID,p1,p2))
fun RBRACE (p1,p2) = Token.TOKEN (ParserData.LrTable.T 12,(
ParserData.MlyValue.VOID,p1,p2))
fun DOT (p1,p2) = Token.TOKEN (ParserData.LrTable.T 13,(
ParserData.MlyValue.VOID,p1,p2))
fun PLUS (p1,p2) = Token.TOKEN (ParserData.LrTable.T 14,(
ParserData.MlyValue.VOID,p1,p2))
fun MINUS (p1,p2) = Token.TOKEN (ParserData.LrTable.T 15,(
ParserData.MlyValue.VOID,p1,p2))
fun TIMES (p1,p2) = Token.TOKEN (ParserData.LrTable.T 16,(
ParserData.MlyValue.VOID,p1,p2))
fun DIVIDE (p1,p2) = Token.TOKEN (ParserData.LrTable.T 17,(
ParserData.MlyValue.VOID,p1,p2))
fun EQ (p1,p2) = Token.TOKEN (ParserData.LrTable.T 18,(
ParserData.MlyValue.VOID,p1,p2))
fun NEQ (p1,p2) = Token.TOKEN (ParserData.LrTable.T 19,(
ParserData.MlyValue.VOID,p1,p2))
fun LT (p1,p2) = Token.TOKEN (ParserData.LrTable.T 20,(
ParserData.MlyValue.VOID,p1,p2))
fun LE (p1,p2) = Token.TOKEN (ParserData.LrTable.T 21,(
ParserData.MlyValue.VOID,p1,p2))
fun GT (p1,p2) = Token.TOKEN (ParserData.LrTable.T 22,(
ParserData.MlyValue.VOID,p1,p2))
fun GE (p1,p2) = Token.TOKEN (ParserData.LrTable.T 23,(
ParserData.MlyValue.VOID,p1,p2))
fun AND (p1,p2) = Token.TOKEN (ParserData.LrTable.T 24,(
ParserData.MlyValue.VOID,p1,p2))
fun OR (p1,p2) = Token.TOKEN (ParserData.LrTable.T 25,(
ParserData.MlyValue.VOID,p1,p2))
fun ASSIGN (p1,p2) = Token.TOKEN (ParserData.LrTable.T 26,(
ParserData.MlyValue.VOID,p1,p2))
fun ARRAY (p1,p2) = Token.TOKEN (ParserData.LrTable.T 27,(
ParserData.MlyValue.VOID,p1,p2))
fun IF (p1,p2) = Token.TOKEN (ParserData.LrTable.T 28,(
ParserData.MlyValue.VOID,p1,p2))
fun THEN (p1,p2) = Token.TOKEN (ParserData.LrTable.T 29,(
ParserData.MlyValue.VOID,p1,p2))
fun ELSE (p1,p2) = Token.TOKEN (ParserData.LrTable.T 30,(
ParserData.MlyValue.VOID,p1,p2))
fun WHILE (p1,p2) = Token.TOKEN (ParserData.LrTable.T 31,(
ParserData.MlyValue.VOID,p1,p2))
fun FOR (p1,p2) = Token.TOKEN (ParserData.LrTable.T 32,(
ParserData.MlyValue.VOID,p1,p2))
fun TO (p1,p2) = Token.TOKEN (ParserData.LrTable.T 33,(
ParserData.MlyValue.VOID,p1,p2))
fun DO (p1,p2) = Token.TOKEN (ParserData.LrTable.T 34,(
ParserData.MlyValue.VOID,p1,p2))
fun LET (p1,p2) = Token.TOKEN (ParserData.LrTable.T 35,(
ParserData.MlyValue.VOID,p1,p2))
fun IN (p1,p2) = Token.TOKEN (ParserData.LrTable.T 36,(
ParserData.MlyValue.VOID,p1,p2))
fun END (p1,p2) = Token.TOKEN (ParserData.LrTable.T 37,(
ParserData.MlyValue.VOID,p1,p2))
fun OF (p1,p2) = Token.TOKEN (ParserData.LrTable.T 38,(
ParserData.MlyValue.VOID,p1,p2))
fun BREAK (p1,p2) = Token.TOKEN (ParserData.LrTable.T 39,(
ParserData.MlyValue.VOID,p1,p2))
fun NIL (p1,p2) = Token.TOKEN (ParserData.LrTable.T 40,(
ParserData.MlyValue.VOID,p1,p2))
fun FUNCTION (p1,p2) = Token.TOKEN (ParserData.LrTable.T 41,(
ParserData.MlyValue.VOID,p1,p2))
fun VAR (p1,p2) = Token.TOKEN (ParserData.LrTable.T 42,(
ParserData.MlyValue.VOID,p1,p2))
fun TYPE (p1,p2) = Token.TOKEN (ParserData.LrTable.T 43,(
ParserData.MlyValue.VOID,p1,p2))
fun UMINUS (p1,p2) = Token.TOKEN (ParserData.LrTable.T 44,(
ParserData.MlyValue.VOID,p1,p2))
end
end
