# To do -- use Google Search API instead of IMDb search, it's smarter. Then retrieve the IMDb URL from Google
# and query IMDb for that information.
# Sidebar that holds whatever summary was last requested? Perhaps with a title and link to the movie? Maybe
# have covers act as toggles that switch between movie title and movie summary in the middle column?
# How to detect clicks on background?
# Javascript -- write file with a set date/tme

import sys
import os
import marshal
import time
import cgi
import shutil
import re
import ast
import urllib
import urllib2

if len(sys.argv) != 4:
    print 'Usage: %s input-directory output-filename placeholder-image' % sys.argv[0]
    sys.exit(1)

# Check if directory exists.
try:
    if not os.path.exists(sys.argv[1]):
        print 'Error: %s is not an existing directory' % sys.argv[1]
        sys.exit(1)
except:
    print 'Error: %s is inaccessible' % sys.argv[1]
    sys.exit(1)

# Make sure we can have a file.
try:
    if not os.path.exists(os.path.dirname(sys.argv[2])):
        print 'Error: %s is not an existing directory' % os.path.dirname(sys.argv[2])
        sys.exit(1)
except:
    print 'Error: %s is inaccessible' % sys.argv[2]
    sys.exit(1)

# Make sure the placeholder image exists or is at least an HTTP URL.
if sys.argv[3][:7].lower() != 'http://':
    try:
        if not os.path.exists(sys.argv[3]):
            print 'Error: %s does not exist' % sys.argv[3]
            sys.exit(1)
    except:
        print 'Error: %s is inaccessible' % sys.argv[3]
        sys.exit(1)

# Check the modification time saved in the HTML against the modification time of the folder;
# skip updating if they match (nothing has changed since it was written). Update the modification
# time of the HTML file itself (in the Javascript) appropriately.
FOLDER_MODIFICATION_TIME = int(os.path.getmtime(sys.argv[1]))

if os.path.exists(sys.argv[2]):
    f = open(sys.argv[2], 'r+')
    try:
        timestamp = int(f.readline().strip('<>!-\t\n '))
    except:
        timestamp = -1
    
    if timestamp == FOLDER_MODIFICATION_TIME:
        print 'File is already up to date, updating modification timestamp.'
        
        l = f.readline()
        while 'var WRITE_TIME' not in l:
            l = f.readline()
        # We know the timestamp is 16 characters long and is at the end of the line (+1 for newline),
        # so seek back 17 characters and then overwrite the timestamp with the new one.
        f.seek(-17, os.SEEK_CUR)
        f.write('%16d' % int(time.time()))
        
        f.close()
        print 'Timestamp updated, exiting.'
        sys.exit()
    
    f.close()

# Try to read in a stored version of the movie list.
if os.path.exists(sys.argv[2] + '.bak'):
    f = open(sys.argv[2] + '.bak', 'rb')
    cached_movies = marshal.load(f)
    f.close()
    print 'Loaded %d cached movies.' % len(cached_movies)
else:
    print 'No cached movie file was found.'
    cached_movies = {}

print 'Beginning IMDb queries.'

movies_dict = {}

num_movies = cache_hits = queries = successful_queries = 0

def format_for_sort(title):
    if '(' in title or '[' in title or '{' in title:
        title = title[:min(title.find('(') if '(' in title else len(title),
                           title.find('[') if '[' in title else len(title),
                           title.find('{') if '{' in title else len(title))]
    title = title.lower()
    
    if title.startswith('the '):
        return title[4:]
    else:
        return title

def format_for_query(title):
    if '(' in title or '[' in title or '{' in title:
        title = title[:min(title.find('(') if '(' in title else len(title),
                           title.find('[') if '[' in title else len(title),
                           title.find('{') if '{' in title else len(title))]
    title = title.strip()
    return urllib.quote_plus(title.lower())

class BrowserUserAgentURLopener(urllib.URLopener):
    version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1201.0 Safari/537.1'

urlopener = BrowserUserAgentURLopener()

for f in os.listdir(sys.argv[1]):
    # Ignore Unix hidden files.
    if f[0] == '.':
        continue
    
    num_movies += 1
    
    # Get rid of extension.
    f = os.path.splitext(f)[0].replace(':', '/')
    
    # Movie already has a listing so copy it.
    if f in cached_movies and cached_movies[f].get('imdb_had_movie', False):
        cache_hits += 1
        movies_dict[f] = cached_movies[f]
        continue
    
    queries += 1
    
    try:
        google_result = urlopener.open('https://www.google.com/search?q=%s+site:imdb.com' % format_for_query(f))
        google_result_text = google_result.read()
        google_result.close()
    except IOError, e:
        # Google probably denying due to too many searches in succession.
        print 'Error while connecting to Google.'
        print e
        continue
    except urllib2.URLError, e:
        # Unknown error.
        print 'Error while connecting to Google.'
        print e
        continue
    
    start = google_result_text.find('<cite>www.imdb.com/title/')
    url = google_result_text[start+6:google_result_text.find('</cite>', start)]
    
    try:
        imdb_result = urllib2.urlopen('http://www.imdbapi.com/?i=%s' % re.search(r'tt\d+', url).group(0))
        movie_json = imdb_result.read()
        imdb_result.close()
    except urllib2.URLError, e:
        # Unknown error.
        print 'Error while connecting to imdbapi.com.'
        print e
        continue
    except AttributeError, e:
        # Movie was not first search result, assume for now it doesn't exist with this title.
        print 'No movie found for %s.' % f
        movies_dict[f] = {'imdb_had_movie' : False, 'title' : f, 'sorting_title' : format_for_sort(f), 'kind' : 'unknown'}
        continue
    
    movie = ast.literal_eval(movie_json)
    
    if movie['Response'] == 'False':
        movies_dict[f] = {'imdb_had_movie' : False, 'title' : f, 'sorting_title' : format_for_sort(f), 'kind' : 'unknown'}
        continue
    
    successful_queries += 1
    
    # Get the relevant information for the movie.
    m_dict = {'imdb_had_movie' : True,
              'title' : f,
              'sorting_title' : format_for_sort(f),
              # Does not account for accidental classifications of movie for VGs, etc.
              'kind' : 'tv' if ('TV' in movie['Rated'] and 'hr' not in movie['Runtime']) else 'movie',
              'url' : 'http://www.imdb.com/title/%s/' % movie['imdbID'],
              'plot' : movie['Plot'],
              'genres' : movie['Genre'],
              'rating' : movie['imdbRating'],
              'cover url' : movie['Poster']
             }
        
    movies_dict[f] = m_dict

print 'Finished queries for %d movies/shows: %d cache hits, %d/%d queries successful.' % (num_movies, cache_hits, successful_queries, queries)

print 'Writing cache file.'

dict_file = open(sys.argv[2] + '.bak', 'wb')
marshal.dump(movies_dict, dict_file)
dict_file.close()

print 'Building layout table.'

def compute_layout_table(movie_or_tv_list):
    if len(movie_or_tv_list) == 0:
        return []
    
    rows = (len(movie_or_tv_list) / 2) * 4 + 1
    if len(movie_or_tv_list) % 2 == 1:
        rows += 2
    
    # Indexed by row/column
    table = [[None] * 3 for i in xrange(rows)]
    
    # Precompute the entire table that will be output
    # First do middle (name) column
    for i in xrange(rows):
        if i % 2 == 1:
            table[i][1] = movie_or_tv_list[(i - 1) / 2]
        else:
            table[i][1] = ''
    
    # Second do alternating cover art columns
    for (i, u) in enumerate(movie_or_tv_list):
        if i % 2 == 0:
            r = 4 * (i / 2)
            c = 0
        else:
            r = 4 * ((i - 1) / 2) + 2
            c = 2
    
        table[r][c] = u
        if r + 3 < rows:
            table[r + 3][c] = ''
    
    # Add an empty cell to even out the one-element table.
    if len(movie_or_tv_list) == 1:
        table[0][2] = ''
    
    return table

movies = sorted(movies_dict.values(), lambda x, y: cmp(x['sorting_title'], y['sorting_title']))

movie_list = []
tv_list = []
other_list= []

# Sort movies into categories; convert all properties to be HTML-safe if they are strings.
for m in movies:
    tmp = {}
    for (k, v) in m.items():
        if isinstance(v, str):
            tmp[k] = cgi.escape(v, True)
        elif isinstance(v, unicode):
            tmp[k] = cgi.escape(v, True).encode('ascii', 'xmlcharrefreplace')
        else:
            tmp[k] = v
    m = tmp
    
    if 'movie' in m['kind']: # Includes TV movies.
        movie_list.append(m)
    elif 'tv' in m['kind']:
        tv_list.append(m)
    else:
        other_list.append(m)

movie_table = compute_layout_table(movie_list)
tv_table = compute_layout_table(tv_list)
other_table = compute_layout_table(other_list)

# None -> produce no cell
# '' -> Produce a cell, but with no meaningful content (for layout purposes)
# Movie dictionary -> Depending on the location in the array, produce a clickable image or a title link

print 'Writing HTML file.'

if sys.argv[3][:7].lower() == 'http://':
    PLACEHOLDER_IMAGE_NAME = sys.argv[3]
else:
    PLACEHOLDER_IMAGE_NAME = os.path.split(sys.argv[3])[1]
    shutil.copy(sys.argv[3], os.path.join(os.path.dirname(sys.argv[2]), PLACEHOLDER_IMAGE_NAME))

# Reopen the file, for writing this time, which removes all previous contents.
html_file = open(sys.argv[2], 'w')

# Write timestamp for modification date of the folder.
html_file.write('<!-- %d -->' % FOLDER_MODIFICATION_TIME)

# Write header
html_file.write('''
<html>
    <head>
        <title>Movie Selection</title>''')

# Write styles
html_file.write('''
        <style type="text/css">
            .main{ border-spacing:0px;
                   font-size:14pt;
                   font-family:Optima;
                   margin-left:auto; 
                   margin-right:auto; }

            .cover_col{ width:95px; }
    
            .title_col{ width:300px; }

            .center{ text-align:center; }
    
            .fixed_height{ height:48px; }

            .placeholder{ width:95px; 
                          height:140px; }
        
            .movie_title{ font-size:14pt; }
        
            .movie_subtitle{ font-size:10pt; }
        
            .section_header { font-size:20pt; }
        
            .fine_print { font-size:8pt; }
        
            .navigation_options { font-size:10pt; }
            
            img { max-width:100px;
                  max-height:200px;
                  width:100%;
                  height:auto;
            }
        
            #summary { position:absolute;
                       padding:10px;
                       width:300px;
                       font-size:10pt; }
        </style>
    </head>''')

# Write body
# The 16-'digit' value for WRITE_TIME is very important; updates to the file use the fact that it
# is 16 characters to do an in-place overwriting instead of rewriting the whole file. ('Digit' because
# we cannot actually zero-pad the value: in that case, it would be interpreted as octal! Use spaces
# instead).
html_file.write('''
    <body>
        <script type="text/javascript">
        function findPos(obj) {
        	var curleft = curtop = 0
        	if (obj.offsetParent) {
        	    do {
        		    curleft += obj.offsetLeft
        			curtop += obj.offsetTop
        		} while (obj = obj.offsetParent)
        	}
        	return [curleft, curtop]
        }
        
        function clamp(num, min, max){
            return Math.min(max, Math.max(min, num))
        }
        
        function setSummary(source){
            var source_element = document.getElementById(source)
            var summary_element = document.getElementById("summary")
            
            summary_element.childNodes[0].innerHTML = source
            if (source_element.getAttribute("summary").length > 0){
                summary_element.childNodes[2].innerHTML = source_element.getAttribute("summary")
            }
            else{
                summary_element.childNodes[2].innerHTML = "No plot summary provided."
            }
            
            var p = findPos(source_element)
            summary_element.style.top = clamp(0, p[1] + (source_element.offsetHeight - summary_element.offsetHeight) / 2, document.body.offsetHeight - summary_element.offsetHeight)
            if (p[0] > document.body.offsetWidth / 2){
                summary_element.style.left = p[0] + source_element.offsetWidth
            }
            else{
                summary_element.style.left = p[0] - summary_element.offsetWidth
            }
        }
        
        function setTimeSinceModification(){
            var WRITE_TIME = %16d
            var current_time = new Date().getTime() / 1000
            
            var sec_diff = current_time - WRITE_TIME
            
            var day_diff = Math.floor(sec_diff / (60 * 60 * 24))
            sec_diff -= day_diff * (60 * 60 * 24)
            var hour_diff = Math.floor(sec_diff / (60 * 60))
            sec_diff -= hour_diff * (60 * 60)
            var minute_diff = Math.floor(sec_diff / 60)
            
            var timestamp = ""
            
            if (day_diff > 0){
                timestamp += day_diff + " day" + (day_diff > 1 ? "s" : "") + " "
            }
            if (hour_diff > 0){
                timestamp += hour_diff + " hour" + (hour_diff > 1 ? "s" : "") + " "
            }
            timestamp += minute_diff + " minute" + (minute_diff != 1 ? "s" : "") + " ago"
            
            document.getElementById("modification_timestamp").innerHTML = timestamp
            
            setTimeout("setTimeSinceModification()", 60000)
        }
        </script>
        
        <div id="summary" class="main"><div class="movie_title"></div><br><div class="movie_subtitle"></div></div>''' % int(time.time()))

def write_table_to_file(html_file, table):
    html_file.write('''
        <table class="main">
            <col class="cover_col"/>
            <col class="title_col"/>
            <col class="cover_col"/>''')
    
    for row in table:
        html_file.write('''
                <tr>''')
        for (i, cell) in enumerate(row):
            if cell is None:
                continue
            elif cell == '':
                html_file.write('''
                    <td class="fixed_height">&nbsp;</td>''')
            else:
                html_file.write('''
                    ''')
                if i == 1:
                    if cell.get('url', None) is not None:
                        html_file.write('<td class="center fixed_height"><a href="%s">%s</a>' % (cell['url'], cell['title']))
                    else:
                        html_file.write('<td class="center fixed_height">%s' % cell['title'])
                
                    html_file.write('<span class="movie_subtitle"><br/>')
                    if cell.get('genres', None) is not None:
                        html_file.write('<span>%s</span> ' % cell['genres'])
                
                    if cell.get('rating', None) is not None:
                        html_file.write('<span>(<b>%s</b>)</span>' % cell['rating'])
                
                    html_file.write('</span></td>')
                else:
                    if cell.get('cover url', None) is not None:
                        html_file.write('<td rowspan="3"><img src="%s" id="%s" onclick="setSummary(&quot;%s&quot;)" border="0" summary="%s"/></td>' % (cell['cover url'], cell['title'], cell['title'], cell.get('plot', '')))
                    else:
                        html_file.write('<td rowspan="3"><img src="%s" id="%s" onclick="setSummary(&quot;%s&quot;)" border="0" summary="%s"/></td>' % (PLACEHOLDER_IMAGE_NAME, cell['title'], cell['title'], cell.get('plot', '')))
        html_file.write('''
                </tr>''')
    html_file.write('''
        </table>''')


if len(movie_table) > 0:
    html_file.write('''
        <p class="main center section_header">
            <a name="movies">Movies</a>''')
    if len(tv_table) + len(other_table) > 0:
        html_file.write('''
            <br>
            <span class="navigation_options">''')
        if len(tv_table) > 0:
                html_file.write('''
                <a href="#tv">TV</a>''')
        if len(other_table) > 0:
            if len(tv_table) > 0:
                html_file.write(' &middot; ')
            html_file.write('''
                <a href="#other">Other</a>''')
        html_file.write('''
            </span>''')
    html_file.write('''
        </p>''')
    write_table_to_file(html_file, movie_table)

if len(tv_table) > 0:
    html_file.write('''
        <br>
        <p class="main center section_header">
            <a name="tv">TV</a>''')
    if len(movie_table) + len(other_table) > 0:
        html_file.write('''
            <br>
            <span class="navigation_options">''')
        if len(movie_table) > 0:
            html_file.write('''
                <a href="#movies">Movies</a>''')
        if len(other_table) > 0:
            if len(movie_table) > 0:
                html_file.write(' &middot; ')
            html_file.write('''
                <a href="#other">Other</a>''')
        html_file.write('''
            </span>''')
    html_file.write('''
        </p>''')
    write_table_to_file(html_file, tv_table)

if len(other_table) > 0:
    html_file.write('''
        <br>
        <p class="main center section_header">
            <a name="other">Other/Unknown</a>''')
    if len(movie_table) + len(tv_table)> 0:
        html_file.write('''
            <br>
            <span class="navigation_options">''')
        if len(movie_table) > 0:
            html_file.write('''
                <a href="#movies">Movies</a>''')
        if len(tv_table) > 0:
            if len(movie_table) > 0:
                html_file.write(' &middot; ')
            html_file.write('''
                <a href="#tv">TV</a>''')
        html_file.write('''
            </span>''')
    html_file.write('''
        </p>''')
    write_table_to_file(html_file, other_table)

html_file.write('''
        <br>
        <p class="main center fine_print">Last updated <span id="modification_timestamp"></span></p>
        <script type="text/javascript">
            setTimeSinceModification()
        </script>
    </body>
</html>''')

html_file.close()

print 'HTML file successfully built, exiting.'