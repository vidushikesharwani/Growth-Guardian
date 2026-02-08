"""
WHO Milestone Checker
Compares child's milestones against WHO standards
"""

# WHO MILESTONE STANDARDS (in months)
WHO_MILESTONES = {
    "motor": {
        "lifts_head": {
            "name": "Lifts head when on tummy",
            "normal_age_months": 1,
            "delay_threshold_months": 3
        },
        "holds_head_steady": {
            "name": "Holds head steady",
            "normal_age_months": 2,
            "delay_threshold_months": 4
        },
        "sits_with_support": {
            "name": "Sits with support",
            "normal_age_months": 4,
            "delay_threshold_months": 6
        },
        "sits_without_support": {
            "name": "Sits without support",
            "normal_age_months": 6,
            "delay_threshold_months": 9
        },
        "crawls": {
            "name": "Crawls",
            "normal_age_months": 8,
            "delay_threshold_months": 12
        },
        "stands_with_support": {
            "name": "Stands with support",
            "normal_age_months": 9,
            "delay_threshold_months": 14
        },
        "walks_independently": {
            "name": "Walks independently",
            "normal_age_months": 12,
            "delay_threshold_months": 18
        },
        "runs": {
            "name": "Runs",
            "normal_age_months": 18,
            "delay_threshold_months": 24
        }
    },
    
    "speech": {
        "coos_gurgles": {
            "name": "Coos and gurgles",
            "normal_age_months": 2,
            "delay_threshold_months": 4
        },
        "babbles": {
            "name": "Babbles (ba-ba, ma-ma)",
            "normal_age_months": 6,
            "delay_threshold_months": 10
        },
        "says_first_words": {
            "name": "Says first words",
            "normal_age_months": 12,
            "delay_threshold_months": 18
        },
        "two_word_phrases": {
            "name": "Says 2-word phrases",
            "normal_age_months": 24,
            "delay_threshold_months": 30
        },
        "simple_sentences": {
            "name": "Speaks in simple sentences",
            "normal_age_months": 36,
            "delay_threshold_months": 42
        }
    },
    
    "social": {
        "smiles_at_people": {
            "name": "Smiles at people",
            "normal_age_months": 2,
            "delay_threshold_months": 4
        },
        "laughs": {
            "name": "Laughs",
            "normal_age_months": 4,
            "delay_threshold_months": 6
        },
        "responds_to_name": {
            "name": "Responds to name",
            "normal_age_months": 9,
            "delay_threshold_months": 12
        },
        "plays_peekaboo": {
            "name": "Plays simple games (peek-a-boo)",
            "normal_age_months": 12,
            "delay_threshold_months": 18
        },
        "shows_affection": {
            "name": "Shows affection to familiar people",
            "normal_age_months": 18,
            "delay_threshold_months": 24
        },
        "plays_with_others": {
            "name": "Plays with other children",
            "normal_age_months": 24,
            "delay_threshold_months": 30
        }
    },
    
    "cognitive": {
        "reaches_for_toys": {
            "name": "Reaches for toys",
            "normal_age_months": 4,
            "delay_threshold_months": 6
        },
        "finds_hidden_objects": {
            "name": "Finds hidden objects",
            "normal_age_months": 8,
            "delay_threshold_months": 12
        },
        "points_at_objects": {
            "name": "Points at objects to show interest",
            "normal_age_months": 12,
            "delay_threshold_months": 18
        },
        "sorts_shapes": {
            "name": "Sorts shapes and colors",
            "normal_age_months": 24,
            "delay_threshold_months": 30
        },
        "understands_counting": {
            "name": "Understands counting",
            "normal_age_months": 36,
            "delay_threshold_months": 42
        }
    }
}


def check_milestone_status(category, milestone_name, child_age_months, achieved):
    """
    Compare child's milestone with WHO standards
    
    Args:
        category: 'motor', 'speech', 'social', or 'cognitive'
        milestone_name: key from WHO_MILESTONES dict
        child_age_months: child's current age in months
        achieved: True if child has achieved this milestone
        
    Returns:
        risk_level: 'normal', 'mild_delay', 'high_risk', 'achieved_late', 'too_early'
    """
    
    # Get the milestone standard
    standard = WHO_MILESTONES.get(category, {}).get(milestone_name)
    
    if not standard:
        return "unknown"
    
    normal_age = standard["normal_age_months"]
    delay_threshold = standard["delay_threshold_months"]
    
    if achieved:
        # Child HAS achieved the milestone
        if child_age_months <= delay_threshold:
            return "normal"
        else:
            return "achieved_late"
    else:
        # Child has NOT achieved the milestone yet
        if child_age_months < normal_age:
            # Too early to expect this milestone
            return "too_early"
        elif child_age_months < delay_threshold:
            # Mild concern - past normal age but before threshold
            return "mild_delay"
        else:
            # Past delay threshold - high risk
            return "high_risk"


def get_all_milestones():
    """
    Get all available milestones organized by category
    Returns dict with full milestone info
    """
    return WHO_MILESTONES


def get_milestones_for_age(age_months):
    """
    Get recommended milestones to check for a given age
    Returns list of milestones expected around this age
    """
    relevant_milestones = []
    
    for category, milestones in WHO_MILESTONES.items():
        for key, data in milestones.items():
            # Include milestones within ±2 months of normal age
            if abs(data["normal_age_months"] - age_months) <= 2:
                relevant_milestones.append({
                    "category": category,
                    "key": key,
                    "name": data["name"],
                    "normal_age": data["normal_age_months"]
                })
    
    return relevant_milestones


# Test function
if __name__ == "__main__":
    # Test cases
    print("Testing milestone checker...\n")
    
    # Test 1: Normal - 3 month old holds head steady
    result = check_milestone_status("motor", "holds_head_steady", 3, True)
    print(f"Test 1: 3-month-old holds head steady = {result}")
    
    # Test 2: Mild delay - 7 month old not sitting without support
    result = check_milestone_status("motor", "sits_without_support", 7, False)
    print(f"Test 2: 7-month-old not sitting = {result}")
    
    # Test 3: High risk - 10 month old not sitting without support
    result = check_milestone_status("motor", "sits_without_support", 10, False)
    print(f"Test 3: 10-month-old not sitting = {result}")
    
    # Test 4: Too early - 4 month old not walking
    result = check_milestone_status("motor", "walks_independently", 4, False)
    print(f"Test 4: 4-month-old not walking = {result}")
    
    print("\n✓ Milestone checker working!")
