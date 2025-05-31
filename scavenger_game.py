"""
Portland Scavenger Hunt Game Logic
Manages game state, clues, scoring, and OpenAI integration for natural language processing.
"""

import openai
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class ScavengerHuntGame:
    def __init__(self):
        # Initialize OpenAI client only if API key is available
        api_key = os.environ.get('OPENAI_API_KEY')
        if api_key and not api_key.startswith('your_'):
            try:
                self.openai_client = openai.OpenAI(api_key=api_key)
                self.has_openai = True
            except Exception as e:
                print(f"Warning: OpenAI initialization failed: {e}")
                self.openai_client = None
                self.has_openai = False
        else:
            self.openai_client = None
            self.has_openai = False
        
        # Game data storage (in production, use a database)
        self.players = {}  # phone_number -> player_data
        
        # Portland Scavenger Hunt Clues
        self.clues = [
            {
                "id": 1,
                "clue": "🌹 Start your adventure at Portland's most famous garden, where over 10,000 rose bushes bloom. This International Rose Test Garden has been testing roses since 1917. What's the name of this fragrant paradise?",
                "expected_answers": [
                    "International Rose Test Garden",
                    "Rose Test Garden", 
                    "Rose Garden",
                    "International Rose Garden",
                    "Portland Rose Garden"
                ],
                "hints": [
                    "🌹 This garden is in Washington Park and offers stunning views of Mount Hood on clear days.",
                    "🌹 It's located in the same park as the Japanese Garden and has 'International' in its name.",
                    "🌹 The garden tests new rose varieties and has been doing so for over 100 years!"
                ],
                "location": "Washington Park"
            },
            {
                "id": 2,
                "clue": "📚 Next, visit the largest independent bookstore in the world! This colorful store takes up an entire city block and has a slogan about covering the city. Where are you going?",
                "expected_answers": [
                    "Powell's Books",
                    "Powell's City of Books",
                    "Powells",
                    "Powell's",
                    "City of Books"
                ],
                "hints": [
                    "📚 The store uses different colored rooms (Blue, Red, Green, etc.) to organize its sections.",
                    "📚 It's located in the Pearl District and their slogan mentions 'covering' something.",
                    "📚 The founder's last name is Powell, and they claim to cover the city like a good book!"
                ],
                "location": "Pearl District"
            },
            {
                "id": 3,
                "clue": "🍩 Time for a sweet treat! Head to the place where the donuts are as weird as the city's slogan. This iconic pink box shop has been serving unusual flavors since 2003. The owner's goal was to keep Portland weird. What's this donut shop called?",
                "expected_answers": [
                    "Voodoo Doughnut",
                    "Voodoo Donuts",
                    "Voodoo Doughnuts",
                    "Voodoo",
                    "VooDoo Doughnut"
                ],
                "hints": [
                    "🍩 They're famous for donuts with cereal on top and bacon-covered varieties.",
                    "🍩 The shop has a pink neon sign and is often associated with 'magic' or 'spells'.",
                    "🍩 Their most famous donut is covered in Fruit Loops cereal!"
                ],
                "location": "Downtown Portland"
            },
            {
                "id": 4,
                "clue": "🏛️ Now explore Portland's living room! This beautiful public square hosts farmers markets, festivals, and events. It's been the heart of downtown since 1984 and is named after a civic leader. What's this gathering place called?",
                "expected_answers": [
                    "Pioneer Courthouse Square",
                    "Pioneer Square",
                    "Courthouse Square",
                    "Pioneer Courthouse",
                    "Portland's Living Room"
                ],
                "hints": [
                    "🏛️ It's directly across from a historic federal courthouse built in the 1870s.",
                    "🏛️ The square features red brick and often has a large Christmas tree during holidays.",
                    "🏛️ It's nicknamed 'Portland's Living Room' and hosts the annual Festival of Lights!"
                ],
                "location": "Downtown Portland"
            },
            {
                "id": 5,
                "clue": "🌊 For your final destination, visit the area where two major rivers meet! This waterfront district offers great views, food carts, and Saturday Market. It's named after the direction you'd travel to reach the ocean. What's this riverside area called?",
                "expected_answers": [
                    "Tom McCall Waterfront Park",
                    "Waterfront Park",
                    "Tom McCall Park",
                    "McCall Waterfront Park",
                    "Waterfront District",
                    "Saturday Market area"
                ],
                "hints": [
                    "🌊 This park stretches along the Willamette River and hosts the Saturday Market.",
                    "🌊 It's named after a former Oregon governor who was known for environmental protection.",
                    "🌊 The park offers great views of the Hawthorne and Morrison bridges!"
                ],
                "location": "Waterfront"
            }
        ]
    
    def get_player_data(self, phone_number: str) -> Dict:
        """Get or create player data."""
        if phone_number not in self.players:
            self.players[phone_number] = {
                "current_clue": 0,
                "total_score": 0,
                "hints_used": 0,
                "game_started": False,
                "completed_clues": [],
                "start_time": None,
                "last_activity": datetime.now().isoformat()
            }
        return self.players[phone_number]
    
    def start_game(self, phone_number: str) -> str:
        """Start the scavenger hunt game."""
        player = self.get_player_data(phone_number)
        player["game_started"] = True
        player["current_clue"] = 1
        player["start_time"] = datetime.now().isoformat()
        player["hints_used"] = 0
        
        welcome_msg = """🎯 Welcome to the Portland Scavenger Hunt! 🌲

You'll visit 5 amazing Portland locations. Answer correctly to earn points:
• First try: 40 points
• With 1 hint: 30 points  
• With 2 hints: 20 points
• With 3 hints: 10 points

Let's begin your adventure!

"""
        
        first_clue = self.clues[0]["clue"]
        return welcome_msg + first_clue
    
    def process_answer(self, phone_number: str, user_message: str) -> str:
        """Process user's answer using OpenAI to check if it matches expected responses."""
        player = self.get_player_data(phone_number)
        
        if not player["game_started"]:
            return "Send 'READY' to start the Portland Scavenger Hunt! 🎯"
        
        current_clue_index = player["current_clue"] - 1
        if current_clue_index >= len(self.clues):
            return self.get_final_score(phone_number)
        
        current_clue = self.clues[current_clue_index]
        
        # Use OpenAI to check if the answer is correct
        is_correct = self.check_answer_with_ai(user_message, current_clue["expected_answers"])
        
        if is_correct:
            return self.handle_correct_answer(phone_number)
        else:
            return self.handle_incorrect_answer(phone_number)
    
    def check_answer_with_ai(self, user_answer: str, expected_answers: List[str]) -> bool:
        """Use OpenAI to determine if the user's answer matches any expected answer."""
        if not self.has_openai or not self.openai_client:
            # Fallback to simple string matching if no OpenAI
            user_lower = user_answer.lower()
            return any(expected.lower() in user_lower for expected in expected_answers)
        
        try:
            expected_list = ", ".join(expected_answers)
            
            prompt = f"""
You are helping with a Portland scavenger hunt. Determine if the user's answer matches any of the expected answers.

Expected answers: {expected_list}

User's answer: "{user_answer}"

The user's answer should be considered correct if it:
1. Contains the main name/location mentioned in the expected answers
2. Is clearly referring to the same place, even with different wording
3. Has minor spelling variations or abbreviations

Respond with only "CORRECT" or "INCORRECT".
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0
            )
            
            result = response.choices[0].message.content.strip().upper()
            return result == "CORRECT"
            
        except Exception as e:
            print(f"OpenAI error: {e}")
            # Fallback to simple matching
            user_lower = user_answer.lower()
            return any(expected.lower() in user_lower for expected in expected_answers)
    
    def handle_correct_answer(self, phone_number: str) -> str:
        """Handle when user gets the answer correct."""
        player = self.get_player_data(phone_number)
        current_clue_index = player["current_clue"] - 1
        current_clue = self.clues[current_clue_index]
        
        # Calculate points based on hints used
        points_map = {0: 40, 1: 30, 2: 20, 3: 10}
        points = points_map.get(player["hints_used"], 10)
        
        player["total_score"] += points
        player["completed_clues"].append({
            "clue_id": current_clue["id"],
            "points_earned": points,
            "hints_used": player["hints_used"]
        })
        
        response = f"🎉 Correct! You earned {points} points!\n\n"
        
        # Move to next clue
        player["current_clue"] += 1
        player["hints_used"] = 0  # Reset hints for next clue
        
        if player["current_clue"] <= len(self.clues):
            if player["current_clue"] == len(self.clues) + 1:
                # Game completed
                return response + self.get_final_score(phone_number)
            else:
                # Next clue
                next_clue = self.clues[player["current_clue"] - 1]
                response += f"📍 Clue {player['current_clue']}/5:\n\n{next_clue['clue']}"
        
        return response
    
    def handle_incorrect_answer(self, phone_number: str) -> str:
        """Handle when user gets the answer wrong."""
        player = self.get_player_data(phone_number)
        current_clue_index = player["current_clue"] - 1
        current_clue = self.clues[current_clue_index]
        
        if player["hints_used"] < len(current_clue["hints"]):
            # Provide a hint
            hint = current_clue["hints"][player["hints_used"]]
            player["hints_used"] += 1
            
            return f"❌ Not quite right! Here's a hint:\n\n{hint}\n\nTry again! 🤔"
        else:
            # No more hints, give the answer and move on
            correct_answer = current_clue["expected_answers"][0]
            player["total_score"] += 5  # Consolation points
            player["completed_clues"].append({
                "clue_id": current_clue["id"],
                "points_earned": 5,
                "hints_used": player["hints_used"]
            })
            
            response = f"❌ The answer was: {correct_answer}\nYou get 5 consolation points! 💪\n\n"
            
            # Move to next clue
            player["current_clue"] += 1
            player["hints_used"] = 0
            
            if player["current_clue"] <= len(self.clues):
                if player["current_clue"] == len(self.clues) + 1:
                    return response + self.get_final_score(phone_number)
                else:
                    next_clue = self.clues[player["current_clue"] - 1]
                    response += f"📍 Clue {player['current_clue']}/5:\n\n{next_clue['clue']}"
            
            return response
    
    def get_final_score(self, phone_number: str) -> str:
        """Get final score and game completion message."""
        player = self.get_player_data(phone_number)
        
        score_msg = f"""🏆 Congratulations! You've completed the Portland Scavenger Hunt!

Final Score: {player['total_score']} points

Your Performance:
"""
        
        for completed in player["completed_clues"]:
            clue_id = completed["clue_id"]
            points = completed["points_earned"]
            hints = completed["hints_used"]
            score_msg += f"• Clue {clue_id}: {points} points ({hints} hints used)\n"
        
        # Score ranking
        if player['total_score'] >= 180:
            rank = "🥇 Portland Expert!"
        elif player['total_score'] >= 150:
            rank = "🥈 City Explorer!"
        elif player['total_score'] >= 100:
            rank = "🥉 Tourist Guide!"
        else:
            rank = "🎯 Adventure Seeker!"
        
        score_msg += f"\nRank: {rank}\n\nThanks for exploring Portland! Send 'READY' to play again! 🌲"
        
        # Reset player for new game
        self.players[phone_number] = {
            "current_clue": 0,
            "total_score": 0,
            "hints_used": 0,
            "game_started": False,
            "completed_clues": [],
            "start_time": None,
            "last_activity": datetime.now().isoformat()
        }
        
        return score_msg
    
    def get_status(self, phone_number: str) -> str:
        """Get current game status for a player."""
        player = self.get_player_data(phone_number)
        
        if not player["game_started"]:
            return "🎯 Ready to explore Portland? Send 'READY' to start the scavenger hunt!"
        
        current_clue_num = player["current_clue"]
        if current_clue_num > len(self.clues):
            return "🏆 Game completed! Send 'READY' to play again!"
        
        return f"""📊 Current Status:
• Clue: {current_clue_num}/5
• Score: {player['total_score']} points
• Hints used this clue: {player['hints_used']}/3

Current clue: {self.clues[current_clue_num - 1]['clue']}"""

# Global game instance
game = ScavengerHuntGame() 