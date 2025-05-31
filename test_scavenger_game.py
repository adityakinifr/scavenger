#!/usr/bin/env python3
"""
Test script for the Portland Scavenger Hunt Game
Tests game logic, OpenAI integration, and scoring system.
"""

import os
import sys
from datetime import datetime

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_game_import():
    """Test that the scavenger game module can be imported."""
    try:
        from scavenger_game import ScavengerHuntGame, game
        print("✅ Successfully imported scavenger_game module")
        return True
    except ImportError as e:
        print(f"❌ Failed to import scavenger_game: {e}")
        return False

def test_openai_setup():
    """Test OpenAI configuration."""
    try:
        import openai
        api_key = os.environ.get('OPENAI_API_KEY')
        if api_key:
            print("✅ OpenAI API key found in environment")
            if api_key.startswith('sk-'):
                print("✅ OpenAI API key format looks correct")
            else:
                print("⚠️  OpenAI API key format may be incorrect (should start with 'sk-')")
        else:
            print("⚠️  OpenAI API key not found - game will use fallback string matching")
        return True
    except ImportError as e:
        print(f"❌ Failed to import openai: {e}")
        return False

def test_game_initialization():
    """Test game initialization and basic functionality."""
    try:
        from scavenger_game import ScavengerHuntGame
        
        # Create a test game instance
        test_game = ScavengerHuntGame()
        
        # Test clues are loaded
        if len(test_game.clues) == 5:
            print("✅ All 5 Portland clues loaded successfully")
        else:
            print(f"❌ Expected 5 clues, found {len(test_game.clues)}")
            return False
        
        # Test clue structure
        first_clue = test_game.clues[0]
        required_keys = ['id', 'clue', 'expected_answers', 'hints', 'location']
        
        for key in required_keys:
            if key not in first_clue:
                print(f"❌ Missing required key '{key}' in clue structure")
                return False
        
        print("✅ Clue structure is valid")
        
        # Test that each clue has the right number of hints
        for i, clue in enumerate(test_game.clues):
            if len(clue['hints']) != 3:
                print(f"❌ Clue {i+1} has {len(clue['hints'])} hints, expected 3")
                return False
        
        print("✅ All clues have 3 hints each")
        return True
        
    except Exception as e:
        print(f"❌ Game initialization failed: {e}")
        return False

def test_game_flow():
    """Test the complete game flow with a mock player."""
    try:
        from scavenger_game import ScavengerHuntGame
        
        test_game = ScavengerHuntGame()
        test_phone = "+1234567890"
        
        print("\n🎮 Testing Game Flow:")
        
        # Test game start
        start_response = test_game.start_game(test_phone)
        if "Welcome to the Portland Scavenger Hunt" in start_response:
            print("✅ Game start message is correct")
        else:
            print("❌ Game start message is incorrect")
            return False
        
        # Check player data was created
        player = test_game.get_player_data(test_phone)
        if player["game_started"] and player["current_clue"] == 1:
            print("✅ Player data initialized correctly")
        else:
            print("❌ Player data not initialized correctly")
            return False
        
        # Test correct answer (first clue - Rose Garden)
        correct_answers = ["Rose Garden", "International Rose Test Garden", "Portland Rose Garden"]
        
        for answer in correct_answers:
            # Reset for each test
            test_game.players[test_phone]["current_clue"] = 1
            test_game.players[test_phone]["hints_used"] = 0
            
            response = test_game.process_answer(test_phone, answer)
            if "Correct! You earned 40 points" in response:
                print(f"✅ Correct answer '{answer}' recognized and scored properly")
                break
        else:
            print("❌ None of the correct answers were recognized")
            return False
        
        # Test wrong answer and hint system
        test_game.players[test_phone]["current_clue"] = 1
        test_game.players[test_phone]["hints_used"] = 0
        
        wrong_response = test_game.process_answer(test_phone, "Wrong Answer")
        if "Not quite right! Here's a hint:" in wrong_response:
            print("✅ Wrong answer triggers hint correctly")
        else:
            print("❌ Wrong answer doesn't trigger hint")
            return False
        
        # Test status command
        status_response = test_game.get_status(test_phone)
        if "Current Status:" in status_response:
            print("✅ Status command works correctly")
        else:
            print("❌ Status command not working")
            return False
        
        print("✅ Game flow test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Game flow test failed: {e}")
        return False

def test_scoring_system():
    """Test the scoring system with different hint scenarios."""
    try:
        from scavenger_game import ScavengerHuntGame
        
        test_game = ScavengerHuntGame()
        test_phone = "+1234567891"
        
        print("\n🏆 Testing Scoring System:")
        
        # Test scoring with no hints (should get 40 points)
        test_game.start_game(test_phone)
        response = test_game.process_answer(test_phone, "Rose Garden")
        
        player = test_game.get_player_data(test_phone)
        if player["total_score"] == 40:
            print("✅ No hints: 40 points awarded correctly")
        else:
            print(f"❌ Expected 40 points, got {player['total_score']}")
            return False
        
        # Test scoring with 1 hint (should get 30 points)
        test_game.players[test_phone]["current_clue"] = 2
        test_game.players[test_phone]["hints_used"] = 0
        
        # Get a hint first
        test_game.process_answer(test_phone, "Wrong Answer")
        # Then answer correctly
        response = test_game.process_answer(test_phone, "Powell's Books")
        
        if player["total_score"] == 70:  # 40 + 30
            print("✅ With 1 hint: 30 points awarded correctly")
        else:
            print(f"❌ Expected 70 total points, got {player['total_score']}")
            return False
        
        print("✅ Scoring system test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Scoring system test failed: {e}")
        return False

def test_portland_locations():
    """Test that all Portland locations are properly represented."""
    try:
        from scavenger_game import ScavengerHuntGame
        
        test_game = ScavengerHuntGame()
        
        print("\n🌲 Testing Portland Locations:")
        
        expected_locations = [
            "Washington Park",
            "Pearl District", 
            "Downtown Portland",
            "Downtown Portland",
            "Waterfront"
        ]
        
        expected_keywords = [
            ["rose", "garden", "international"],
            ["powell", "books", "bookstore"],
            ["voodoo", "doughnut", "donut"],
            ["pioneer", "courthouse", "square"],
            ["waterfront", "park", "mccall"]
        ]
        
        for i, clue in enumerate(test_game.clues):
            # Check location
            if clue["location"] == expected_locations[i]:
                print(f"✅ Clue {i+1}: Location '{clue['location']}' is correct")
            else:
                print(f"❌ Clue {i+1}: Expected '{expected_locations[i]}', got '{clue['location']}'")
                return False
            
            # Check that clue contains expected keywords
            clue_text = clue["clue"].lower()
            keywords = expected_keywords[i]
            
            if any(keyword in clue_text for keyword in keywords):
                print(f"✅ Clue {i+1}: Contains relevant Portland keywords")
            else:
                print(f"❌ Clue {i+1}: Missing expected keywords {keywords}")
                return False
        
        print("✅ All Portland locations properly represented")
        return True
        
    except Exception as e:
        print(f"❌ Portland locations test failed: {e}")
        return False

def test_flask_integration():
    """Test that the Flask app can import and use the game."""
    try:
        # Test importing the main app
        from app import app, process_scavenger_hunt_message
        
        print("\n🌐 Testing Flask Integration:")
        
        # Test that the game is imported in the app
        test_response = process_scavenger_hunt_message("READY", "+1234567892")
        
        if "Welcome to the Portland Scavenger Hunt" in test_response:
            print("✅ Flask app successfully integrates with scavenger game")
        else:
            print("❌ Flask app integration failed")
            return False
        
        # Test help command
        help_response = process_scavenger_hunt_message("HELP", "+1234567892")
        if "Portland Scavenger Hunt Help" in help_response:
            print("✅ Help command works in Flask integration")
        else:
            print("❌ Help command failed in Flask integration")
            return False
        
        print("✅ Flask integration test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Flask integration test failed: {e}")
        return False

def main():
    """Run all tests and provide a summary."""
    print("🎯 Portland Scavenger Hunt Game - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Game Import", test_game_import),
        ("OpenAI Setup", test_openai_setup),
        ("Game Initialization", test_game_initialization),
        ("Game Flow", test_game_flow),
        ("Scoring System", test_scoring_system),
        ("Portland Locations", test_portland_locations),
        ("Flask Integration", test_flask_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} Test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your Portland Scavenger Hunt is ready to go!")
        print("\nNext steps:")
        print("1. Set up your .env file with Twilio and OpenAI credentials")
        print("2. Run 'python app.py' to start the server")
        print("3. Configure Twilio webhooks to point to your server")
        print("4. Send 'READY' to your Twilio number to start playing!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 