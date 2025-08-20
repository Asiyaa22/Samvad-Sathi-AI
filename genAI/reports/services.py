# services.py
import statistics
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from reports.models import Report
from core.llm import call_llm
from core.prompts import Final_Summary_template

def generate_and_save_final_report(db: Session, interview_attempt_id: str, analysis_list: list):
    """
    Generate a final report from session-level analysis, call the LLM for summary,
    and save the result to the `reports` table.

    :param db: SQLAlchemy session
    :param interview_attempt_id: ID of the interview attempt
    :param analysis_list: List of per-question analysis dicts from the session
    :return: Saved Report ORM object
    """
    if not analysis_list:
        raise ValueError("No analysis data provided")

    # Extract data from each analysis
    questions_list = [analysis["Question"] for analysis in analysis_list]
    answers_list = [analysis["Answer"] for analysis in analysis_list]
    pause_list = [analysis['pause_analysis'] for analysis in analysis_list]
    pace_list = [analysis['pace_analysis'] for analysis in analysis_list]
    communication_list = [analysis['communication_analysis'] for analysis in analysis_list]
    domain_list = [analysis['domain_analysis'] for analysis in analysis_list]

    # Structure for Speech/Sfluency analysis
    Speech_Structure_Fluency = [
        {"pace": i, "pause": j, "communication": k}
        for i, j, k in zip(pace_list, pause_list, communication_list)
    ]

    # Initialize the report object (to be filled)
    report = {
        "Summery": None,
        "knowledge_competence": domain_list,
        "Speech_Structure_Fluency": Speech_Structure_Fluency
    }

    # -------------------------
    # Score aggregation
    # -------------------------
    acc_sum = dou_sum = rel_sum = example_sum = 0
    for domain in domain_list:
        acc_sum += domain["attribute_scores"]["Accuracy"]["score"]
        dou_sum += domain["attribute_scores"]["Depth of Understanding"]["score"]
        example_sum += domain["attribute_scores"]["Examples/Evidence"]["score"]
        rel_sum += domain["attribute_scores"]["Relevance"]["score"]

    clarity_sum = vocabulary_sum = grammar_sum = structure_sum = 0
    for comm in communication_list:
        clarity_sum += comm["clarity"]["score"]
        vocabulary_sum += comm["vocabulary_richness"]["score"]
        grammar_sum += comm["grammar_syntax"]["score"]
        structure_sum += comm["structure_flow"]["score"]

    scores = {
        "knowledge_competence": {
            "Accuracy": acc_sum,
            "Depth of Understanding": dou_sum,
            "Examples/Evidence": example_sum,
            "Relevance": rel_sum
        },
        "Speech_Structure_Fluency": {
            "clarity": clarity_sum,
            "vocabulary_richness": vocabulary_sum,
            "grammar_syntax": grammar_sum,
            "structure_flow": structure_sum
        }
    }

    # -------------------------
    # Detailed aggregation for LLM prompt
    # -------------------------
    knowledge_attributes = {
        'Accuracy': {'scores': [], 'reasons': []},
        'Depth of Understanding': {'scores': [], 'reasons': []},
        'Relevance': {'scores': [], 'reasons': []},
        'Examples/Evidence': {'scores': [], 'reasons': []}
    }

    communication_attributes = {
        'clarity': {'scores': [], 'rationales': [], 'quotes': []},
        'vocabulary_richness': {'scores': [], 'rationales': [], 'quotes': []},
        'grammar_syntax': {'scores': [], 'rationales': [], 'quotes': []},
        'structure_flow': {'scores': [], 'rationales': [], 'quotes': []}
    }

    wpm_values = []
    rushed_pause_percentages = []
    all_knowledge_feedbacks = []

    for entry in analysis_list:
        # Domain aggregation
        domain = entry['domain_analysis']
        for attr, info in domain['attribute_scores'].items():
            knowledge_attributes[attr]['scores'].append(info['score'])
            knowledge_attributes[attr]['reasons'].append(info['reason'])
        all_knowledge_feedbacks.append(domain['overall_feedback'])

        # Communication aggregation
        comm = entry['communication_analysis']
        for category in communication_attributes.keys():
            cat_data = comm[category]
            communication_attributes[category]['scores'].append(cat_data['score'])
            communication_attributes[category]['rationales'].append(cat_data['rationale'])
            communication_attributes[category]['quotes'].extend(cat_data['quotes'])

        # Pace extraction
        pace_str = entry['pace_analysis']
        if "Your average pace:" in pace_str:
            wpm_line = next(line for line in pace_str.split('\n') if "Your average pace:" in line)
            wpm_values.append(float(wpm_line.split(":")[2].split()[0]))

        # Pause extraction
        pause = entry['pause_analysis']
        rushed_pct = float(pause['distribution']['rushed'].strip('%'))
        rushed_pause_percentages.append(rushed_pct)

    # Averages
    avg_wpm = statistics.mean(wpm_values) if wpm_values else 0
    avg_rushed_pause = statistics.mean(rushed_pause_percentages) if rushed_pause_percentages else 0

    # -------------------------
    # Build LLM prompt
    # -------------------------
    knowledge_section = "=== KNOWLEDGE PERFORMANCE ===\nAverage Scores (1-5 scale):\n"
    for attr, data in knowledge_attributes.items():
        avg_score = statistics.mean(data['scores'])
        unique_reasons = set(data['reasons'])
        knowledge_section += f"- {attr}: {avg_score:.1f}\n"
        knowledge_section += f"  Reasons:\n"
        for reason in unique_reasons:
            knowledge_section += f"  • {reason}\n"
        knowledge_section += "\n"

    knowledge_section += "Key Feedback Themes:\n"
    for fb in set(all_knowledge_feedbacks):
        knowledge_section += f"- {fb}\n"

    comm_section = "\n\n=== COMMUNICATION PERFORMANCE ===\nAverage Scores (1-5 scale):\n"
    for category, data in communication_attributes.items():
        avg_score = statistics.mean(data['scores'])
        comm_section += f"- {category.replace('_', ' ').title()}: {avg_score:.1f}\n"

        unique_quotes = set(data['quotes'])
        if unique_quotes:
            comm_section += f"  Example Quotes:\n"
            for quote in list(unique_quotes)[:3]:
                comm_section += f"  • \"{quote}\"\n"

        unique_rationales = set(data['rationales'])
        comm_section += f"  Rationales:\n"
        for rationale in unique_rationales:
            comm_section += f"  • {rationale}\n"
        comm_section += "\n"

    prompt = Final_Summary_template.format(
        knowledge_section=knowledge_section,
        comm_section=comm_section,
        avg_wpm=avg_wpm,
        avg_rushed_pause=avg_rushed_pause
    )

    # -------------------------
    # Call LLM for final summary
    # -------------------------
    Final_Summary = call_llm(prompt, model="gpt-4o")

    # Attach to report dict
    report['Summery'] = {
        "Scores": scores,
        "Final Summary": Final_Summary
    }

    # -------------------------
    # Save to DB
    # -------------------------
    new_report = Report(
        interview_attempt_id=interview_attempt_id,
        summary=report['Summery'],
        details=report,
        created_at=datetime.utcnow()
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report
