# Prompts 

Welcome to our interactive game. In this game, you’ll assume the role of a specialist on a search and rescue team.
Together with three other players, you must make your way through the room with the mission of reaching the exit together. 

**The rules**: 
You are operating in a grid-based environment where your objective is to maximize your team’s score. The grid contains different elements such as lasers, diamonds, and exit tiles.

Your main goal is to reach an exit cell, which grants 1 points. If all of you reach the exit tile 1 more point is granted. Diamonds that can be collected are scattered in the map and give 1 point. 

Across the grid, you may encounter laser beams of different colors. Each agent has its own color. If a laser beam has the same color as your agent, you can safely pass through it or block it. However, if you attempt to pass through a laser of a different color, your agent dies and the episode immediately ends.

**Role:**
As Delta player, you are red
Player Omega is yellow

**The map**: 
You are in a 5×5 grid-based environment where positions are given as (row, column), with (0,0) at the bottom-left corner. A laser beam yellow is located at cell (2,0) and projects a beam horizontally across the entire row 2. A diamond is located at (4,0). You start at position (0,2) and player Omega starts at (0,3) , and your goal is to reach the exit at (4,3). Plan your path carefully to maximize your score while avoiding the laser.

**Actions**: 
Each round you can move to a designate tile :  NORTH, SOUTH, EAST, WEST, STAY.

**Communications**: 
In addition to selecting an action to take from the above list, you can also
send communication message texts to both of your teammates in each round. The message text you sent will be shared to all of your teamates in their next round.

**Observations**: 
While you can only see what’s in your current position and the environment and read text messages from teammates. You’ll also be informed of the current round number, team score and the current location of your teammates. Your teammates have the same observability as you. They will not be able to know your action and its consequences unless you explicitly communicate.

**Interaction**: 
To facilitate our interaction, reply your action selection and communication messages in this fixed format:
Action selection: "Your action".  
Message to Team: “Your Message”. 

For the action, to move to another tile say : move X (you can chose up - ORTH, SOUTH, EAST, WEST, STAY)

Remember, your replies must adhere strictly to these rules. Feel free to ask clarifying questions if needed. I’ll supply the necessary information as we progress. Are you ready to take on this explosive challenge?

## Inital belief state

Below is your current belief about game state based
on your previous observations about the environ-
ment and interactions with your teammates. 

Your role: You are playing as Player *agent color* + *give tile postition*
Current round : 1
Total team score : 0 
Observation: *in progress... give all position of lasers color and position of diamonds*
Teamates location: Omega (0,3)
Roles: 
*Player Omega is yellow*

Avalaible action options: *avalaible_actions* 