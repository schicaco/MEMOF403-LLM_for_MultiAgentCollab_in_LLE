from ollama import Client 
import re 
import csv 
import sys
import os
import sys

from configs import AGENT_NAME_MAP, INTRO_BELIEF, ACTION_MAP

LLM_MODEL = 'gpt-oss:120b-cloud'



class ChatAgent(): 

    def __init__(self, agent_id):

        self.agent_id = agent_id

        self.current_round = 0

        self.own_messages = ""  # Track messages this agent has sent
        self.background_prompt = ""
        self.background_prompt_first = ""
        self.last_belief = ""

        # Initialize belief history to store last 3 rounds
        self.belief_history = []
        self.own_messages_history = []  # Track this agent's sent messages

    def set_background_prompt(self, background_prompt): 
        self.background_prompt = background_prompt

    def set_background_prompt_first(self, background_prompt_first): 
        self.background_prompt_first = background_prompt_first

    def set_initial_belief(self, initial_belief): 
        self.last_belief = INTRO_BELIEF + initial_belief

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


    def makeApiCall(self, current_round, agent_pos):

        self.current_round = current_round

        if current_round == 0:
            # background_prompt = self.background_prompt + "Since this is the round 0, you must remain in your current position to ensure coordination with your other teammates."
            background_prompt = self.background_prompt_first
        else: 
            background_prompt = self.background_prompt

        client = Client()
        messages = [
        {
            'role': 'user',
            'content': background_prompt + "\n" + self.last_belief,
        },
        ]

        message = ''
        for part in client.chat(LLM_MODEL, messages=messages, stream=True):
             message += part['message']['content']

        self.save_prompt("history/prompt_history.csv", self.current_round, agent_pos, self.last_belief, message)

        parsed_message = self.parse_agent_response(message)

        return parsed_message 
    

    def update_history(self, initial_belief, own_message): 
        """
        Update parameters of  chatAgent after each round, which will be included in the belief state for the next round.
        Keeps only the last 5 rounds of belief states.
        """

        # Add current belief to history and keep only last 4
        self.belief_history.append(initial_belief)
        if len(self.belief_history) > 5:
            self.belief_history = self.belief_history[-5:]
        
        # Track own messages history
        self.own_messages_history.append(own_message)
        if len(self.own_messages_history) > 5:
            self.own_messages_history = self.own_messages_history[-5:]

        belief_string = ""
        # Build the new belief state with INTRO_BELIEF for current and run numbers for old ones
        for idx, old_belief in enumerate(self.belief_history[:-1], start=1):
            belief_string += f"\nRun {self.current_round+idx}: {old_belief}"
        
        # Add old belief states with run numbers (most recent first)
        belief_string += "\n" + INTRO_BELIEF
        # Add current belief state
        belief_string += initial_belief

        self.last_belief = belief_string
