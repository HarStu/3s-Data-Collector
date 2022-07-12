--[[
	testing lua scripting capabilities 

	NOTES:
		emu.framecount() persists even through resets
		the ingame frame_number does not 

	TODOS:
		file out
			write to file in JSON format
		additional data to capture
			(more to come)
		verification
			it can't be assumed that registerafter is only called once per frame, so make sure that the frame_number value is unique before adding the data to the output
]]

-- if there's issues, try adding dkjson.lua to /fbneo/lua
local json = require ("libs/dkjson")

-- important memory addresses
p1_base = 0x02068C6C
p2_base = 0x02069104
frame_number = 0x2007F00 --dword
match_state = 0x020154A7 --byte

-- important memory offsets
-- add these to the base addresses to get the relevant value for each player
life_offset = 0x9F --byte

-- setup the output files
output_txt = io.open("../data/log.txt", "w")
output_json = io.open("../data/log.json", "w")

-- output table
output_table = {}

-- runs when emulation starts, or is reset
function on_start() 
	output_txt:write("\nemulation started!\n\n")
end

-- runs when the lua is stopped
-- note that this isn't properly occur if the window is closed early!
function on_exit()
	output_table_json_string = json.encode(output_table, {indent = true})
	output_json:write(output_table_json_string)

	output_txt:write("just a quick test that on_exit is being entered")
	output_txt:close()
	output_json:close()
end

-- runs every frame (currently at the end)
function per_frame()

	-- capture information about the game
	ingame_frame = memory.readdword(frame_number)
	emu_frame = emu.framecount()

	p1_life = memory.readbyte(p1_base + life_offset)
	p2_life = memory.readbyte(p2_base + life_offset)

	in_match = nil 
	if memory.readbyte(match_state) == 0x02 then
		in_match = "yes"
	else
		in_match = "no"
	end

	-- write captured information to output_txt
	output_txt:write("ingame frame: " .. tostring(ingame_frame) .. "\n")
	output_txt:write("emu frame: " .. tostring(emu_frame) .. "\n")
	output_txt:write("p1 life: " .. tostring(p1_life) .. "\n")
	output_txt:write("p2 life: " .. tostring(p2_life) .. "\n")
	output_txt:write("in match?: " .. tostring(in_match) .. "\n")
	output_txt:write("\n")

	-- write captured information to a frame table
	frame = {}
	frame["p1 life"] = p1_life
	frame["p2 life"] = p2_life
	frame["ingame frame"] = ingame_frame
	frame["in match"] = in_match
	
	-- add the frame table to the output table
	-- since the emu framecount is persistent across resets, it will serve as the key 
	output_table[emu_frame] = frame
end

emu.registerstart(on_start)
emu.registerexit(on_exit)
emu.registerafter(per_frame)