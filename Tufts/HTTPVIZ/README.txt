This version of the code is an earlier revision from before image thumbnails were implemented. The newest version
is exceptionally unstable and generally unreliable. This version is able to see the image data, but it does not
extract it and display it to the user.

I included the source code for examination purposes, but when running use the included jar rather that recompiling
the included code into a jar. It includes required libraries that I did not include the source for (the prefuse
library -- you can download it yourself, but there's not much point).

Before running Wireshark with the script, modify the content of the script so that the first line refers to the
absolute path of the included jar. Also locate the init.lua script in the Wireshark directory (usually
/usr/share/wireshark) and do the following:

comment out the line 'disable_lua = true; do return end;' to enable Lua
set 'run_user_scripts_when_superuser = true' on a line soon after the above line to let Wireshark run non-init Lua
    scripts
"comment out" the 'if running_superuser then' block by replacing it with 'if false then' to allow the scripts to
    do things generally considered harmful (in this case, allow them to spawn other processes)

After making these changes, run Wireshark with the -X lua_script:<location of the script>

An empty visualization window should appear; running Wireshark on a live network or a packet capture with HTTP
data will cause the list in the visualization to be populated and updated. The functionality of the visualizer
is quite sparse since it's only intended as a proof of concept.