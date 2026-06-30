
# Same prompt as the background prompt but saying since it is the first round that the agent needs to stay in its current position to coordinate with the other agent.
FIRST_ROUND_BACKGROUND_PROMPT_NEW = "Welcome to our interactive game. In this game, you’ll assume the role of a specialist on a search and rescue team. Together with one other players, you must make your way through the room with the mission of reaching the exit together.\
The rules: You are operating in a grid-based environment where your objective is to reach an exit tile. The grid contains different elements such as lasers, diamonds, and exit tiles.  If all of you reach the exit tile 1 more point is granted. Diamonds that can be collected are scattered in the map and give 1 point. Across the grid, you may encounter laser beams of different colors. Each agent has its own color. If a laser beam has the same color as your agent, you can safely pass through it or block it. Blocking can only occur on beam cells (not at the source), and placing yourself on a beam cell stops the laser from extending further beyond that position in its direction. However, if you attempt to pass through a laser of a different color, your agent dies and the episode immediately ends. Two agents cannot occupy the same cell.\
Role: As {agent_name} player, you are {agent_color}.  Your teamate name is {team_names} and is {team_color} \
The map: You are in a 5x5 grid-based environment where positions are given as (row, column), with (0,0) at the top-left corner and (4,4) at the bottom-right corner. \
Each round you can move to a designate tile : NORTH, SOUTH, EAST, WEST, STAY. Since this is the round 0, you must remain in your current position to ensure coordination with your other teammates. \
Communications: In addition to selecting an action to take from the above list, you can also send communication message texts to both of your teammates in each round. The message text you sent will be shared to all of your teamates in their next round.\
Observations: While you can only see what’s in your current position and the environment and read text messages from teammates. You’ll also be informed of the current round number, team score and the current location of your teammates. Your teammates have the same observability as you. They will not be able to know your action and its consequences unless you explicitly communicate.\
Interaction: To facilitate our interaction, reply your action selection and communication messages in this fixed format: Action selection: 'Your action', Message to Team: 'Your Message'. For the action, to move to another tile say : move X (you can chose up - NORTH, SOUTH, EAST, WEST, STAY). Remember, your replies must adhere strictly to these rules. Feel free to ask clarifying questions if needed. I’ll supply the necessary information as we progress. Are you ready to take on this challenge?"

# Goal: "Your main goal is to reach an exit cell"
BACKGROUND_PROMPT_NEW = "Welcome to our interactive game. In this game, you’ll assume the role of a specialist on a search and rescue team. Together with one other players, you must make your way through the room with the mission of reaching the exit together.\
The rules: You are operating in a grid-based environment where your objective is to reach an exit tile. The grid contains different elements such as lasers, diamonds, and exit tiles.  If all of you reach the exit tile 1 more point is granted. Diamonds that can be collected are scattered in the map and give 1 point. Across the grid, you may encounter laser beams of different colors. Each agent has its own color. If a laser beam has the same color as your agent, you can safely pass through it or block it. Blocking can only occur on beam cells (not at the source), and placing yourself on a beam cell stops the laser from extending further beyond that position in its direction. However, if you attempt to pass through a laser of a different color, your agent dies and the episode immediately ends. Two agents cannot occupy the same cell.\
Role: As {agent_name} player, you are {agent_color}.  Your teamate name is {team_names} and is {team_color} \
The map: You are in a 5x5 grid-based environment where positions are given as (row, column), with (0,0) at the top-left corner and (4,4) at the bottom-right corner. \
Each round you can move to a designate tile : NORTH, SOUTH, EAST, WEST, STAY.\
Communications: In addition to selecting an action to take from the above list, you can also send communication message texts to both of your teammates in each round. The message text you sent will be shared to all of your teamates in their next round.\
Observations: While you can only see what’s in your current position and the environment and read text messages from teammates. You’ll also be informed of the current round number, team score and the current location of your teammates. Your teammates have the same observability as you. They will not be able to know your action and its consequences unless you explicitly communicate.\
Interaction: To facilitate our interaction, reply your action selection and communication messages in this fixed format: Action selection: 'Your action', Message to Team: 'Your Message'. For the action, to move to another tile say : move X (you can chose up - NORTH, SOUTH, EAST, WEST, STAY). Remember, your replies must adhere strictly to these rules. Feel free to ask clarifying questions if needed. I’ll supply the necessary information as we progress. Are you ready to take on this challenge?"


INITIAL_BELIEF = "Your role: You are playing as Player {agent_color} at {agent_pos}; Current round : {current_round}; Total team score : {team_score}; \
Observation: laser beam red at (2,0) and projects a beam horizontally across the entire row 2. diamond at (4,0). Exit tile at (4,3) and (4,4);\
Team roles: {team_name} {team_color}; Teamate location:{team_location}; Your message from last round: {own_messages}; Teammates messages: {team_messages} available actions: {available_actions}"
#TODO add possibility to change info of obsevation so it will always match the map given 

INITIAL_PROMPT = "Given the above belief state, what is your next action?"

INTRO_BELIEF = "Below is your current belief about game state based on your previous observations about the environment and interactions with your teammates.\n"

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

# TODO there was an lle upgrade ! check the id colors 
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
