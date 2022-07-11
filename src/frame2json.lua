--[[
	Lua script tasked with capturing a game-state json from a single frame. 
	Strictly a test right now.

	player 1: located at 0x02068C6C
	player 2: located at 0x02069104
]]

-- file must be present in /fbneo/lua
local json = require ("dkjson")

-- verify that the script has started
emu.print("hello world")

-- return a single value from memory. eventually this will return a table of values
function take_snapshot()
	return memory.readdword(0x2007F00)
end

emu.print("here's the current frame_number value")
print(tostring(take_snapshot()))
emu.print("goodbye!\n")