--[[
	testing lua scripting capabilities 

	TODOS:
		file out
			write to file rather than command line
			write to file in JSON format
		additional data
			ingame timer
			p1 health
			p2 health
			(more to come)
		verification
			it can't be assumed that registerafter is only called once per frame
			so make sure that the frame_number value is unique before adding the data to the output


]]

-- file must be present in /fbneo/lua
local json = require ("dkjson")

-- important memory addresses
p1_base = 0x02068C6C
p2_base = 0x02069104
frame_number = 0x2007F00 --dword


-- verify that the script has started
emu.print("hello world")

-- setup the output file
output_file = io.open("../data/log.txt", "w")


function on_start() 
	output_file:write("script started!\n\n")
end

function on_exit()
	print("all done!")
	output_file:close()
end

function per_frame()
	emu_frame = emu.framecount()
	ingame_frame = memory.readdword(frame_number)

	output_file:write("INGAME FRAME: " .. tostring(ingame_frame) .. "\n")
	output_file:write("\n")

end

emu.registerstart(on_start)
emu.registerexit(on_exit)
emu.registerafter(per_frame)