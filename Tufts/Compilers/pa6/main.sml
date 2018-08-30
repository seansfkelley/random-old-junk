structure Main =
struct 
    fun compile filename = 
        let
            fun registername (t) = 
                case Temp.Table.look(x86Frame.tempMap, t) of
                      SOME(r) => #name r
                    | NONE => Temp.makestring t
            
            fun print_tree_assem (tree, frame) = 
                let
                    fun flatten([]) = []
                      | flatten(l :: ls) = l @ flatten ls
                  
                    val body = flatten (map (Codegen.codegen frame) (Canon.linearize(tree)))
                    val {prolog, body, epilog} = 
                        case frame of 
                              SOME(f) => x86Frame.procEntryExit3(f, body)
                            | NONE => {prolog = "", body = body, epilog = ""}
                in
                    (TextIO.print prolog;
                     map TextIO.print (map (Assem.format registername) (Codegen.emitParamMoves frame));
                     map TextIO.print (map (Assem.format registername) body);
                     TextIO.print epilog)
                end
            
            fun process_fragments (x86Frame.PROC{frame, body} :: fs) = (print_tree_assem(body, SOME(frame)); process_fragments(fs))
              | process_fragments (x86Frame.STRING(l, s) :: fs) = (TextIO.print (Symbol.name l ^ ":\n.ascii \"" ^ String.toString s ^ "\"\n"); process_fragments(fs))
              | process_fragments ([]) = ()
            
            val body = Semant.transProg (Parse.parse filename)
        in
            (process_fragments(Trans.getFragments());
            print_tree_assem (body, NONE); true)
        end
end

(* CM.make "sources.cm" andalso Main.compile "queens.tig"; *)
(* (CM.make "sources.cm"; Main.compile "queens.tig"); *)
(*
CM.make "sources.cm";
Main.compile "queens.tig";
*)