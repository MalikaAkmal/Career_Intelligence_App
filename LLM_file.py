
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_insights_and_roadmap(role_name, tool_name, job_descriptions):
    cleaned_descriptions = []
    for item in job_descriptions:
        if isinstance(item, dict): #it will check whether that is in dict format ,# Normalizes mixed API formats into a uniform list of description text strings
            text = item.get("job_description") or item.get("description") or str(item) 
            cleaned_descriptions.append(text)
        else:
            cleaned_descriptions.append(str(item))

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gemini API key is missing.", "Please set GEMINI_API_KEY in your .env file."

    client = genai.Client(api_key=api_key)
    
    combined_text = "\n\n--- NEXT JOB DESCRIPTION ---\n\n".join(cleaned_descriptions[:10])

    prompt = f"""
    You are an expert tech career analyst and recruiter advisor.
    
    Target Role: {role_name}
    Specific Tool/Skill: {tool_name}

    Task 1: Analyze the provided job descriptions specifically for how '{tool_name}' is used in practice.
    Task 2: Based on these job descriptions AND your broader knowledge of current hiring trends across major job portals (e.g., LinkedIn, Indeed, Glassdoor), estimate the overall market demand percentage for '{tool_name}' in '{role_name}' roles.
    Task 3: Extract 3 to 5 key tasks recruiters explicitly expect candidates to perform using '{tool_name}'.
    Task 4: Provide a 3-step learning roadmap to master this tool for this role.
    Task 5: Also calculate the percentage use of this tool in that field which user entered {role_name}

    Format your output strictly with these exact headers:

    ### Market Verification & Estimated Usage
    * Estimated Cross-Portal Demand Percentage: [Provide an estimated % based on market data]
    * Primary Use Case in Role: [1-2 sentences on how the tool is specifically applied]

    ### Recruiter Task Requirements
    * [Requirement/Task 1]
    * [Requirement/Task 2]
    * [Requirement/Task 3]

    ### Recommended Roadmap
    1. [Step 1]
    2. [Step 2]
    3. [Step 3]

    Job Descriptions mentioning {tool_name}:
    {combined_text[:4000]}
    """

    response = client.models.generate_content(
        model="models/gemini-3.5-flash",
        contents=prompt
    )
    
    output_text = response.text
    
    if "### Recommended Roadmap" in output_text:
        parts = output_text.split("### Recommended Roadmap")
        analysis = parts[0].replace("### Market Verification & Estimated Usage", "").strip()
        roadmap = parts[1].strip()
    else:
        analysis = output_text
        roadmap = "Follow standard practical modules for this tool."

    return analysis, roadmap