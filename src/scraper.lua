--[[
	testing lua scripting capabilities 

	NOTES:
		emu.framecount() persists even through resets
		the ingame frame_number does not 

	TODOS:
		find a reliable way to end the lua when the replay is complete
			necessary so that we can use the on_exit function to encode and output the json file
		file output
			create a hierarchical {replay {game {round {frame}}}} format for the json output
		additional data to capture
			capture additional values each frame, as well as values which are relevant on a replay/round/game level
		verification
			it can't be assumed that registerafter is only called once per frame, so make sure that the frame_number value is unique before adding the data to the output
			this is also relevant for updating replay_frame_count
		compartmentalize parts of per_frame()
			create a get_frame_table function which returns a frame_table
			create a print_frame_table function which outputs the contents of a frame table to the gui
			create a function for adding frame_table to output.txt
			create a functino for adding frame_table to output.json
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

-- set up working json (fightcade api information about the replay being scraped)
json_tempfile = io.input("../data/.working.json"):read('*a')
working_json = json.decode(tostring(json_tempfile))

-- setup the output files
output_txt = io.open("../data/log.txt", "w")
output_json = io.open("../data/log.json", "w")

-- replay frame count
-- emulator and ingame frame counts don't start at 0, but this will
replay_frame = 0

-- startpoint for the emu framecount
initial_emu_framecount = 0

-- first startup flag; used to make sure certain operations will only execute the first time on_start() is called
first_startup = true

-- projected duration of the replay in frames
duration_in_frames = working_json["duration"] * 60

-- output table
output_table = {}


-- runs when emulation starts, or is reset
function on_start() 
	output_txt:write("emulation started!\n")

	-- only execute these operations during the initial startup
	if first_startup == true then
		output_txt:write("Initial emu frame: " .. emu.framecount() .. "\n\n")
		initial_emu_framecount = emu.framecount()
		first_startup = false
	end
end


-- runs when the lua script ends
-- note that this doesn't run if the window is closed before the lua ends
function on_exit()
	-- encode the table of frame tables to a string
	-- write that string as a json files
	output_table_json_string = json.encode(output_table, {indent = true})
	output_json:write(output_table_json_string)

	-- close the output files being worked on
	output_txt:close()
	output_json:close()
end


-- runs every frame (currently registered to run at the end of the frame, before the inputs for the next frame are grabbed)
function per_frame()
	frame = get_frame_table()

	-- update gui
	gui.text(30, 30, "PROJECTED REPLAY DURATION: " .. duration_in_frames)
	gui.text(30, 40, "     CURRENT REPLAY FRAME: " .. tostring(frame["replay frame"]))
	gui.text(30, 60, "                IN MATCH?: " .. frame["in match"])
	gui.text(30, 70, "                  P1 LIFE: " .. tostring(frame["p1 life"]))
	gui.text(30, 80, "                  P2 LIFE: " .. tostring(frame["p2 life"]))

	-- write scraped frame information to output_txt
	output_txt:write("ingame frame: " .. tostring(frame["ingame frame"]) .. "\n")
	output_txt:write("emu frame: " .. tostring(frame["emu frame"]) .. "\n")
	output_txt:write("p1 life: " .. tostring(frame["p1 life"]) .. "\n")
	output_txt:write("p2 life: " .. tostring(frame["p2 life"]) .. "\n")
	output_txt:write("in match?: " .. frame["in match"] .. "\n")
	output_txt:write("\n")

	-- add frame as a entry on output table
	-- since the replay frame is persistent across resets, it will serve as the key 
	output_table[frame["replay frame"]] = frame
end


-- returns a table with information about the current frame
function get_frame_table()
	frame_table = {}

	-- scrape information about the frame
	ingame_frame = memory.readdword(frame_number)
	p1_life = memory.readbyte(p1_base + life_offset)
	p2_life = memory.readbyte(p2_base + life_offset)

	in_match = nil 
	if memory.readbyte(match_state) == 0x02 then
		in_match = "yes"
	else
		in_match = "no"
	end

	-- calculate replay frame
	replay_frame = emu.framecount() - initial_emu_framecount

	-- add values to frame_table
	frame_table["p1 life"] = p1_life
	frame_table["p2 life"] = p2_life
	frame_table["ingame frame"] = ingame_frame
	frame_table["in match"] = in_match
	frame_table["replay frame"] = replay_frame

	return frame_table
end

emu.registerstart(on_start)
emu.registerexit(on_exit)
emu.registerafter(per_frame)