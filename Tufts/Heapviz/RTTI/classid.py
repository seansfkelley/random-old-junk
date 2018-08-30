import sys
import shutil
import re
import pickle

if len(sys.argv) == 1:
    print 'Usage: %s filenames' % sys.argv[0]
    sys.exit(0)

def identifier_character(c):
    return c.isalnum() or c == '_'

# Functor that maintains global count and mapping of integer class IDs. Feed it individual
# lines of C++ sourse files in order, calling reset() between each file.
#
# The source-checking code is very simplistic. It does NOT understand comments and may
# misunderstand them as real code (watch out for braces and the 'class' keyword), among
# other things.
class AddClassID:
    def __init__(self):
        self.reset()
        self.classmap = {}
        self._cur_classid = 0
        
    def reset(self):
        self._cur_class = None
        self._brace_count = 0
        self._line = 0
    
    # Function to insert the classid field into classes and keep track of which classes
    # hve been found. 
    def field(self, line):
        original_line = line
        self._line += 1
        if  'class' in line:
            # Verify that the instance of 'class' here is a keyword, not a comment or
            # part of some other identifier. This is not the most accurate check w/r/t
            # the C++ grammar, but it's good enough for now.
            i = line.find('class')
            if not ((i > 0 and identifier_character(line[i - 1])) or identifier_character(line[i + 5])):                
                if self._cur_class:
                    raise Exception('line %d: nested class?' % self._line)
                classname_substring = line[line.find('class') + 5:] + ' '
                brace, colon = classname_substring.find('{'), classname_substring.find(':')
                if min(brace, colon) == -1:
                    classname = classname_substring[:max(brace, colon)]
                else:
                    classname = classname_substring[:min(brace, colon)]
                self._cur_class = classname.strip()
                self._brace_count = 0
        if self._cur_class:
            self._brace_count += line.count('{') - line.count('}')
            if self._brace_count == 0:
                i = line.rfind('}')
                line = line[:i] + 'private: int __classid;' + line[i:]
                self.classmap[self._cur_classid] = self._cur_class
                self._cur_class = None
                self._cur_classid += 1
        print 'line %d (class: %s, braces: %d): "%s"' % (self._line, self._cur_class, self._brace_count, line.rstrip())
        return line
    
    
    # Function to insert classid field initializations into class constructors


add_classid = AddClassID()

for filename in sys.argv[1:]:
    try:
        shutil.copyfile(filename, filename + '.backup')
        f = open(filename, 'r')
        add_classid_field.reset()
        lines = map(add_classid.field, f.readlines())
        f.close()
        f = open(filename, 'w')
        f.writelines(lines)
        f.close()
        
    except IOError as e:
        print e

with open('classid_map.dict', 'w') as f:
    pickle.dump(add_classid_field.classmap, f)

for filename in sys.argv[1:]:
    try:
        f = open(filename, 'r')
        add_classid.reset()
        lines = map(add_classid., f.readlines())
        f.close()
        f = open(filename, 'w')
        f.writelines(lines)
        f.close()

    except IOError as e:
        print e