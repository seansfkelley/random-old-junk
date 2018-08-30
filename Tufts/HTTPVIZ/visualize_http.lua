visualizer = assert (io.popen ("java -jar /home/ubuntu/HTTPVisualizer.jar", "w"))

-- this is going to be our tap
tap_http = nil

-- first we declare the tap called "http tap" with the filter it is going to use
tap_http = Listener.new(nil,"http")

-- this function will get called at the end(3) of the capture to print the summary
function tap_http.draw()
    -- debug("http packets:" .. http_packets)
end

-- this function is going to be called once each time the filter of the tap matches
function tap_http.packet(pinfo, tvb)
    --print(tostring(pinfo.number))
    visualizer:write(tostring(pinfo.src) .. ";" .. tostring(pinfo.dst) .. ";" .. tostring(tvb:range():bytes()) .. "\n")
	visualizer:flush()
end

