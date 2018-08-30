import sys
import marshal

if len(sys.argv) < 2:
	print 'Usage: %s movie-backup-filename' % sys.argv[0]

try:
    f = open(sys.argv[1], 'rb')
except IOError:
    print 'No backup file found; not stripping movies with errors.'
    sys.exit(0)
    
cached_movies = marshal.load(f)
f.close()
print 'Loaded %d cached movies.' % len(cached_movies)

stripped_movies = {}
for (title, movie_info) in cached_movies.iteritems():
    if movie_info['imdb_had_movie']:
        stripped_movies[title] = movie_info

print 'Stripped %d movies with no IMDb results.' % (len(cached_movies) - len(stripped_movies))

f = open(sys.argv[1], 'wb')
marshal.dump(stripped_movies, f)
f.close()
print 'Successfully wrote new cache with %d movies.' % len(stripped_movies)