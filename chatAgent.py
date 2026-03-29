from lle import LLE, Agent
import time
import cv2
import re 
from ollama import Client 
import csv 
import sys
import os


BACKGROUND_PROMPT_NEW = "Welcome to our interactive game. In this game, you’ll assume the role of a specialist on a search and rescue team. Together with three other players, you must make your way through the room with the mission of reaching the exit together.\
The rules: You are operating in a grid-based environment where your objective is to maximize your team’s score. The grid contains different elements such as lasers, diamonds, and exit tiles. Your main goal is to reach an exit cell, which grants 1 points. If all of you reach the exit tile 1 more point is granted. Diamonds that can be collected are scattered in the map and give 1 point. Across the grid, you may encounter laser beams of different colors. Each agent has its own color. If a laser beam has the same color as your agent, you can safely pass through it or block it. However, if you attempt to pass through a laser of a different color, your agent dies and the episode immediately ends. \
Role: As {agent_name} player, you are {agent_color}.\
The map: You are in a 5x5 grid-based environment where positions are given as (row, column), with (0,0) at the bottom-left corner.\
Each round you can move to a designate tile :  NORTH, SOUTH, EAST, WEST, STAY.\
Communications:  In addition to selecting an action to take from the above list, you can also send communication message texts to both of your teammates in each round. The message text you sent will be shared to all of your teamates in their next round.\
Observations: While you can only see what’s in your current position and the environment and read text messages from teammates. You’ll also be informed of the current round number, team score and the current location of your teammates. Your teammates have the same observability as you. They will not be able to know your action and its consequences unless you explicitly communicate.\
Interaction: To facilitate our interaction, reply your action selection and communication messages in this fixed format: Action selection: 'Your action', Message to Team: 'Your Message'.  For the action, to move to another tile say : move X (you can chose up - NORTH, SOUTH, EAST, WEST, STAY). Remember, your replies must adhere strictly to these rules. Feel free to ask clarifying questions if needed. I’ll supply the necessary information as we progress. Are you ready to take on this challenge?"

INITIAL_BELIEF = "Below is your current belief about game state based on your previous observations about the environment and interactions with your teammates. \n \
Your role: You are playing as Player {agent_color} at {agent_pos}; Current round : {current_round}; Total team score : {team_score}; \
Observation: laser beam yellow at (2,0) and projects a beam horizontally across the entire row 2. diamond at (4,0). Exit tile at (4,3) and (4,4);\
Team roles: {team_name} {team_color}; Teamate location:{team_location}; Teammates messages: {team_messages} available actions: {available_actions}"

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
    1: "yellow",
    2: "blue",
    3: "green"
}

AGENT_NAME_MAP = {
    0: "Alpha",
    1: "Omega",
    2: "Sigma",
    3: "Delta"
}

class ChatAgent(): 

  def __init__(self, agent_id, agents_pos, available_actions):

    self.agent_id = agent_id
    self.agent_color = COLOR_MAP[agent_id]
    self.agent_pos = agents_pos[agent_id]

    self.available_actions = available_actions
    #Team mate pos is the other index in angents_pos (for the moment the len will only be of 2)
    self.current_round = 0
    self.team_score = 0

    self.team_color = COLOR_MAP[1 - agent_id]  #TODO for when there'll be more agents
    self.team_mate_pos = agents_pos[1 - agent_id] #TODO for when there'll be more agents 
    self.team_names = AGENT_NAME_MAP[1 - agent_id] #TODO for when there'll be more agents
    self.team_messages = ""


    self.background_prompt = BACKGROUND_PROMPT_NEW.format(agent_name=AGENT_NAME_MAP[agent_id], agent_color=self.agent_color)

    self.last_belief = INITIAL_BELIEF.format(
        agent_id=self.agent_id,
        agent_color=self.agent_color,
        agent_pos=self.agent_pos,
        current_round=self.current_round,
        team_score=self.team_score,
        team_color=self.team_color,
        team_name=self.team_names,
        team_location=self.team_mate_pos,
        team_messages=self.team_messages,
        available_actions=self.available_actions
    )

  def parse_action(self, action_str): 
      """
      Example input: "move EAST"
      """
      # Search for any valid action word
      for action in ACTION_MAP.keys():
          if re.search(rf"\b{action}\b", action_str):
              return ACTION_MAP[action]

      # If no valid action is found, print an error message and exit
      print(f"Error: Invalid action '{action}'. Valid actions are: {', '.join(ACTION_MAP.keys())}.")
      sys.exit(1)  


  def parse_agent_response(self, text):
    result = {"action": None, "message": None}
    
    # Extract action and message 
    action_match = re.search(r"Action selection:\s*([^,]+)", text)
    message_match = re.search(r"Message to Team:\s*(.+)", text)

    if action_match and message_match:
        result["action"] = self.parse_action(action_match.group(1))
        result["message"] = message_match.group(1)
    else :
        print("Error: Response format is incorrect. Expected format: Action selection: 'Your action', Message to Team: 'Your Message'.")
        sys.exit(1)
        
    return result


  def makeApiCall(self):

    client = Client()
    messages = [
      {
        'role': 'user',
        'content': self.background_prompt + "\n" + self.last_belief,
      },
    ]

    print("\n WHAT AGENT GETS: \n")
    print(self.background_prompt + "\n" + self.last_belief)

    message = ''
    for part in client.chat('kimi-k2.5:cloud', messages=messages, stream=True):
      message += part['message']['content']

    print("\n AGENT RAW RESPONSE: \n")
    print("agent", self.agent_id,"\n", "response:", message, "\n") #TODO remove this, just for testing

    parsed_message = self.parse_agent_response(message)

    return parsed_message 
  

  def update_history(self, current_round, team_score, agents_pos, team_messages, available_actions): 
    """
    Update parameters of  chatAgent after each round, which will be included in the belief state for the next round.
    """

    self.current_round = current_round
    self.team_score = team_score
    self.agent_pos = agents_pos[self.agent_id]
    self.team_mate_pos = agents_pos[1 - self.agent_id]
    self.team_messages = team_messages
    self.available_actions = available_actions

    last_belief = "Below is the belief state of your last round: " + self.last_belief  

    self.last_belief = last_belief + INITIAL_BELIEF.format(
        agent_id=self.agent_id,
        agent_color=self.agent_color,
        agent_pos=self.agent_pos,
        current_round=self.current_round,
        team_score=self.team_score,
        team_color=self.team_color,
        team_name=self.team_names,
        team_location=self.team_mate_pos,
        team_messages=self.team_messages,
        available_actions=self.available_actions
    )



class Environment():

  def __init__(self, env):
    """
    env = lle environment 
    """
    self.env = env 
    self.chat_agents = []
    self.agents_pos = env.world.agents_positions 
    self.history = [] # list of dict, each dict contains: agent_id, action, message

  def  set_chat_agents(self, agents): 
      for i in range(self.env.n_agents):
         chat_agent = ChatAgent(agents[i].num, self.agents_pos, self.str_action(self.env.available_actions(), i))
         self.chat_agents.append(chat_agent)

  def str_action(self, actions, agent_id):
    """Convert the list of available actions for an agent into a string format to be included in the belief state."""
    
    action_str = ""
    agent_action = []
    for j in range(len(actions[agent_id])):
        if actions[agent_id][j]:
            agent_action.append(list(ACTION_MAP.keys())[j])
    action_str += ", ".join(agent_action) 
    return action_str

  def save_history(self, data_path, record):
     """Append a single record to the history CSV file. Creates file with header if it doesn't exist."""
     file_exists = os.path.exists(data_path)
     
     with open(data_path, 'a', newline='') as csvfile:
        fieldnames = ['round','agent_id', 'action', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header only if file is new
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(record)

  def run_experiment(self): 
      
    done = False
    current_round = 0
    team_score = None #TODO 

    self.set_chat_agents(self.env.world.agents)

    while not done:
        time.sleep(0.5)
        self.env.render() 
        actions = []
        messages = []
        for i in range(self.env.n_agents):
          agent = self.chat_agents[i]
          response = agent.makeApiCall()

          actions.append(response["action"])
          messages.append(response["message"])

          agent.update_history(current_round, team_score, self.env.world.agents_positions, messages[-1], self.str_action(self.env.available_actions(),i)) 

          # Increment round and save the action and message to history
          current_round += 1
          record = {
              "round": current_round,
              "agent_id": AGENT_NAME_MAP[agent.agent_id],
              "action": ACTION_MAP_REVERSE[response["action"]],
              "message": response["message"]
          }

          # get key of ACTION_MAP by value of response["action"] example if it is 0, get "NORTH"
          for key, value in ACTION_MAP.items():
              if value == response["action"]:
                  record["action"] = key
                  break



          self.history.append(record)
          # Save to CSV
          self.save_history("history.csv", record)

        step = self.env.step(actions)

        #TODO if got diamond or exit, update the team score 

        self.env.render()            
        done = step.is_terminal 

      
    print("\n \n \n")
    print("ended")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
      



if __name__ == "__main__": 
  world = LLE.from_file("map.txt").obs_type("layered").build()
  env = Environment(world)
  env.run_experiment()