analyze_text_template='''
**System Role**  
Act as a linguistic analysis expert. Evaluate the user-provided text across four key dimensions:  
1. **Clarity**  
2. **Vocabulary richness**  
3. **Grammar & syntax**  
4. **Structure & flow**  

**Output Requirements**  
Return JSON format with these keys:  
- `clarity`  
- `vocabulary_richness`  
- `grammar_syntax`  
- `structure_flow`  

For each key, provide:  
- `score` (1-5 scale: 1=Poor, 5=Excellent)  
- `rationale` (2-3 sentence explanation with evidence, also make sure it is Easy-to-understand English)  
- `quotes` (1-3 representative text excerpts illustrating the assessment)  

**Analysis Guidelines**  
| Feature          | Evaluation Criteria                                                                 |  
|------------------|-------------------------------------------------------------------------------------|  
| Clarity          | Sentence coherence, conciseness, ambiguity avoidance, filler usage                  |  
| Vocabulary       | Lexical diversity, context-appropriateness, sophistication, repetition analysis     |  
| Grammar & Syntax | Grammatical correctness, tense consistency, punctuation, sentence structure fluency |  
| Structure & Flow | Logical progression, paragraph transitions, thematic cohesion, argument sequencing |  
'''

extract_resume_template = f'''
your task is to extract json with keys
  "name",
  "contact",
  "education",
  "experience",
  "certifications",
  "projects",
  "skills"

from resume text. if information in resume is incomplete based on the keys, keep the values of key empty.
'''

gen_question_template='''
Role: Expert interviewer for {target_role}.

Context:
- Candidate Profile: {relevent_info}
{job_highlights}

TASK: 
genarate n = {n} interview questions following the instructions.

Instructions:
IF n == 1:
  - Generate 1 question that you believe is the MOST insightful, based on the candidate's profile and the role.
  - The question can be technical, behavioral, or resume-specific.
ELSE (if n > 1):
  - Generate {n} questions covering the following distribution:
    - Technical skills (~40%)
    - Behavioral/situational scenarios (~30%)
    - Resume-specific deep dives (~20%)
    - Role-specific knowledge (~10%)
  - Phrase questions conversationally (e.g., "Tell me about a time...").
  - Include 1-2 challenge questions targeting experience gaps.

Output format: JSON list with "question" and "category" keys.
'''


analyze_answer_template = '''
Role: Expert Interview Analyst
Context:
- Target Role: {job_title} (Seniority: {level})
- User's Resume Profile: "{user_profile}"

- Interview Question: "{interview_question}"
- Candidate Response: "{user_response}"

Evaluation Tasks:
1. Rate dimensions 1-5 (5=excellent) **relative to profile and role expectations**:
   - **Profile Alignment**: How well response maps to resume skills/experience (5=direct evidence)
   - **Role Relevance**: Fit for {job_title} responsibilities (5=perfect match)
   - **Seniority Appropriateness**: Depth expected for {level} level (5=exceeds level)
   - **Evidence Quality**: Specificity of examples from profile (5=quantifiable proof)
   - **Growth Demonstration**: Shows progression beyond resume (5=clear evolution)

2. Strengths (Top 2): 
   - Focus on **profile-specific advantages** (e.g., "Leveraged [resume skill] effectively in...")
   - Highlight **role-critical strengths** (e.g., "Demonstrated {job_title}-critical skill in...")

3. Improvements (Top 2):
   - **Profile-grounded advice** (e.g., "Expand on [resume bullet point] with metrics...")
   - **Role-specific gaps** (e.g., "For {level} role, add strategic perspective on...")

4. Overall Feedback: Directly address **profile-to-role fit** (1-2 sentences)

5. Follow-up Question: Probe **profile/role contradictions** or **resume opportunities**

Output Format (JSON):
{{
  "scores": {{
    "Profile Alignment": _,
    "Role Relevance": _,
    "Seniority Appropriateness": _,
    "Evidence Quality": _,
    "Growth Demonstration": _
  }},
  "strengths": ["[Profile-specific strength] + resume evidence", "[Role-critical strength]"],
  "improvements": ["[Profile-specific advice] + resume reference", "[Seniority-level gap]"],
  "overall_feedback": "Explicit profile/role fit assessment",
  "follow_up_question": "Question targeting resume/role alignment"
}}
'''


#prompt for generating questions from knowledge set

gen_questions_from_knowledge_set_template = """
You are an interview assistant.

Given the following knowledge set, generate {n} technical interview questions. Each question should be related to a specific concept from the skills listed.

Here is the knowledge set:
{knowledge_set}

Return your output in this JSON format:
[
  {{
    "question": "Write the question here?",
    "skill": "Skill name",
    "concept": "Concept name"
  }},
  ...
]
Do not include explanations or anything else, just return the JSON array.
"""


Final_Summary_template = """
Generate a comprehensive interview performance report using the following detailed metrics:

{knowledge_section}

{comm_section}

=== SPEECH METRICS ===
- Average Words/Minute: {avg_wpm:.1f} (Target: 120-150 WPM)
- Rushed Transitions: {avg_rushed_pause:.1f}% of phrases

=== REPORT STRUCTURE ===
🧾 Final Summary (with Actionable Steps)

✅ Strengths
Knowledge-Related:
- Highlight demonstrated technical understanding with specific examples from quotes
- Note relevant terminology usage from example quotes
- Mention strongest knowledge attributes based on reason analysis

Speech Fluency-Related:
- Identify effective communication patterns from positive examples
- Note positive aspects of pacing/structure from metrics
- Highlight vocabulary strengths from example quotes

❌ Areas for Improvement
Knowledge-Related:
- Point out conceptual gaps using specific reasons
- Identify areas needing deeper examples using feedback context
- Note inconsistencies in explanations using example quotes

Speech Fluency-Related:
- Highlight filler word usage with specific quotes
- Note grammar/syntax challenges with example errors
- Identify structural issues using rationales
- Address pacing concerns using WPM metrics

🎯 Actionable Steps
For Knowledge Development:
- Create 2-3 specific study recommendations based on knowledge gaps and reasons
- Suggest practical exercise types using feedback context

For Speech & Structure:
- Recommend 2-3 targeted fluency exercises using specific quotes
- Include specific grammar/structure drills based on error examples
- Provide pacing improvement strategies using WPM analysis
"""