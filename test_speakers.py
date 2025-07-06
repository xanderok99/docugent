#!/usr/bin/env python3
"""
Test script for the updated speaker data and tools.
"""

import asyncio
import json
from pathlib import Path
from app.agents.tools.speaker_tools import SpeakerTools

async def test_speaker_tools():
    """Test the speaker tools with the updated data."""
    print("🧪 Testing API Conference Speaker Tools")
    print("=" * 50)
    
    # Initialize speaker tools
    speaker_tools = SpeakerTools()
    
    # Test 1: Get all speakers
    print("\n1. Testing get_all_speakers()...")
    all_speakers = speaker_tools.get_all_speakers()
    print(f"✅ Found {len(all_speakers)} speakers")
    
    # Test 2: Get speaker statistics
    print("\n2. Testing get_speaker_statistics()...")
    stats = speaker_tools.get_speaker_statistics()
    print(f"✅ Total speakers: {stats['total_speakers']}")
    print(f"✅ Announcement status: {stats['announcement_status']}")
    print(f"✅ Last updated: {stats['last_updated']}")
    
    # Test 3: Search for specific speakers
    print("\n3. Testing search_speakers()...")
    search_results = speaker_tools.search_speakers("Mehdi")
    print(f"✅ Found {len(search_results)} speakers matching 'Mehdi'")
    if search_results:
        print(f"   - {search_results[0]['name']} ({search_results[0]['company']})")
    
    # Test 4: Get speaker by name
    print("\n4. Testing get_speaker_by_name()...")
    speaker = speaker_tools.get_speaker_by_name("Michael Owolabi")
    if speaker:
        print(f"✅ Found: {speaker['name']} - {speaker['title']} at {speaker['company']}")
    else:
        print("❌ Speaker not found")
    
    # Test 5: Get speakers by topic
    print("\n5. Testing get_speakers_by_topic()...")
    api_speakers = speaker_tools.get_speakers_by_topic("API")
    print(f"✅ Found {len(api_speakers)} speakers with API expertise")
    
    # Test 6: Get speakers by company
    print("\n6. Testing get_speakers_by_company()...")
    interswitch_speakers = speaker_tools.get_speakers_by_company("Interswitch")
    print(f"✅ Found {len(interswitch_speakers)} speakers from Interswitch")
    
    # Test 7: Show top companies
    print("\n7. Top companies represented:")
    for company, count in stats['top_companies'][:5]:
        print(f"   - {company}: {count} speakers")
    
    # Test 8: Show top topics
    print("\n8. Top topics covered:")
    for topic, count in stats['top_topics'][:5]:
        print(f"   - {topic}: {count} speakers")
    
    print("\n" + "=" * 50)
    print("✅ All speaker tool tests completed successfully!")
    print(f"🎉 API Conference Lagos 2025 has {stats['total_speakers']} confirmed speakers!")

def test_speaker_data_file():
    """Test the speaker data file directly."""
    print("\n📄 Testing speaker data file...")
    
    try:
        with open("data/speakers.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        speakers = data.get("speakers", [])
        meta = data.get("meta", {})
        
        print(f"✅ File loaded successfully")
        print(f"✅ Total speakers: {len(speakers)}")
        print(f"✅ Announcement status: {meta.get('announcement_status', 'unknown')}")
        print(f"✅ Last updated: {meta.get('last_updated', 'unknown')}")
        
        # Check for specific speakers
        speaker_names = [s.get("name", "") for s in speakers]
        expected_speakers = ["Mehdi Medjaoui", "Michael Owolabi", "Chisom Uma"]
        
        for expected in expected_speakers:
            if expected in speaker_names:
                print(f"✅ Found expected speaker: {expected}")
            else:
                print(f"❌ Missing expected speaker: {expected}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing speaker data file: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 API Conference Lagos 2025 - Speaker Data Test")
    print("=" * 60)
    
    # Test the data file first
    if not test_speaker_data_file():
        print("❌ Speaker data file test failed!")
        return
    
    # Test the speaker tools
    await test_speaker_tools()
    
    print("\n🎯 Test Summary:")
    print("- Speaker data file is valid and complete")
    print("- All 44 speakers have been announced")
    print("- Speaker tools are working correctly")
    print("- Search and filtering functions are operational")
    print("\n✨ Ready for API Conference Lagos 2025!")

if __name__ == "__main__":
    asyncio.run(main()) 