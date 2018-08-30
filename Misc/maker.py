import ply.yacc as yacc
import ply.lex as lex
import sys
import os
import getopt

sources=('.cpp','.cc','.c++','.cp')
headers=('.h','.hh','.hpp')

#------------------------------------------------------------------define tokens
tokens=('INCLUDE',
        'FILENAME',
        'CATCHALL')

t_ignore=' \t'

def t_INCLUDE(t):
    r'\#include'
    return t

def t_FILENAME(t):
    r'".+"'
    return t

def t_CATCHALL(t):
    r'.+'
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno+=1

def t_error(t):
    print 'Error (line %d) at character \'%s\'' % (t.lexer.lineno, t.value[0])
    t.lexer.skip(1)

lexer=lex.lex()

#-----------------------------------------------------------------define grammar
filename=""

def p_include_line(p):
    'line : INCLUDE FILENAME'
    dependencies[filename].append(p[2][1:-1])

def p_catchall(p):
    'line : CATCHALL'
    pass

def p_error(p):
    #print 'error: line %d in file \'%s\'' % (lineno, filename)
    pass

#------------------------------------------------------------------parse options
short_opt={'--program':'-p',
           '--makefile':'-m',
           '--compiler':'-c',
           '--options':'-o',
           '--test':'-t',
           '--directory':'-d'}

opt_list, args=getopt.getopt(sys.argv[1:], 'p:m:c:o:t:d:', 
                             ['program=','makefile=','compiler=','options=','test=', 'directory='])

if len(args)>0:
    print 'Excess arguments: '+str(args)

options={'-p':'a.out',
         '-m':'Makefile',
         '-c':'g++',
         '-d':os.getcwd()} #cwd is where the program is called from, not where it lives

for (arg, opt) in opt_list:
    if len(arg)>2:
        arg=short_opt[arg]
    options[arg]=opt

for v in short_opt.values():
    if not options.has_key(v):
        options[v]=''

#------------------------------------------------------------------parse grammar
parser=yacc.yacc()

dependencies={}
object_files={}

def valid_cpp_filename(f):
    return f.endswith(sources) or f.endswith(headers)

for f in os.listdir(options['-d']):
    filename=f.strip(' \n\t')
    if not valid_cpp_filename(f):
        continue
    try:
        cpp_file=open(filename)
    except IOError:
        continue
    if filename.endswith(sources):
        object_files[filename]=filename[:-3]+'o'
    lineno=0
    dependencies[filename]=[]
    for l in cpp_file:
        #print l
        lineno+=1
        parser.parse(l)
    #print '%s:\n%s\n' % (l, pc)

#-------------------------------------------------------generate makefile header
makefile=open(os.path.join(options['-d'],options['-m']), 'w')

makefile.write('OBJECTS=')
for o in sorted(object_files.values()):
    makefile.write(o+' ')
makefile.write('\n')

makefile.write('CC=%s\n' % options['-c'])
makefile.write('NAME=%s\n'% options['-p'])
makefile.write('OPTS=%s\n' % options['-o'])
makefile.write('TESTPARAMS=%s\n\n' % options['-t'])
makefile.write('test: $(NAME) $(TESTPARAMS)\n\t./$(NAME) $(TESTPARAMS)\n\n')
makefile.write('$(NAME): $(OBJECTS)\n\trm -f $(NAME); $(CC) $(OBJECTS) $(OPTS) -o $(NAME)\n\n')

#---------------------------------------------------generate makefile directives
def comp_filenames(one, two):
    if one.endswith(headers):
        priority1=0
    else:
        priority1=1
        
    if two.endswith(headers):
        priority2=0
    else:
        priority2=1
    
    if priority1==priority2:
        return cmp(one[:one.rfind('.')], two[:two.rfind('.')]) #compare non-extension part
    else:
        return priority1-priority2

filenames=sorted(dependencies.keys(), comp_filenames)

for f in filenames:
    if f in object_files:
        makefile.write(object_files[f]+': '+f+' ')
    else:
        makefile.write(f+': ')
    for d in sorted(dependencies[f], comp_filenames):
        makefile.write(d+' ')
    makefile.write('\n')
    if f.endswith(sources):
        makefile.write('\t$(CC) $(OPTS) -c '+f+'\n')
    makefile.write('\n')

makefile.write('clean:\n\trm -f $(OBJECTS)')

makefile.close()
