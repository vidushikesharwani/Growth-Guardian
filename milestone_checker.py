"""
WHO Milestone Standards & Risk Assessment
Based on CDC & WHO developmental milestones
"""

# WHO Standard Milestones (age in months)
MILESTONE_STANDARDS = {
    "Motor": {
        "Holds head steady": {"min": 2, "max": 4, "typical": 3},
        "Sits without support": {"min": 4, "max": 8, "typical": 6},
        "Crawls": {"min": 6, "max": 10, "typical": 8},
        "Pulls to stand": {"min": 7, "max": 12, "typical": 9},
        "Walks independently": {"min": 9, "max": 18, "typical": 12},
        "Runs": {"min": 13, "max": 24, "typical": 18},
        "Jumps": {"min": 16, "max": 30, "typical": 24},
    },
    "Speech": {
        "Coos and babbles": {"min": 2, "max": 6, "typical": 4},
        "Says first words": {"min": 10, "max": 15, "typical": 12},
        "Says 2-word phrases": {"min": 16, "max": 24, "typical": 20},
        "Says simple sentences": {"min": 24, "max": 36, "typical": 30},
        "Tells stories": {"min": 36, "max": 48, "typical": 42},
    },
    "Social": {
        "Smiles at people": {"min": 1, "max": 3, "typical": 2},
        "Recognizes familiar faces": {"min": 3, "max": 6, "typical": 4},
        "Shows affection": {"min": 6, "max": 12, "typical": 9},
        "Plays with other children": {"min": 18, "max": 30, "typical": 24},
        "Shows independence": {"min": 24, "max": 36, "typical": 30},
    },
    "Cognitive": {
        "Follows moving objects": {"min": 2, "max": 4, "typical": 3},
        "Recognizes familiar objects": {"min": 6, "max": 10, "typical": 8},
        "Points at objects": {"min": 9, "max": 15, "typical": 12},
        "Sorts shapes and colors": {"min": 18, "max": 30, "typical": 24},
        "Understands time concepts": {"min": 30, "max": 42, "typical": 36},
    }
}


def check_milestone_status(category, milestone_name, child_age_months, achieved):
    """
    Check if milestone achievement is on track, delayed, or at risk
    
    Returns: "on_track", "mild_delay", or "high_risk"
    """
    
    # If achieved, check if within normal range
    if achieved:
        return "on_track"
    
    # If NOT achieved, check against standards
    if category not in MILESTONE_STANDARDS:
        return "unknown"
    
    if milestone_name not in MILESTONE_STANDARDS[category]:
        return "unknown"
    
    standard = MILESTONE_STANDARDS[category][milestone_name]
    
    # High risk: Child is past maximum expected age
    if child_age_months > standard["max"]:
        return "high_risk"
    
    # Mild delay: Child is past typical age but before max
    if child_age_months > standard["typical"]:
        return "mild_delay"
    
    # Still within normal range
    return "on_track"


def get_milestones_for_age(age_months):
    """
    Get expected milestones for a given age
    Returns list of milestones the child should be working on
    """
    expected = []
    
    for category, milestones in MILESTONE_STANDARDS.items():
        for milestone_name, ages in milestones.items():
            # Include if child's age is within the range
            if ages["min"] <= age_months <= ages["max"] + 6:  # +6 months buffer
                expected.append({
                    "category": category,
                    "milestone": milestone_name,
                    "typical_age": ages["typical"],
                    "max_age": ages["max"],
                    "status": "expected" if age_months <= ages["typical"] else "overdue"
                })
    
    return expected


def get_all_milestones():
    """Get all available milestones"""
    all_milestones = []
    
    for category, milestones in MILESTONE_STANDARDS.items():
        for milestone_name, ages in milestones.items():
            all_milestones.append({
                "category": category,
                "name": milestone_name,
                "typical_age": ages["typical"],
                "min_age": ages["min"],
                "max_age": ages["max"]
            })
    
    return all_milestones


def get_risk_assessment(child_milestones, child_age_months):
    """
    Analyze all milestones for a child and provide risk assessment
    
    Args:
        child_milestones: List of milestone records from database
        child_age_months: Current age of child in months
        
    Returns:
        dict with overall_risk, concerns, and recommendations
    """
    high_risk_count = 0
    mild_delay_count = 0
    concerns = []
    
    # Check each category
    for category in MILESTONE_STANDARDS.keys():
        category_milestones = [m for m in child_milestones if m['category'] == category]
        
        # Count delays in this category
        category_high_risk = len([m for m in category_milestones if m.get('risk_level') == 'high_risk'])
        category_mild_delay = len([m for m in category_milestones if m.get('risk_level') == 'mild_delay'])
        
        high_risk_count += category_high_risk
        mild_delay_count += category_mild_delay
        
        if category_high_risk > 0:
            concerns.append(f"⚠️ {category_high_risk} high-risk delays in {category}")
        elif category_mild_delay > 0:
            concerns.append(f"⚡ {category_mild_delay} mild delays in {category}")
    
    # Overall assessment
    if high_risk_count >= 2:
        overall_risk = "high"
        recommendation = "🚨 URGENT: Consult pediatrician immediately for developmental screening"
    elif high_risk_count == 1:
        overall_risk = "medium"
        recommendation = "⚠️ Schedule pediatrician visit within 2 weeks"
    elif mild_delay_count >= 3:
        overall_risk = "medium"
        recommendation = "📋 Monitor closely and discuss with pediatrician at next visit"
    elif mild_delay_count >= 1:
        overall_risk = "low"
        recommendation = "📊 Continue monitoring, mention to pediatrician"
    else:
        overall_risk = "none"
        recommendation = "✅ Development appears on track!"
    
    return {
        "overall_risk": overall_risk,
        "high_risk_count": high_risk_count,
        "mild_delay_count": mild_delay_count,
        "concerns": concerns,
        "recommendation": recommendation
    }