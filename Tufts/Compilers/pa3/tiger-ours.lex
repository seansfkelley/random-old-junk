val lineNum = ErrorMsg.lineNum
val linePos = ErrorMsg.linePos
fun err(p1,p2) = ErrorMsg.error p1

val comment_depth = ref 0

fun eof() = let 
                val pos = hd(!linePos) 
            in     
                if !comment_depth > 0
                then (ErrorMsg.error pos ("unclosed comment reaches end of file"); Tokens.EOF(pos, pos))
                else Tokens.EOF(pos, pos) 
            end

type svalue = Tokens.svalue
type pos = int
type ('a,'b) token = ('a,'b) Tokens.token
type lexresult = (svalue,pos) token

%%

%header (functor TigerLexFun(structure Tokens: Tiger_TOKENS));

alpha = [a-zA-Z];
digit = [0-9];
%s COMMENT;

%%

<COMMENT, INITIAL> \n   => (lineNum := !lineNum + 1; linePos := yypos :: !linePos; continue());
<INITIAL> [ \t]         => (continue());

<COMMENT, INITIAL> "/*" => (YYBEGIN COMMENT; comment_depth := !comment_depth + 1; continue());
<COMMENT> .             => (continue());
<COMMENT> "*/"          => (comment_depth := !comment_depth - 1; if !comment_depth = 0 then YYBEGIN INITIAL else YYBEGIN COMMENT; continue());

<INITIAL> \"([ -[\]-~] | \\n | \\t | \\\^[@-_] | \\[0-9]{3} | \\\" | \\\\)*\" => (Tokens.STRING(yytext, yypos, yypos + size(yytext)));
<INITIAL> \"[ -~]*\\.[ -~]*\" => (ErrorMsg.error yypos ("string contains illegal escape sequence"); continue());
<INITIAL> \"([ !#-~] | \\\")* => (ErrorMsg.error yypos ("unclosed string literal"); continue());

<INITIAL> array    => (Tokens.ARRAY(yypos, yypos + 5));
<INITIAL> break    => (Tokens.BREAK(yypos, yypos + 5));
<INITIAL> do       => (Tokens.DO(yypos, yypos + 2));
<INITIAL> else     => (Tokens.ELSE(yypos, yypos + 4));
<INITIAL> end      => (Tokens.END(yypos, yypos + 3));
<INITIAL> for      => (Tokens.FOR(yypos, yypos + 3));
<INITIAL> function => (Tokens.FUNCTION(yypos, yypos + 8));
<INITIAL> if       => (Tokens.IF(yypos, yypos + 2));
<INITIAL> in       => (Tokens.IN(yypos, yypos + 2));
<INITIAL> let      => (Tokens.LET(yypos, yypos + 3));
<INITIAL> nil      => (Tokens.NIL(yypos, yypos + 3));
<INITIAL> of       => (Tokens.OF(yypos, yypos + 2));
<INITIAL> then     => (Tokens.THEN(yypos, yypos + 4));
<INITIAL> to       => (Tokens.TO(yypos, yypos + 2));
<INITIAL> type     => (Tokens.TYPE(yypos, yypos + 4));
<INITIAL> var      => (Tokens.VAR(yypos, yypos + 3));
<INITIAL> while    => (Tokens.WHILE(yypos, yypos + 5));

<INITIAL> "}"      => (Tokens.RBRACE(yypos, yypos + 1));
<INITIAL> "{"      => (Tokens.LBRACE(yypos, yypos + 1));
<INITIAL> "]"      => (Tokens.RBRACK(yypos, yypos + 1));
<INITIAL> "["      => (Tokens.LBRACK(yypos, yypos + 1));
<INITIAL> ")"      => (Tokens.RPAREN(yypos, yypos + 1));
<INITIAL> "("      => (Tokens.LPAREN(yypos, yypos + 1));
<INITIAL> ";"      => (Tokens.SEMICOLON(yypos, yypos + 1));
<INITIAL> ":"      => (Tokens.COLON(yypos, yypos + 1));
<INITIAL> ","      => (Tokens.COMMA(yypos, yypos+1));
<INITIAL> ":="     => (Tokens.ASSIGN(yypos, yypos + 2));
<INITIAL> ">="     => (Tokens.GE(yypos, yypos + 2));
<INITIAL> ">"      => (Tokens.GT(yypos, yypos + 1));
<INITIAL> "<="     => (Tokens.LE(yypos, yypos + 2));
<INITIAL> "<"      => (Tokens.LT(yypos, yypos + 1));
<INITIAL> "<>"     => (Tokens.NEQ(yypos, yypos + 2));
<INITIAL> "="      => (Tokens.EQ(yypos, yypos + 1));
<INITIAL> "&"      => (Tokens.AND(yypos, yypos + 1));
<INITIAL> "|"      => (Tokens.OR(yypos, yypos + 1));
<INITIAL> "*"      => (Tokens.TIMES(yypos, yypos + 1));
<INITIAL> "/"      => (Tokens.DIVIDE(yypos, yypos + 1));
<INITIAL> "+"      => (Tokens.PLUS(yypos, yypos + 1));
<INITIAL> "-"      => (Tokens.MINUS(yypos, yypos + 1));
<INITIAL> "."      => (Tokens.DOT(yypos, yypos + 1));

<INITIAL> [a-zA-Z][a-zA-Z0-9_]* => (Tokens.ID(yytext, yypos, yypos + size(yytext)));
<INITIAL> [0-9]+                => (Tokens.INT(valOf(Int.fromString(yytext)), yypos, yypos + size(yytext)));

<INITIAL> .        => (ErrorMsg.error yypos ("illegal character " ^ yytext); continue());