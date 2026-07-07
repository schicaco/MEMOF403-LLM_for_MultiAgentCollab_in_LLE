from lle import LLE
import time
import cv2
import sys
import os 
import csv 

from ChatAgent import ChatAgent
from configs import ACTION_MAP, ACTION_MAP_REVERSE, AGENT_NAME_MAP


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
        
        print("Record:", record)

        with open(data_path, 'a', newline='') as csvfile:
            fieldnames = ['round','agent_name','agent_id','agent position', 'action', 'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            
            # Write header only if file is new
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(record)


    def play_history(self, history_path):
        """Play back the recorded action from the history CSV file with the rendering."""

        actions = []
        with open(history_path, 'r', newline='') as file:
            reader = csv.DictReader(file, delimiter=';')

            # Since there's 2 agents, each two lines correspond to one round of actions
            # create a list of rounds, where each round is a list of the two agents' actions
            current_round = None  
            round_actions = []    
            for row in reader:
                if current_round is None:
                    #first row starts a new round list
                    current_round = int(row['round'])
                    round_actions.append(ACTION_MAP[row['action']])
                elif int(row['round']) == current_round:
                    #same round, add to current round list
                    round_actions.append(ACTION_MAP[row['action']])
                else:
                    #new round, save current and start a new round list
                    actions.append(round_actions)
                    round_actions = []
                    current_round = int(row['round'])
                    round_actions.append(ACTION_MAP[row['action']])
                        
            # Don't forget to append the last round
            if round_actions:
                actions.append(round_actions)

        time.sleep(1)
        self.env.render()
        self.env.step([4,4]) #make them stay so we can see the init state 
        self.env.render()
        time.sleep(2)


        for i in range(len(actions)): 
            # be aware that the last action is probably an invalid action
            time.sleep(1)
            self.env.render() 
            self.env.step(actions[i])
            self.env.render()
            print("Round ", i, " actions: ", ACTION_MAP_REVERSE[actions[i][0]], ACTION_MAP_REVERSE[actions[i][1]])

        self.env.render()
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def run_experiment(self): 
      
        done = False
        current_round = -1
        team_score = None #TODO 

        self.set_chat_agents(self.env.world.agents)

        while not done:
            agents_positions = self.env.world.agents_positions

            actions = []
            messages = []
            response = []
            current_round += 1

            for i in range(self.env.n_agents):
                
                agent = self.chat_agents[i]
                response = agent.makeApiCall(current_round)

                actions.append(response["action"])
                messages.append(response["message"])

                # agent.update_history(current_round, team_score, agents_positions, messages[-1], response["message"], self.str_action(self.env.available_actions(),i)) 

                # Increment round and save the action and message to history
                record = {
                    "round": current_round,
                    "agent_name": AGENT_NAME_MAP[agent.agent_id],
                    "agent_id": agent.agent_id,
                    "agent position": agents_positions[i],
                    "action": ACTION_MAP_REVERSE[response["action"]],
                    "message": response["message"]
                }


                self.history.append(record)
                # Save to CSV
                self.save_history("history/history.csv", record)

            step = self.env.step(actions)
            
            team_score = self.env.world.gems_collected

            self.chat_agents[0].update_history(current_round, team_score, self.env.world.agents_positions, messages[1], messages[0], self.str_action(self.env.available_actions(),0))
            self.chat_agents[1].update_history(current_round, team_score, self.env.world.agents_positions, messages[0], messages[1], self.str_action(self.env.available_actions(),1))


            done = step.is_terminal 

        team_score += 1

        print("Team's score :", team_score)



def main(): 
    world = LLE.from_file("maps/map.txt").obs_type("layered").build()
    env = Environment(world)
    
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg == "run":
        env.run_experiment()
    elif arg == "play":
        env.play_history("play.csv")
    else:
        print("Please provide a valid argument: 'run' or 'play'.")
        sys.exit(1)


if __name__ == "__main__": 
    main()