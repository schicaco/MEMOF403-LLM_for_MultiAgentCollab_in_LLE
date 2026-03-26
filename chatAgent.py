from lle import LLE
import time
import cv2
import re 


BACKGROUND_PROMPT_NEW = "Welcome to our interactive game. In this game, you’ll assume the role of a specialist on a search and rescue team. Together with three other players, you must make your way through the room with the mission of reaching the exit together.\
The rules: You are operating in a grid-based environment where your objective is to maximize your team’s score. The grid contains different elements such as lasers, diamonds, and exit tiles. Your main goal is to reach an exit cell, which grants 1 points. If all of you reach the exit tile 1 more point is granted. Diamonds that can be collected are scattered in the map and give 1 point. Across the grid, you may encounter laser beams of different colors. Each agent has its own color. If a laser beam has the same color as your agent, you can safely pass through it or block it. However, if you attempt to pass through a laser of a different color, your agent dies and the episode immediately ends.\
Role: As {agent_id} player, you are {agent_color}.\
The map: You are in a 5x5 grid-based environment where positions are given as (row, column), with (0,0) at the bottom-left corner.\
Each round you can move to a designate tile :  NORTH, SOUTH, EAST, WEST, STAY.\
Communications:  In addition to selecting an action to take from the above list, you can also send communication message texts to both of your teammates in each round. The message text you sent will be shared to all of your teamates in their next round.\
Observations: While you can only see what’s in your current position and the environment and read text messages from teammates. You’ll also be informed of the current round number, team score and the current location of your teammates. Your teammates have the same observability as you. They will not be able to know your action and its consequences unless you explicitly communicate.\
Interaction: To facilitate our interaction, reply your action selection and communication messages in this fixed format: Action selection: 'Your action', Message to Team: 'Your Message'.  For the action, to move to another tile say : move X (you can chose up - NORTH, SOUTH, EAST, WEST, STAY). Remember, your replies must adhere strictly to these rules. Feel free to ask clarifying questions if needed. I’ll supply the necessary information as we progress. Are you ready to take on this challenge?"


INITIAL_BELIEF = "Below is your current belief about game state based on your previous observations about the environment and interactions with your teammates.\
Your role: You are playing as Player {agent_color} at {agent_pos}; Current round : {current_round}; Total team score : {team_score}; Observation: laser beam yellow at (2,0) and projects a beam horizontally across the entire row 2. diamond at (4,0). Exit tile at (4,3) and (4,4); Roles: {team_name} {team_color}; Teamates location:{team_location}; Teammates messages: {team_messages} Avalaible: {avalaible_actions}"




class ChatAgent(): 
  def __init__(self, agent_id, agent_color, init_pos, team_mates):
    self.agent_id = agent_id
    self.agent_color = agent_color
    self.agent_pos = init_pos
    self.current_round = 0
    self.team_score = 0

    self.team_mates = team_mates

    BACKGROUND_PROMPT = BACKGROUND_PROMPT_NEW.format(agent_id=agent_id, agent_color=agent_color)
    self.last_belief = INITIAL_BELIEF.format(agent_id= agent_id, agent_color=agent_color, current_round=self.current_round, team_score=self.team_score,team_color="yellow", team_name="omega")

  def makeApiCall(self):
    pass 

  def update_history(self, text): 
    pass 


  def save(self, data_path):
    pass 


class Environment():

  def __init__(self, env):
    self.env = env 

  def parse_agent_response(response: str):
      """
      Parses the agent response string and returns action and message.

      Expected format:
      Action selection: "move X",
      Message to Team: "Your Message".
      """

      action_match = re.search(r'Action selection:\s*"(.*?)"', response)
      message_match = re.search(r'Message to Team:\s*"(.*?)"', response)

      action = action_match.group(1) if action_match else None
      message = message_match.group(1) if message_match else None

      return {
          "action": action,
          "message": message
      }
  
  def run_experiment(self): 
      
      done = False       
      while not done:
        # self.env.render() # Uncomment to render
        time.sleep(0.2)

        actions = self.env.sample_action()
        step = self.env.step(actions)


        # self.env.render() # Uncomment to render    
        
        done = step.is_terminal # Either done or truncated

      
      print("\n \n \n")
      cv2.waitKey(0)
      cv2.destroyAllWindows()
      







def main():
  world = LLE.from_file("map.txt").obs_type("layered").build()
  env = Environment(world)

  env.run_experiment()
  


 
  
  


if __name__ == "__main__": 
  pass 


# while not done:
#     env.render() # Uncomment to render
#     time.sleep(0.2)

#     actions = env.sample_action()
#     step = env.step(actions)

#     print(actions)
#     # Access the step data with `step.obs`, `step.reward`, ...
#     env.render() # Uncomment to render    
    
#     done = step.is_terminal # Either done or truncated
