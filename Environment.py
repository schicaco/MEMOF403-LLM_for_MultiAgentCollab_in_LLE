from lle import LLE
import time
import cv2
import sys
import os 
import csv 

from ChatAgent import ChatAgent
from configs import ACTION_MAP, ACTION_MAP_REVERSE, AGENT_NAME_MAP, COLOR_MAP, BACKGROUND_PROMPT, INITIAL_BELIEF


class Environment():

    def __init__(self, env):
        """
        env = lle environment 
        """
        self.env = env 
        self.chat_agents = []
        self.agents_pos = env.world.agents_positions 
        self.history = [] # list of dict, each dict contains: agent_id, action, message


    def build_background_prompt(self, agent_id, first = False):
        agent_name = AGENT_NAME_MAP[agent_id]
        agent_color = COLOR_MAP[agent_id]

        teammate_ids = [i for i in range(self.env.world.n_agents) if i != agent_id]
        teammates_info = ", ".join(
            f"{AGENT_NAME_MAP[i]}  as {COLOR_MAP[i]}" for i in teammate_ids
        )

        first_background_prompt = ""
        if first: 
            first_background_prompt = "Since this is the round 0, you must remain in your current position to ensure coordination with your other teammates."

        # Build grid size dynamically (in case it's not always 5x5)
        width = self.env.world.width
        height = self.env.world.height

    
        background_prompt = BACKGROUND_PROMPT.format(
            agent_name=agent_name,
            agent_color=agent_color,
            teammates_info=teammates_info,
            width=width,
            height=height,
            width_minus_1 = width - 1,      
            height_minus_1 = height -1,
            first_background_prompt=first_background_prompt
        )

        return background_prompt


    def build_initial_belief(self, agent_id, current_round, team_score,own_messages, team_messages, available_actions):
        
        agent_name = AGENT_NAME_MAP[agent_id]
        agent_color = COLOR_MAP[agent_id]
        agent_pos = self.env.world.agents_positions[agent_id]
        
        
        teammate_ids = [i for i in range(self.env.world.n_agents) if i != agent_id]

        # Teammates info: name, color, and position combined
        teammates_info = ", ".join(
            f"{AGENT_NAME_MAP[i]} is {COLOR_MAP[i]} at {self.env.world.agents_positions[i]}"
            for i in teammate_ids
        )

        # Build team messages string: "from Alpha : 'message'"
        if current_round == "0": 
            team_messages_str = ""
        else: 
            team_messages_str = "; ".join(
                f"from {AGENT_NAME_MAP[i]} : {team_messages[i]}"
                for i in teammate_ids
            )
    
        # Build laser info string
        laser_lines = []
        for i in range(self.env.world.n_laser_colours):
            laser_source = self.env.world.laser_sources[i]
            laser_color = COLOR_MAP[laser_source.agent_id]
            laser_tile_pos = [
                laser.pos for laser in self.env.world.lasers 
                if laser.agent_id == laser_source.agent_id
            ]
            laser_lines.append(
                f"laser beam {laser_color} at {laser_source.pos} projecting at {laser_tile_pos}"
            )
        laser_info = "; ".join(laser_lines) if laser_lines else "no lasers visible"

        # Build gems info string
        state = self.env.world.get_state()  # returns a WorldState
        gems_collected = state.gems_collected  # list[bool], indexed by gem id

        gems_positions = ", ".join(
            str(self.env.world.gems[i].pos) 
            for i in range(self.env.world.n_gems) 
            if not gems_collected[i]
        )
        gems_info = f"diamond at {gems_positions}" if gems_positions else "no diamonds visible"

        # Build wall info string
        wall_positions = self.env.world.wall_pos if hasattr(self.env.world, "wall_pos") else []
        walls_info = "; ".join(str(pos) for pos in wall_positions) if wall_positions else "no walls visible"

        # Exit tiles info
        exits_str = " and ".join(str(pos) for pos in self.env.world.exit_pos)

        # Combine full observation string
        observation_str = (
            f"{laser_info}; {gems_info}; Exit tile at {exits_str}; Walls at {walls_info}"
        )

        initial_belief = INITIAL_BELIEF.format(
            agent_name=agent_name,
            agent_color=agent_color,
            agent_pos=agent_pos,
            current_round=current_round, 
            team_score= team_score, 
            observation_str = observation_str, 
            teammates_info = teammates_info, 
            own_messages = own_messages, 
            team_messages= team_messages_str, 
            available_actions = available_actions
        )

        return initial_belief


    def  set_chat_agents(self, agents):
        messages = ["" for i in range(self.env.n_agents)]

        for i in range(self.env.n_agents):
            chat_agent = ChatAgent(agents[i].num)
            chat_agent.set_background_prompt(self.build_background_prompt(i,False))
            chat_agent.set_background_prompt_first(self.build_background_prompt(i,True))
            chat_agent.set_initial_belief(self.build_initial_belief(i, 0, 0, "", messages, ["STAY"]))
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

        n_agents = self.env.n_agents  # adjust to self.env.world.n_agents if needed

        actions = []
        with open(history_path, 'r', newline='') as file:
            reader = csv.DictReader(file, delimiter=';')

            current_round = None
            round_actions = []
            for row in reader:
                if current_round is None:
                    current_round = int(row['round'])
                    round_actions.append(ACTION_MAP[row['action']])
                elif int(row['round']) == current_round:
                    round_actions.append(ACTION_MAP[row['action']])
                else:
                    actions.append(round_actions)
                    round_actions = []
                    current_round = int(row['round'])
                    round_actions.append(ACTION_MAP[row['action']])

            if round_actions:
                actions.append(round_actions)

        time.sleep(1)
        self.env.render()
        self.env.step([4] * n_agents)  # make everyone stay so we can see the init state
        self.env.render()
        time.sleep(2)

        for i in range(len(actions)):
            time.sleep(1)
            self.env.render()
            self.env.step(actions[i])
            self.env.render()

            round_str = ", ".join(
                ACTION_MAP_REVERSE[actions[i][j]] for j in range(n_agents)
            )
            print("Round ", i, " actions: ", round_str)

        self.env.render()
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def run_experiment(self, history_path): 
      
        done = False
        current_round = -1
        team_score = None 

        self.set_chat_agents(self.env.world.agents)

        while not done:
            agents_positions = self.env.world.agents_positions

            actions = []
            messages = []
            response = []
            current_round += 1

            for i in range(self.env.n_agents):
                
                agent = self.chat_agents[i]

                response = agent.makeApiCall(current_round, agents_positions[i])

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
                self.save_history(history_path, record)

            step = self.env.step(actions)
            
            team_score = self.env.world.gems_collected

            # TODO maybe change to ChatAgent 
            # for i in range(self.env.n_agents): 
            #     self.chat_agents[i].update_history(response["belief"])
            #     self.chat_agents[i].update_history(response["belief"])
            for i in range(self.env.n_agents): 
                self.chat_agents[i].update_history(self.build_initial_belief(i, current_round, team_score, messages[i], messages,self.str_action(self.env.available_actions(),i)))
                self.chat_agents[i].update_history(self.build_initial_belief(i, current_round, team_score, messages[i], messages, self.str_action(self.env.available_actions(),i)))


            done = step.is_terminal 

        team_score += 1

        print("Team's score :", team_score)



def main(): 
    world = LLE.from_file("maps/map.txt").obs_type("layered").build()
    # world = LLE.level(2).obs_type("layered").build()
    env = Environment(world)
    
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg == "run":
        env.run_experiment("history/history_new_belief_handling.csv")
    elif arg == "play":
        env.play_history("play.csv")
    else:
        print("Please provide a valid argument: 'run' or 'play'.")
        sys.exit(1)


if __name__ == "__main__": 
    main()