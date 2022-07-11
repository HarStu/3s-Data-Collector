--[[
	Lua script tasked with capturing a game-state json from a single frame. 
	Strictly a test right now.

	player 1: located at 0x02068C6C
	player 2: located at 0x02069104
]]

json = require ("./lua-libs/dkjson")

p1_location = 0x02068C6C

game_data = {}

-- collect a snapshot of game data and return it as a table
function take_snapshot()
	return {
		frame_number = memory.readdword(0x2007F00),
		p1_posture = memory.readbyte(p1_location + 0x20E)
	}
end

-- every frame, take a snapshot, convert it to a json, and output such. 
while emu.frameadvance() do
	table_frame = take_snapshot
	json_frame = json.encode(frame, {indent = true})
	print(json_frame)
end

print(frame)