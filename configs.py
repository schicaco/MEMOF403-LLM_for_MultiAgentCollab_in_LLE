BACKGROUND_PROMPT = """
You are Player {agent_name} (color {agent_color}) on a search-and-rescue team in a {width}x{height} grid. Positions are (row, column); (0,0) is top-left, ({width_minus_1},{height_minus_1}) bottom-right. Teammates: {teammates_info}.

Goal: maximize the TEAM score.
- Each diamond collected: +1.
- Exit tiles: an agent that reaches one stops moving. If ALL agents reach an exit, +1 for the team.

Rules:
- Walls and laser sources are impassable. Two agents cannot share a cell.
- You may safely step on beams of your own color; standing on one blocks it beyond you.
- Stepping on a beam of another color kills you and ends the episode for everyone.
- An agent cannot move when he reach an exit tile. 

Each round you see: your position and tile, the round number, the team score, teammates' positions, and the messages they sent last round. You do not see their local tiles or actions unless they tell you.

Reply with one action: move NORTH, move SOUTH, move EAST, move WEST, or move STAY. You may also send a message to all teammates, delivered at the start of their next round. Use it for what you see, your plan, help you need, and safety warnings.
Only state what you have observed or been told; if unsure, say so. Do not invent diamonds, exits, walls or lasers. {first_background_prompt}. 

Reply exactly in this format:
Action selection: 'move NORTH'
Message to Team: 'Moving north toward a diamond; avoiding non-red lasers.'


"""

INTRO_BELIEF = "Below is your current belief about the game based on the observations and teammate interactions from the LAST round.\n"

INITIAL_BELIEF = ("Your role: You are Player {agent_name}, color {agent_color}, currently at position {agent_pos}. "
                  "Current round: {current_round}. Total team score: {team_score}. "
                  "Your current observation (this round): {observation_str}. "
                  "Teammates: {teammates_info}. "
                  "Your own message from last round: {own_messages}. "
                  "Teammate messages received from last round: {team_messages}. "
                  "Available actions: {available_actions}.")

UPDATE_PROMPT = (
"Below are the interactions from last round: "
"Your own message from last round: {own_messages}. "
"Teammate messages received from last round: {team_messages}. "
"Please update your belief state based on the information above. "
"Represent your belief concisely, covering at least:\n"
"- Your role, color and position "
"- Known positions of diamonds, exits, walls, and lasers.\n"
"- Known or inferred positions and roles of teammates.\n"
"- Any important plans or intentions (yours and teammates') for the next few rounds.\n"
"Begin your answer EXACTLY with: 'Below is your current belief' followed by Action selection: 'your action' Message to Team: 'your message'  "
"Do NOT add extra explanations outside the belief description."
)

INITIAL_PROMPT = "Given the above belief state, what is your next action?"


ACTION_MAP = {
    "NORTH": 0,
    "SOUTH": 1,
    "EAST": 2,
    "WEST": 3,
    "STAY": 4
}


ACTION_MAP_REVERSE ={
    0: "NORTH",
    1: "SOUTH",
    2: "EAST",
    3: "WEST",
    4: "STAY"
}


COLOR_MAP = {
    0: "red",
    1: "blue",
    2: "yellow",
    3: "green"
}

AGENT_NAME_MAP = {
    0: "Alpha",
    1: "Omega",
    2: "Sigma",
    3: "Delta"
}
