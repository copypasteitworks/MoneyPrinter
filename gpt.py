import re
import json
import g4f
from typing import Tuple, List  
from termcolor import colored


def generate_script(video_subject: str) -> str:
    """
    Generate a script for a video, depending on the subject of the video.

    Args:
        video_subject (str): The subject of the video.

    Returns:
        str: The script for the video.
    """

    # Build prompt
    prompt = f"""
    Video Subject: {video_subject}

    Craft a compelling script tailored to the specific subject of this video. Ensure the narrative is succinct yet impactful, designed to captivate and engage your audience from the first moment. The script should weave a coherent story or present information directly related to the video's subject, captivating viewers' attention and encouraging them to watch till the end.

    Your script must:
    - Begin with a strong hook that immediately grabs the viewer's attention.
    - Clearly convey the main message or story related to the video's subject in a concise manner.
    - Include a very short and memorable closing sentence that leaves a lasting impression or calls the viewer to action.

    Please adhere to the following guidelines:
    1. The script is to be returned as a string. Here is an example of a string: "This is an example string."
    2. The script HAS TO BE between 50 to 120 words, optimal for short form video content. NEVER more then 200!
    3. Avoid introductory phrases such as 'welcome to this video' to maintain immediacy and relevance.
    4. Present the script content as direct narration without indicating 'voiceover' or 'narrator' cues.
    5. Do not under any circumstance reference this prompt in your response.
    6. YOU MUST ONLY RETURN THE RAW CONTENT OF THE SCRIPT. 
    7. DO NOT INCLUDE "VOICEOVER", "NARRATOR" OR SIMILAR INDICATORS OF WHAT SHOULD BE SPOKEN AT THE BEGINNING OF EACH PARAGRAPH OR LINE.
    8. DO NOT include the Video Subject ({video_subject}) in the script.
    
    Strategize and think step by step ensuring to ONLY RETURNING THE RAW CONTENT OF THE SCRIPT within the word limit. I will tip you greatly for following the instructions carefully and creating a high-quality script.
    """

    # Generate script
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[{"role": "user", "content": prompt}],
    )

    print(colored(response, "cyan"))

    # Return the generated script
    if response:
        # Clean the script
        # Remove asterisks, hashes
        response = response.replace("*", "")
        response = response.replace("#", "")

        # Remove markdown syntax
        response = re.sub(r'\[.*\]', '', response)
        response = re.sub(r'\(.*\)', '', response)

        return f"{response} "
    print(colored("[-] GPT returned an empty response.", "red"))
    return None


def get_search_terms(video_subject: str, amount: int, script: str) -> List[str]:
    """
    Generate a JSON-Array of search terms for stock videos,
    depending on the subject of a video.

    Args:
        video_subject (str): The subject of the video.
        amount (int): The amount of search terms to generate.
        script (str): The script of the video.

    Returns:
        List[str]: The search terms for the video subject.
    """

    # Build prompt
    prompt = f"""
    Based on the video subject '{video_subject}', generate {amount} relevant search terms. 
    These terms should be closely related to the subject and concise (1-3 words each). 
    Consider the script for context but focus on the subject. 
    
    The search terms are to be returned as
    a JSON-Array of strings.

    Each search term should consist of 1-4 words, ensuring the search terms are distinct.
    
    YOU MUST ONLY RETURN THE JSON-ARRAY OF STRINGS.
    YOU MUST NOT RETURN ANYTHING ELSE. 
    YOU MUST NOT RETURN THE SCRIPT.
    
    The search terms must be related to the subject of the video.
    Here is an example of a JSON-Array of strings:
    ["search term 1", "search term 2", "search term 3"]

    
     Constraints:
    - Include the video subject in most search terms.
    - Ensure terms are concise and directly related to the video content.
    - Output format: JSON array of strings, e.g., ["term1", "term2"].
    
    Example:
    If the video subject is 'wildlife conservation' and the script mentions 'tigers', 'national parks', and 'conservation efforts', appropriate search terms could be ["wildlife conservation", "tiger conservation", "national parks"].
    
    For context, here is the full text:
    {script}
    
    
    Strategize and think step by step ensuring to JSON-ARRAY OF STRINGS. I will tip you greatly for following the instructions carefully and creating a high-quality output.
    """

    # Generate search terms
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[{"role": "user", "content": prompt}],
    )

    # Load response into JSON-Array
    try:
        search_terms = json.loads(response)
    except Exception:
        print(colored("[*] GPT returned an unformatted response. Attempting to clean...", "yellow"))

        # Use Regex to extract the array from the markdown
        search_terms = re.findall(r'\[.*\]', str(response))

        if not search_terms:
            print(colored("[-] Could not parse response.", "red"))

        # Load the array into a JSON-Array
        search_terms = json.loads(search_terms)

    # Let user know
    print(colored(f"\nGenerated {amount} search terms: {', '.join(search_terms)}", "cyan"))

    # Return search terms
    return search_terms

def generate_metadata(video_subject: str, script: str) -> Tuple[str, str, List[str]]:  
    """  
    Generate metadata for a YouTube video, including the title, description, and keywords.  
  
    Args:  
        video_subject (str): The subject of the video.  
        script (str): The script of the video.  
  
    Returns:  
        Tuple[str, str, List[str]]: The title, description, and keywords for the video.  
    """  
  
    # Build prompt for title  
    title_prompt = f"""  
    Generate a catchy and SEO-friendly title for a YouTube shorts video about {video_subject}.  
    """  
  
    # Generate title  
    title_response = g4f.ChatCompletion.create(  
        model=g4f.models.gpt_35_turbo_16k_0613,  
        messages=[{"role": "user", "content": title_prompt}],  
    )  
  
    # Extract title from response  
    title = title_response.strip()  # Assuming title_response is a string  
  
    # Build prompt for description  
    description_prompt = f"""  
    Write a brief and engaging description for a YouTube shorts video about {video_subject}.  
    The video is based on the following script:  
    {script}  
    """  
  
    # Generate description  
    description_response = g4f.ChatCompletion.create(  
        model=g4f.models.gpt_35_turbo_16k_0613,  
        messages=[{"role": "user", "content": description_prompt}],  
    )  
  
    # Extract description from response  
    description = description_response.strip()  # Assuming description_response is a string  
  
    # Generate keywords  
    keywords = get_search_terms(video_subject, 6, script)  # Assuming you want 6 keywords  
  
    return title, description, keywords  