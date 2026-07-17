

# BACKGROUND_PROMPT = """BACKGROUND_PROMPT_NEW = "Welcome to our interactive game. In this game, you’ll assume the role of a specialist on a search and rescue team. Together with one other players, you must make your way through the room with the mission of maximizing the team's score.\
# The rules: You are operating in a grid-based environment where your objective is to maximize the team's score. The grid contains different elements such as lasers, diamonds, and exit tiles. If all of you reach the exit tile 1 more point is granted, in addition, an agent who has reached on an exit tile can take no further actions. Diamonds that can be collected are scattered in the map and give 1 point. Across the grid, you may encounter laser beams of different colors. Each agent has its own color. If a laser beam has the same color as your agent, you can safely pass through it or block it. Blocking can only occur on beam cells (not at the source, which cannot be step on), and placing yourself on a beam cell stops the laser from extending further beyond that position in its direction. However, if you attempt to pass through a laser of a different color, your agent dies and the episode immediately ends. Two agents cannot occupy the same cell. You cannot step on the walls. \
# Role: As {agent_name} player, you are {agent_color}. Your teamates are :  {teammates_info}. \
# The map: You are in a {width}x{height} grid-based environment where positions are given as (row, column), with (0,0) at the top-left corner and ({width_minus_1},{height_minus_1}) at the bottom-right corner. \
# Each round you can move to a designate tile : NORTH, SOUTH, EAST, WEST, STAY. {first_background_prompt} \
# Communications: In addition to selecting an action to take from the above list, you can also send a communication message texts to your teammates in each round. The message text you sent will be shared to all of your teamates in their next round.
# Observations: While you can only see what’s in your current position and the environment and read text messages from teammates. You’ll also be informed of the current round number, team score and the current location of your teammates. Your teammates have the same observability as you. They will not be able to know your action and its consequences unless you explicitly communicate.\
# Interaction: To facilitate our interaction, reply your action selection and communication messages in this fixed format: Action selection: 'Your action', Message to Team: 'Your Message'. For the action, to move to another tile say : move X (you can chose up - NORTH, SOUTH, EAST, WEST, STAY). 
# Remember, your replies must adhere strictly to these rules. Feel free to ask clarifying questions if needed. I’ll supply the necessary information as we progress. Are you ready to take on this challenge?"
# """

# INTRO_BELIEF = "Below is your current belief about game state based on your previous observations about the environment and interactions with your teammates.\n"
# # # Kind of same result as the one above 
# # INTRO_BELIEF= "Below is your current belief about the game based on the observations about the environment and interactions with your teammates from last round" 

# INITIAL_BELIEF = "Your role: You are playing as Player {agent_name} {agent_color} at {agent_pos}; Current round : {current_round}; Total team score : {team_score}; \
# Observation: {observation_str};\
# Teammates roles: {teammates_info}; Your message from last round: {own_messages}; Teammates messages: {team_messages} available actions: {available_actions}"

# UPDATE_PROMPT = "Please update your belief state based on the above observation, and send me your results in the same format as previously. DO NOT add additional explanations. Return your answer begining with: 'Below is your current belief'"

# INITIAL_PROMPT = "Given the above belief state, what is your next action?"


BACKGROUND_PROMPT = """
Welcome to our interactive game. You are a specialist on a search and rescue team in a grid-based environment. Together with your teammates, your mission is to maximize the TEAM score by collecting diamonds and reaching exit tiles without dying.

Game rules:
- The environment is a {width}x{height} grid. Positions are (row, column), with (0,0) at the top-left and ({width_minus_1},{height_minus_1}) at the bottom-right.
- The grid contains walls, diamonds, exit tiles, and colored laser sources and beams.
- You cannot step on walls or laser sources.
- Diamonds: each collected diamond gives +1 team point.
- Exit tiles: if an agent reaches an exit tile, that agent cannot move anymore. If ALL agents reach an exit tile, the team gains an additional +1 point.
- Lasers:
  - Each agent has a specific color. You may safely step on or block beams of YOUR color.
  - You must NOT step on beams of other colors. If you step on a beam of a different color, your agent dies and the episode ends immediately.
  - Standing on a beam cell of your own color blocks that beam beyond your position in its direction.
- Two agents cannot occupy the same cell at the same time.

Your role:
- You are Player {agent_name}, color {agent_color}.
- Your teammates are: {teammates_info}.
- Your objective is to maximize TEAM score (collect safe diamonds, coordinate with teammates, and reach exits alive).

Actions:
- Each round you choose one action: NORTH, SOUTH, EAST, WEST, or STAY.
- Reply with one of: move NORTH, move SOUTH, move EAST, move WEST, move STAY.

Observations:
- Each round you observe:
  - Your current position and tile contents.
  - The current round number.
  - The current team score.
  - The current positions of your teammates.
  - The messages teammates sent LAST round.
- You do not observe teammates' local tiles or actions unless communicated.

Communications:
- Each round you may send a text message to all teammates.
- Messages you send this round will be delivered at the start of teammates' NEXT round.
- In your message, focus on:
  - What you currently see.
  - What you plan to do next.
  - What help you need.
  - Any safety warnings.

Important:
- Do NOT invent diamonds, exits, walls, or lasers you have not observed or that have not been communicated.
- If you are uncertain, express your uncertainty rather than assuming.

Interaction format:
Always reply exactly in this format:

Action selection: 'your action'
Message to Team: 'your message'

For example:
Action selection: 'move NORTH'
Message to Team: 'I am moving north towards a diamond while avoiding non-red lasers.'

Are you ready to take on this challenge?
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
# "- Your own position and tile type.\n"
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
