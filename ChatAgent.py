from ollama import Client 
import re 
import csv 
import sys
import os
import sys

from configs import COLOR_MAP, AGENT_NAME_MAP, INTRO_BELIEF, INITIAL_BELIEF, ACTION_MAP, FIRST_ROUND_BACKGROUND_PROMPT_NEW, BACKGROUND_PROMPT_NEW

LLM_MODEL = 'gpt-oss:120b-cloud'



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
        self.own_messages = ""  # Track messages this agent has sent

        self.background_prompt = ""


        # Initialize belief history to store last 3 rounds
        self.belief_history = []
        self.own_messages_history = []  # Track this agent's sent messages

        self.last_belief = INTRO_BELIEF + INITIAL_BELIEF.format(
            agent_id=self.agent_id,
            agent_color=self.agent_color,
            agent_pos=self.agent_pos,
            current_round=self.current_round,
            team_score=self.team_score,
            team_color=self.team_color,
            team_name=self.team_names,
            team_location=self.team_mate_pos,
            own_messages=self.own_messages,
            team_messages=self.team_messages,
            available_actions="STAY"
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
    

    def save_prompt(self, data_path, round_number, agent_pos, last_belief, agent_raw_response):
        """
        Debug function: Save the prompt that the agent gets and its raw response to a CSV file.

        """

        file_exists = os.path.exists(data_path)

        with open(data_path, 'a', newline='') as csvfile: 
            fieldnames = ['round', 'agent_name','agent_pos', 'last_belief', 'agent_raw_response']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
            
            if not file_exists:
                writer.writeheader()  # Write header if file doesn't exist

            writer.writerow({
                 'round': round_number,
                 'agent_name': AGENT_NAME_MAP[self.agent_id],
                 'agent_pos': agent_pos,
                 'last_belief':  last_belief ,
                 'agent_raw_response':  agent_raw_response 
            })


    def makeApiCall(self, current_round):
        # TODO change how to handle param (moche)

        if current_round == 0:
            self.background_prompt = FIRST_ROUND_BACKGROUND_PROMPT_NEW.format(agent_name=AGENT_NAME_MAP[self.agent_id], agent_color=self.agent_color, team_names = self.team_names, team_color = self.team_color)
        else: 
            self.background_prompt = BACKGROUND_PROMPT_NEW.format(agent_name=AGENT_NAME_MAP[self.agent_id], agent_color=self.agent_color, team_names = self.team_names, team_color = self.team_color)

        client = Client()
        messages = [
        {
            'role': 'user',
            'content': self.background_prompt + "\n" + self.last_belief,
        },
        ]

        # print(f"In makeApiCall :: Agent {AGENT_NAME_MAP[self.agent_id]} (ID: {self.agent_id}) at position {self.agent_pos} making API call for round {current_round} with belief state:\n{self.last_belief}\n")
        message = ''
        for part in client.chat(LLM_MODEL, messages=messages, stream=True):
             message += part['message']['content']


        self.save_prompt("history/prompt_history.csv", current_round, self.agent_pos, self.last_belief, message)

        parsed_message = self.parse_agent_response(message)

        return parsed_message 
    

    def update_history(self, current_round, team_score, agents_pos, team_messages, own_message, available_actions): 
        """
        Update parameters of  chatAgent after each round, which will be included in the belief state for the next round.
        Keeps only the last 5 rounds of belief states.
        """
        self.current_round = current_round
        self.team_score = team_score
        self.agent_pos = agents_pos[self.agent_id]
        self.team_mate_pos = agents_pos[1 - self.agent_id]
        self.team_messages = team_messages
        self.own_messages = own_message
        self.available_actions = available_actions

        #print current round agent name and it's position and action taken
        # print(f"In chatAgent in update history  :: Round {current_round}, Agent {AGENT_NAME_MAP[self.agent_id]} (ID: {self.agent_id}) at position {self.agent_pos} with available actions: {self.available_actions} and team messages: {self.team_messages} and own message: {self.own_messages}\n")

        # Extract the belief state portion without INTRO_BELIEF and add to history
        belief_state_only = INITIAL_BELIEF.format(
            agent_id=self.agent_id,
            agent_color=self.agent_color,
            agent_pos=self.agent_pos,
            current_round=self.current_round,
            team_score=self.team_score,
            team_color=self.team_color,
            team_name=self.team_names,
            team_location=self.team_mate_pos,
            own_messages=self.own_messages,
            team_messages=self.team_messages,
            available_actions=self.available_actions
        )
        
        # Add current belief to history and keep only last 4
        self.belief_history.append(belief_state_only)
        if len(self.belief_history) > 5:
            self.belief_history = self.belief_history[-5:]
        
        # Track own messages history
        self.own_messages_history.append(own_message)
        if len(self.own_messages_history) > 5:
            self.own_messages_history = self.own_messages_history[-5:]

        belief_string = ""
        # Build the new belief state with INTRO_BELIEF for current and run numbers for old ones
        for idx, old_belief in enumerate(self.belief_history[:-1], start=1):
            belief_string += f"\nRun {idx+1}: {old_belief}"
        
        # Add old belief states with run numbers (most recent first)
        belief_string += "\n" + INTRO_BELIEF
        # Add current belief state
        belief_string += INITIAL_BELIEF.format(
            agent_id=self.agent_id,
            agent_color=self.agent_color,
            agent_pos=self.agent_pos,
            current_round=self.current_round,
            team_score=self.team_score,
            team_color=self.team_color,
            team_name=self.team_names,
            team_location=self.team_mate_pos,
            own_messages=self.own_messages,
            team_messages=self.team_messages,
            available_actions=self.available_actions
        )

        self.last_belief = belief_string
