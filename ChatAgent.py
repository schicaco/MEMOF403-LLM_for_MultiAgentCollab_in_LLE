from ollama import Client 
import re 
import csv 
import sys
import os
import sys
import collections

from configs import AGENT_NAME_MAP, INTRO_BELIEF, ACTION_MAP, UPDATE_PROMPT, ACTION_MAP_REVERSE

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

    def set_last_belief(self, last_belief): 
        self.last_belief = last_belief

    def set_current_round(self, round): 
        self.current_round = round

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
                r"Belief state: .*?(?=\n\s*Action selection:|\Z)",
                text,
                re.DOTALL
            )
            if not belief_match:
                print("Error: Response format is incorrect. Expected a belief state "
                    "starting with 'Belief state: '.")
                sys.exit(1)
            result["belief"] = belief_match.group(0).strip()

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
            text =  self.last_belief + "\n" +  self.update_prompt
        else: 
            text = self.last_belief + "\n" 

        client = Client()
        messages = [
            {'role': 'system', 'content': background_prompt},
            {'role': 'user','content': text},
        ]
        raw_message = ''
        for part in client.chat(LLM_MODEL, messages=messages, stream=True):
             raw_message += part['message']['content']

        parsed_message = self.parse_agent_response(raw_message)
        
        self.save_prompt(prompt_history, self.current_round, agent_pos, self.last_belief, "raw message " + str(current_round))
        
        # parsed_message = {"action": 1, "message": "test","belief": " belief " + str(current_round) }
        # self.save_prompt(prompt_history, current_round, agent_pos, self.last_belief, "raw message " + str(current_round))

        return parsed_message 
    

    def update_history(self, new_belief, round_number=None): 
        """
        Update parameters of chatAgent after each round, which will be included in the belief state for the next round.
        Keeps only the last 5 rounds of belief states and labels them with their actual round numbers.
        """

        if round_number is None:
            round_number = self.current_round

        print("\n NEW BELIEF (agent id :   " +  str(self.agent_id) + ") :  " + new_belief + "\n")


        # Store each belief with its real round number and keep only the last 5
        self.belief_history.append((round_number, new_belief))
        if len(self.belief_history) > 5:
            self.belief_history = self.belief_history[-5:]

        print("\n belief history: ", self.belief_history)

        belief_string = ""
        # Build the new belief state with actual run numbers for historical entries
        for history_round, old_belief in self.belief_history[:-1]:
            belief_string += f"\nRun {history_round+1}: {old_belief}"
        

        belief_string += "\n" + INTRO_BELIEF
        
        belief_string += new_belief
        # else: 
        #     belief_string = new_belief
        self.last_belief = belief_string
