--[[
	Lua script tasked with capturing a game-state json from a single frame
]]

require("libs/dkjson")

frame = {}
frame.p1 = {}
frame.p2 = {}


while emu.frameadvance() do
	frame.p1.health = 
	--frame.p2.health = 
	--frame.p1.meter =
	--frame.p2.meter = 
	--frame.p1.gauge = 
	--frame.p2.gauge = 
	--frame.p1.stun = 
	--frame.p2.stun = 
	--frame.clock = 






print(frame)
