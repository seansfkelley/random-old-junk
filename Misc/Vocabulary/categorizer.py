import stemmer
import sys
import re

ps = stemmer.PorterStemmer()

stemmed_words = {}

if len(sys.argv) > 1:
    f = open(sys.argv[1], 'r')
    for line in f:
        line = line.strip().lower()
        for word in re.findall('[a-z\']+', line):
            stem = ps.stem(word, 0, len(word) - 1)
            stemmed_words[stem] = stemmed_words.get(stem, 0) + 1
    f.close()

for stem, count in sorted(list(stemmed_words.items()), key = lambda x: x[1], reverse = True):
    print stem, count