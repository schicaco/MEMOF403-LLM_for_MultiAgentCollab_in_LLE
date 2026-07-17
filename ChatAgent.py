from ollama import Client 
import re 
import csv 
import sys
import os
import sys

from configs import AGENT_NAME_MAP, INTRO_BELIEF, ACTION_MAP, UPDATE_PROMPT

LLM_MODEL = 'gpt-oss:120b-cloud'


class ChatAgent(): 

    def __init__(self, agent_id, zero_shot):

        self.agent_id = agent_id

        self.current_round = 0

        self.own_messages = ""  # Track messages this agent has sent
        self.background_prompt = ""
        self.background_prompt_first = ""
        self.last_belief = ""
        self.update_prompt = ""
        self.zero_shot = zero_shot

        # Initialize belief history to store last 3 rounds
        self.belief_history = []
        self.own_messages_history = []  # Track this agent's sent messages

    def set_background_prompt(self, background_prompt): 
        self.background_prompt = background_prompt

    def set_background_prompt_first(self, background_prompt_first): 
        self.background_prompt_first = background_prompt_first

    def set_update_prompt(self, update_prompt):
        self.update_prompt = update_prompt

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
        result = {"action": None, "message": None, "belief": None}

        belief_match = None
        if self.zero_shot:
            belief_match = re.search(
                r"Below is your current belief.*?(?=\n\s*Action selection:|\Z)",
                text,
                re.DOTALL
            )
            if not belief_match:
                print("Error: Response format is incorrect. Expected a belief state "
                    "starting with 'Below is your current belief'.")
                sys.exit(1)
            raw_belief = belief_match.group(0).strip()
            result["belief"] = raw_belief.replace("Below is your current belief", INTRO_BELIEF, 1)

        action_match = re.search(r"Action selection:\s*(.+?)(?=\n\s*Message to Team:|\Z)", text, re.DOTALL)
        message_match = re.search(r"Message to Team:\s*(.+)", text, re.DOTALL)

        if not (action_match and message_match):
            print("Error: Response format is incorrect. Expected format: "
                "Action selection: 'Your action', Message to Team: 'Your Message'.")
            sys.exit(1)

        result["action"] = self.parse_action(action_match.group(1).strip())
        result["message"] = message_match.group(1).strip()

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


    def makeApiCall(self, current_round, agent_pos, prompt_history):

        self.current_round = current_round

        background_prompt = self.background_prompt

        if self.zero_shot: 
            text = background_prompt + "\n" + self.last_belief + "\n" +  self.update_prompt
        else: 
            text = background_prompt + "\n" + self.last_belief + "\n" 

        client = Client()
        messages = [
        {
            'role': 'user',
            'content': text,
        },
        ]
        message = ''
        for part in client.chat(LLM_MODEL, messages=messages, stream=True):
             message += part['message']['content']

        # message ="- Below is your current belief  : '[from agent id ="  + str(self.agent_id) +"] , Action selection: 'STAY', Message to Team: my message to the team from me with id " + str(self.agent_id)+ " in the current round - " + str(current_round) 
        
        self.save_prompt(prompt_history, self.current_round, agent_pos, self.last_belief, message)

        parsed_message = self.parse_agent_response(message)

        return parsed_message 
    

    def update_history(self, new_belief, round_number=None): 
        """
        Update parameters of chatAgent after each round, which will be included in the belief state for the next round.
        Keeps only the last 5 rounds of belief states and labels them with their actual round numbers.
        """

        if round_number is None:
            round_number = self.current_round

        # Store each belief with its real round number and keep only the last 5
        self.belief_history.append((round_number, new_belief))
        if len(self.belief_history) > 5:
            self.belief_history = self.belief_history[-5:]

        belief_string = ""
        # Build the new belief state with actual run numbers for historical entries
        for history_round, old_belief in self.belief_history[:-1]:
            belief_string += f"\nRun {history_round+1}: {old_belief}"
        

        if not self.zero_shot: 
            belief_string += "\n" + INTRO_BELIEF
        belief_string += new_belief

        self.last_belief = belief_string
