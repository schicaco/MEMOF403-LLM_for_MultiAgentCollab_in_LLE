from lle import LLE, Agent
import time
import cv2
import re 
from ollama import Client 
import csv 
import sys


BACKGROUND_PROMPT_NEW = "Welcome to our interactive game. In this game, you’ll assume the role of a specialist on a search and rescue team. Together with three other players, you must make your way through the room with the mission of reaching the exit together.\
The rules: You are operating in a grid-based environment where your objective is to maximize your team’s score. The grid contains different elements such as lasers, diamonds, and exit tiles. Your main goal is to reach an exit cell, which grants 1 points. If all of you reach the exit tile 1 more point is granted. Diamonds that can be collected are scattered in the map and give 1 point. Across the grid, you may encounter laser beams of different colors. Each agent has its own color. If a laser beam has the same color as your agent, you can safely pass through it or block it. However, if you attempt to pass through a laser of a different color, your agent dies and the episode immediately ends. \
Role: As {agent_id} player, you are {agent_color}.\
The map: You are in a 5x5 grid-based environment where positions are given as (row, column), with (0,0) at the bottom-left corner.\
Each round you can move to a designate tile :  NORTH, SOUTH, EAST, WEST, STAY.\
Communications:  In addition to selecting an action to take from the above list, you can also send communication message texts to both of your teammates in each round. The message text you sent will be shared to all of your teamates in their next round.\
Observations: While you can only see what’s in your current position and the environment and read text messages from teammates. You’ll also be informed of the current round number, team score and the current location of your teammates. Your teammates have the same observability as you. They will not be able to know your action and its consequences unless you explicitly communicate.\
Interaction: To facilitate our interaction, reply your action selection and communication messages in this fixed format: Action selection: 'Your action', Message to Team: 'Your Message'.  For the action, to move to another tile say : move X (you can chose up - NORTH, SOUTH, EAST, WEST, STAY). Remember, your replies must adhere strictly to these rules. Feel free to ask clarifying questions if needed. I’ll supply the necessary information as we progress. Are you ready to take on this challenge?"

INITIAL_BELIEF = "Below is your current belief about game state based on your previous observations about the environment and interactions with your teammates. \n \
Your role: You are playing as Player {agent_color} at {agent_pos}; Current round : {current_round}; Total team score : {team_score}; \
Observation: laser beam yellow at (2,0) and projects a beam horizontally across the entire row 2. diamond at (4,0). Exit tile at (4,3) and (4,4);\
Roles: {team_name} {team_color}; Teamates location:{team_location}; Teammates messages: {team_messages} Avalaible: {avalaible_actions}"

INITIAL_PROMPT = "Given the above belief state, what is your next action?"

ACTION_MAP = {
    "NORTH": 0,
    "SOUTH": 1,
    "EAST": 2,
    "WEST": 3,
    "STAY": 4
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

  def __init__(self, agent_id, agents_pos, avalaible_actions):

    self.agent_id = agent_id
    self.agent_color = COLOR_MAP[agent_id]
    self.agent_pos = agents_pos
    print("agent_pos: ", self.agent_pos)

    self.avalaible_actions = avalaible_actions
    #Team mate pos is the other index in angents_pos (for the moment the len will only be of 2)
    self.current_round = 0
    self.team_score = 0

    self.team_mate_pos = agents_pos[1 - agent_id]  #TODO for when there'll be more agents 
    self.team_color = COLOR_MAP[1 - agent_id]  #TODO for when there'll be more agents
    self.team_names = "Omega" #TODO for when there'll be more agents
    self.team_messages = ""


    self.background_prompt = BACKGROUND_PROMPT_NEW.format(agent_id=agent_id, agent_color=self.agent_color)

    self.last_belief = INITIAL_BELIEF.format(agent_color=self.agent_color, agent_pos=self.agent_pos, current_round=self.current_round,\
                                            team_score=self.team_score , team_name = self.team_names, team_color=self.team_color, \
                                            team_location=self.team_mate_pos, team_messages=self.team_messages, avalaible_actions=self.avalaible_actions)
    

  def parse_action(self, action_str): 
      """
      Example input: "move EAST"
      """
      action_word = action_str.split()[-1].upper()
      #TODO: error is format not good 
      return ACTION_MAP[action_word]  


  def parse_agent_response(self, response: str):
      """
      Parses the agent response string and returns action and message.

      Expected format:
      Action selection: "move X",
      Message to Team: "Your Message".

      try except error if the format is not good which makes the program stop 
      """

      action_match = re.search(r'Action selection:\s*"(.*?)"', response)
      message_match = re.search(r'Message to Team:\s*"(.*?)"', response)

      action = action_match.group(1) if action_match else None
      message = message_match.group(1) if message_match else None

      try:
         if not action or not message:
            raise ValueError("Response format is incorrect. Expected format: Action selection: 'Your action', Message to Team: 'Your Message'.")
      except ValueError as e:
         print(e)
         sys.exit(1)

      return {
          "action": self.parse_action(action),
          "message": message
      }


  def makeApiCall(self):

    client = Client()
    messages = [
      {
        'role': 'user',
        'content': self.background_prompt + "\n" + self.last_belief,
      },
    ]

    print(self.background_prompt + "\n" + self.last_belief)

    message = ''
    # for part in client.chat('kimi-k2.5:cloud', messages=messages, stream=True):
    #   message += part['message']['content']

    print("agent", self.agent_id, "response:", message, "\n") #TODO remove this, just for testing

    parsed_message = self.parse_agent_response(message)

    return parsed_message 
  

  def update_history(self, current_round, team_score, agents_pos, team_messages, avalaible_actions): 
    # TODO code moche 
    
    self.current_round = current_round
    self.team_score = team_score
    self.team_mate_pos = agents_pos[1 - self.agent_id]
    self.last_belief = INITIAL_BELIEF.format(agent_id= self.agent_id, agent_color=self.agent_color, current_round=self.current_round, team_score=self.team_score,team_color=self.team_color , team_name = self.team_names, team_location=self.team_mate_pos, team_messages=team_messages, avalaible_actions=avalaible_actions)



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
         chat_agent = ChatAgent(agents[i].num, self.agents_pos[i], self.str_action(self.env.available_actions(), i))
         self.chat_agents.append(chat_agent)

  def str_action(self, actions, agent_id):
    """return string of avalaible action for agent i (givent the agent id) in the format of 'WEST, SOUTH'
      if there is 2 agent the format is for example [[False  True False  True  True]
      [False  True  True False  True]]"""
    
    action_str = ""
    agent_action = []
    for j in range(len(actions[agent_id])):
        if actions[agent_id][j]:
            agent_action.append(list(ACTION_MAP.keys())[j])
    action_str += ", ".join(agent_action) 
    return action_str


  def save_history(self, data_path, history):
     """Save the hisory (self.history) to a csv file in the data_path location. 
     The csv file should have columns: round, agent_id, action, message"""

     with open(data_path, 'w', newline='') as csvfile:
        fieldnames = ['agent_id', 'action', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        # for record in self.history:
        #     writer.writerow(record)
        writer.writerows(history)

  def run_experiment(self): 
      
    done = False
    current_round = 0
    team_score = None #TODO 

    self.set_chat_agents(self.env.world.agents)
    while not done:
        # env.render() # Uncomment to render
        actions = []
        messages = []
        for i in range(self.env.n_agents):
          agent = self.chat_agents[i]
          response = agent.makeApiCall()

          actions.append(response["action"])
          messages.append(response["message"])

          agent.update_history(current_round, team_score, self.env.world.agents_positions, messages[-1], self.env.avalaible_actions[i]) 

          # Save the action and message to history
          self.history.append({
              "round": current_round,
              "agent_id": agent.agent_id,
              "action": response["action"],  
              "message": response["message"]
          })

        step = self.env.step(actions)

        #TODO if got diamond or exit, update the team score 
        
        # Access the step data with `step.obs`, `step.reward`, ...
        self.env.render() # Uncomment to render    
        
        done = step.is_terminal # Either done or truncated

        current_round += 1

        if current_round == 2: done = True #TODO remove this, just for testing

    self.save_history("history.csv", self.history) 
      
    print("\n \n \n")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
      



if __name__ == "__main__": 
  world = LLE.from_file("map.txt").obs_type("layered").build()
  env = Environment(world)
  env.run_experiment()