--[[
	testing lua scripting capabilities 
]]

-- file must be present in /fbneo/lua
local json = require ("dkjson")


-- important memory addresses
p1_base = 0x02068C6C
p2_base = 0x02069104
frame_number = 0x2007F00 --dword

-- verify that the script has started
emu.print("hello world")

function get_frame_number()
	return memory.readdword(frame_number)
end

-- return a single value from memory. eventually this will return a table of values
function snapshot()
	-- confirm the frame_number value first. 
	start_snapshot_frame_number = memory.readdword(frame_number)
end

-- function to test emulator pausing capability
-- currently, calling this (even with the pause/unpause commented out!) crashes the emulator
function pause_and_unpause()
	emu.print("entered into the pause and unpause function")
	current_frame = get_frame_number()
	unpause_frame = current_frame + 60
	emu.print("starting on frame " .. tostring(current_frame) .. "and ending on frame " .. tostring(unpause_frame))
	-- emu.pause()
	while current_frame < unpause_frame do
		current_frame = get_frame_number()
		emu.print("the current frame is")
		emu.print(tostring(current_frame))
		emu.print("\n")
	end 
	-- emu.unpause()
end