scp skelle02@linux.cs.tufts.edu:gctest/gc-debug-info gc-debug-info.txt && python extract\ class\ info.py gc-debug-info.txt > gc-debug-info-parsed.txt &
scp skelle02@linux.cs.tufts.edu:gctest/heapdump . && python convert_heap.py heapdump && cp heapdump.xml ~/Documents/Programming/Heapviz/heapviz/data/
