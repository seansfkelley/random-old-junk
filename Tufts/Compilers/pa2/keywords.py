for word in sorted(['array', 'if', 'then', 'else', 'while', 'for', 'to', 'do', 'let', 'in', 'end', 'of', 'break', 'nil', 'function', 'var', 'type']):
    print '%s%s => (Tokens.%s(yypos, yypos + %d));' % \
        (word, ' ' * (8 - len(word)), word.upper(), len(word))
