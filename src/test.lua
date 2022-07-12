--[[
	testing lua scripting capabilities 

	TODOS:
		file out
			write to file in JSON format
		additional data to capture
			(more to come)
		verification
			it can't be assumed that registerafter is only called once per frame, so make sure that the frame_number value is unique before adding the data to the output
]]

-- file must be present in /fbneo/lua
local json = require ("dkjson")

-- important memory addresses
p1_base = 0x02068C6C
p2_base = 0x02069104
frame_number = 0x2007F00 --dword

-- important memory offsets
-- add these to the base addresses to get the relevant value for each player
life_offset = 0x9F --byte

-- setup the output file
output_file = io.open("../data/log.txt", "w")


function on_start() 
	output_file:write("script started!\n\n")
end

function on_exit()
	output_file:close()
end

function per_frame()

	-- capture information about the game
	ingame_frame = memory.readdword(frame_number)
	p1_life = memory.readbyte(p1_base + life_offset)
	p2_life = memory.readbyte(p2_base + life_offset)

	output_file:write("FRAME: " .. tostring(ingame_frame) .. "\n")
	output_file:write("p1 life: " .. tostring(p1_life) .. "\n")
	output_file:write("p2 life: " .. tostring(p2_life) .. "\n")
	output_file:write("\n")
end

emu.registerstart(on_start)
emu.registerexit(on_exit)
emu.registerafter(per_frame)