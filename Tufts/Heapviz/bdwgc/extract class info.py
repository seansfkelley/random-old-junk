# This script parses output from dwarfdump (the version running on the Halligan servers --
# the OS X version has a different output format) and pulls out type information that it 
# then prints to stdout. This information consists of class names, their sizes, and a list
# of the member variables with as much type, size, etc. information as can be recovered.

# To do: figure out how to resolve ordering of types (especially w/r/t const, volatile
# etc. modifiers). DWARF presents them in English order, but that's not how C/C++ parses
# it out. See page 38 (40 in the PDF) for an example.

import sys
import re

filename = '/dev/stdin'

if len(sys.argv) > 1:
    filename = sys.argv[1]

# Map of type identifiers (hexadecimal) onto one of the following type classes. Types
# that represent some level of nesting (typedef, pointer, array) follow multiple maps
# in order to construct their complete type.
types = {}

# List maintaining the classes in the file, in the order they appear.
classes = []

# The input file used by this program. All classes operate on this file and advance its
# location as they parse out the information relevant to them.
input_file = open(filename, 'r')

# Some regular expressions used by multiple functions.
match_tag = re.compile('DW_TAG_[a-z_]+')
match_at = re.compile('DW_AT_[a-z_]+')
match_quote_string = re.compile('"(.+)"')
match_hex = re.compile('0x[0-9a-fA-F]+')

# Basic structure: the file is looped over until a DW_TAG is found. Control is handed to 
# appropriate class for that tag (or UnknownType if there is no such class). That class
# loops over the file and collects all the information it can to construct itself (following
# the model of Type), and returns the last line it uses (i.e. the one that terminated the
# parsing loop, which is always the next logical block of the input). The calling function
# adds the newly constructed type to the type map, and uses the returned line of input to
# decide which type to construct next (or to skip the block, if necessary).
#
# After the file is parsed, the classes are printed out, with their types resolved by
# traversing the map populated with Type instances.

# Base type used for primitives.
class Type:
    attributes = {'DW_AT_name' : ('name',   lambda l: match_quote_string.search(l).group(1))}
    
    def __init__(self):
        self.name = None
        self.type = None
    
    # This is the same for all non-ClassType instances. Each class supplies an 'attributes'
    # dictionary that maps DW_AT names onto (attr, func) pairs, where attr names the
    # attribute of this object to set to the output of func, a function which takes the
    # entire line corresponding to the DW_AT and returns a value to store in attr.
    #
    # This value is then used in resolve_name when types must be resolved in a manner specific
    # to each subclass.
    def parse_from_file(self, l):
        self.type = match_hex.search(l).group(0)
    
        l = input_file.readline()
        while l[0] != '<':
            for (at_name, (obj_attr_name, value_func)) in self.attributes.items():
                if at_name in l:
                    setattr(self, obj_attr_name, value_func(l))
            l = input_file.readline()

        return l
    
    # Resolve the name of this type by recursively traversing the type map (until a base
    # case of type Type or ClassType is encountered, or unknown). 
    #
    # Subclasses have a more interesting implementation that actually uses the map. Type
    # represents a base case of type resolution.
    def resolve_name(self):
        return self.name

# Represents a reference to an unknown type. Supports all the same operations as actual
# types, but will simply skip a block (instead of parsing it) and has a fixed name/type.
class UnknownType(Type):
    def __init__(self):
        Type.__init__(self)
        self.name = 'unknown'
        self.type = None

    def parse_from_file(self, l):
        l = input_file.readline()
        while l[0] != '<':
            l = input_file.readline()
        return l

# Represents a const modifier.
class ConstType(Type):
    attributes = {'DW_AT_type' : ('target', lambda l: match_hex.search(l).group(0))}

    def __init__(self):
        Type.__init__(self)
        self.target = None

    def resolve_name(self):
        if self.target in types:
            return 'const ' + types[self.target].resolve_name()
        else:
            return 'const unknown'

# Represents an arbitrary pointer.
class PointerType(Type):
    attributes = {'DW_AT_type' : ('target', lambda l: match_hex.search(l).group(0))}
    
    def __init__(self):
        Type.__init__(self)
        self.target = None
    
    def resolve_name(self):
        if self.target in types:
            return types[self.target].resolve_name() + '*'
        else:
            return 'unknown*'

# Represents a typedef. Shows the typedef'd name as well as the full type.
class TypedefType(Type):
    attributes = {'DW_AT_name' : ('name',   lambda l: match_quote_string.search(l).group(1)),
                'DW_AT_type' : ('target', lambda l: match_hex.search(l).group(0))}
    
    def __init__(self):
        Type.__init__(self)
        self.target = None
    
    def resolve_name(self):
        if self.target in types:
            return self.name + ' (' + types[self.target].resolve_name() + ')'
        else:
            return self.name + ' (unknown)'

# Represents an arbitrary array type.
class ArrayType(Type):
    attributes = {'DW_AT_type' : ('element', lambda l: match_hex.search(l).group(0))}
    
    def __init__(self):
        Type.__init__(self)
        self.element = None

    def resolve_name(self):
        if self.element in types:
            return types[self.element].resolve_name() + '[]'
        else:
            return 'unknown[]'

# Represents a class. Along with primitives, they are the base case for full type
# resolution. Maintains a list of MemberInfo objects (following) that keep track of the
# information describing each member variable.
class ClassType(Type):    
    def __init__(self):
        Type.__init__(self)
        self.size = None
        self.print_depth = 0
        self.members = []

    def parse_from_file(self, l):
        get_depth = lambda s: int(s[1:s.find('>')])
        depth= get_depth(l)

        self.type = match_hex.search(l).group(0)
        self.print_depth = (depth - 1) * 2
        classes.append(self)

        l = input_file.readline()
        # Parse out information about the class itself.
        while l[0] != '<':
            if 'DW_AT_name' in l:
                self.name = match_quote_string.search(l).group(1)
            elif 'DW_AT_byte_size' in l:
                self.size = int(l[l.find('0x'):], 16)
            l = input_file.readline()

        # Parse out information about nested classes and data members.
        while get_depth(l) > depth:
            m = match_tag.search(l)
            if 'DW_TAG_member' in l:
                # Parse out data-member blocks.
                m = MemberInfo()
                l = m.parse_from_file()
                self.members.append(m)
            elif m:
                # Nested classes, types, etc.
                t = type_handlers.get(m.group(0), UnknownType)()
                l = t.parse_from_file(l)
                types[t.type] = t 
            else:
                # Skip non-data-member, non-nested-type blocks.
                l = input_file.readline()
                while l[0] != '<':
                    l = input_file.readline()

        # Return the line that caused as to terminate, as described above, so that the
        # next step of the program has the correct starting line.
        return l
    
    def resolve_name(self):
        return self.name if self.name else self.type

    def print_with_indent(self):
        indent = ' ' * self.print_depth
        print indent + 'class ' + self.resolve_name() + ((' (%d bytes)' % self.size) if self.size else '')
        for m in self.members:
            print indent + '  ' + str(m)

# Represents a member variable, holding as much information as is provided of name, type,
# and offset from the base of the class.
class MemberInfo:
    def __init__(self):
        self.offset = 0
        self.name = '<anon member>'
        self.type = None

    def __str__(self):
        t = get_type(self.type)
        return '%6s%s%s' %  ('0x%x  ' % self.offset,
                            get_type(self.type),
                            (' ' * (30 - len(t))) + '  ' + self.name)
    
    def parse_from_file(self):
        l = input_file.readline()
        while l[0] != '<':
            if 'DW_AT_name' in l:
                self.name = match_quote_string.search(l).group(1)
            elif 'DW_AT_type' in l:
                self.type = match_hex.search(l).group(0)
            elif 'DW_AT_data_member_location' in l:
                self.offset = int(l[l.rfind(' '):])
            l = input_file.readline()
        return l


# Type and its subclasses know how to recursively resolve the types they represent.
# This function is an entry point that begins with a unique hexadecimal identifier,
# not starting the process if that type is unknown.
def get_type(t):
    if t in types:
        return types[t].resolve_name()
    else:
        return t

# Register classes that know how to parse a block of the input file based off the tag that
# begins the block. For unknown tags that match, UnknownType can be used.
type_handlers = {
    'DW_TAG_structure_type' :   ClassType,
    'DW_TAG_class_type' :       ClassType,
    'DW_TAG_union_type' :       ClassType,
    'DW_TAG_base_type' :        Type,
    'DW_TAG_const_type' :       ConstType,
    'DW_TAG_pointer_type' :     PointerType,
    'DW_TAG_typedef' :          TypedefType,
    'DW_TAG_array_type' :       ArrayType,
    'DW_TAG_enumeration_type' : Type # Because the names of the enumerated values are not
                                     # used, these two classes are functionally identical.
}

# Top level loop for parsing the input file.
l = input_file.readline()
while len(l) > 0:
    m = match_tag.search(l)
    if m:
        t = type_handlers.get(m.group(0), UnknownType)()
        l = t.parse_from_file(l)
        types[t.type] = t
    else:
        l = input_file.readline()

# Finally, output all the information we have collected.
for c in classes:
    c.print_with_indent()
    print
