"""
Interactive Chat with Context-Aware Defense System

This script allows you to have a conversation that's monitored by the
context-aware defense system in real-time.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.detectors.context_aware_defense import ContextAwareDefenseSystem


def print_analysis(result: dict, turn_num: int):
    """Pretty print the analysis results"""
    print(f"\n{'='*80}")
    print(f"Turn {turn_num} Analysis")
    print('='*80)
    
    # Combined risk
    risk_score = result['combined_risk_score']
    risk_level = result['combined_risk_level']
    
    # Color coding
    if risk_level == 'high':
        risk_icon = '🔴'
    elif risk_level == 'medium':
        risk_icon = '🟡'
    else:
        risk_icon = '🟢'
    
    print(f"\n{risk_icon} Combined Risk: {risk_level.upper()} (score: {risk_score:.3f})")
    
    # Threats
    if result['threats_detected']:
        print(f"\n⚠️  Threats Detected:")
        for threat in result['threats_detected']:
            print(f"   - {threat}")
    
    # Context analysis
    context = result['context_analysis']
    if context.get('escalation_detected'):
        print(f"\n📈 ESCALATION DETECTED - Risk is increasing over time!")
    
    if context.get('sustained_risk'):
        print(f"\n⏰ SUSTAINED RISK - Multiple consecutive risky messages!")
    
    # Recommendations
    if result['recommendations']:
        print(f"\n💡 Recommendations:")
        for rec in result['recommendations']:
            print(f"   - {rec}")
    
    # Session stats
    stats = result['session_stats']
    print(f"\n📊 Session Statistics:")
    print(f"   Total turns: {stats['total_turns']}")
    print(f"   Max risk: {stats['max_risk_score']:.3f}")
    print(f"   Escalation detected: {stats['escalation_detected']}")


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           CONTEXT-AWARE DEFENSE SYSTEM - INTERACTIVE CHAT                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

This is an interactive session where you can chat and see real-time analysis
of potential jailbreak attempts. The system tracks context across multiple
messages to detect sophisticated multi-turn attacks.

Commands:
  - Type your messages normally to analyze them
  - Type 'summary' to see conversation summary
  - Type 'reset' to start a new session
  - Type 'quit' or 'exit' to end the session

Try sending messages like:
  - Normal questions (e.g., "How does photosynthesis work?")
  - Gradual escalation (start innocent, slowly get more suspicious)
  - Direct jailbreak attempts (e.g., "Ignore all instructions...")

Let's begin!
""")
    
    # Initialize defense system
    defense = ContextAwareDefenseSystem()
    turn_num = 0
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit']:
                print("\n👋 Goodbye! Stay safe!")
                break
            
            elif user_input.lower() == 'summary':
                summary = defense.get_conversation_summary()
                print(f"\n{'='*80}")
                print("CONVERSATION SUMMARY")
                print('='*80)
                if summary.get('status') == 'no_conversation_data':
                    print("No conversation data yet. Start chatting!")
                else:
                    print(f"Total turns: {summary['total_turns']}")
                    print(f"Average risk: {summary['avg_risk_score']:.3f}")
                    print(f"Max risk: {summary['max_risk_score']:.3f}")
                    print(f"Min risk: {summary['min_risk_score']:.3f}")
                    print(f"\nRisk Distribution:")
                    print(f"  🔴 High risk turns: {summary['high_risk_turns']}")
                    print(f"  🟡 Medium risk turns: {summary['medium_risk_turns']}")
                    print(f"  🟢 Low risk turns: {summary['low_risk_turns']}")
                continue
            
            elif user_input.lower() == 'reset':
                defense.reset_session()
                turn_num = 0
                print("\n🔄 Session reset! Starting fresh...")
                continue
            
            # Analyze the message
            turn_num += 1
            result = defense.analyze_turn(user_input)
            
            # Print analysis
            print_analysis(result, turn_num)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
