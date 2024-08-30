import os
import json
import regex as re
import google.generativeai as genai


from dotenv import load_dotenv
from helpers.logger.logger import logger


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_API_VERSION = os.getenv("GEMINI_API_VERSION")

        
class ProfileEvaluation:
    def __init__(self, jd = "missing description") -> None:
        self.jd = jd
        self.profile_info = ""

    @staticmethod
    def json_format_by_talent_talent_info(fullname, position, talent_info):
        logger.info(f"talent_info: {talent_info}")
        dict_talent_exps = talent_info.get("experience")
        dict_talent_edu = talent_info.get("education")
        dict_talent_skill = talent_info.get("skills")
        dict_talent_languages = talent_info.get("languages")
        if talent_info:
            data_to_dict = {
                "full_name": fullname,
                "position": position,
                "experience": dict_talent_exps if dict_talent_exps else "Not mentioned",
                "skills": dict_talent_skill if dict_talent_skill else "Not mentioned",
                "education": dict_talent_edu if dict_talent_edu else "Not mentioned",
                "languages": dict_talent_languages if dict_talent_languages else "Not mentioned"
            }
            logger.info(data_to_dict)
            return data_to_dict
        else:
            return {}
        
    def set_profile_id(self, fullname, position, talent_info, jd):
        profile_info = ProfileEvaluation.json_format_by_talent_talent_info(fullname, position, talent_info)
        result = ProfileEvaluation.compare_real_profile_with_jd(profile_info, jd)
        json_format_match = re.findall(r'\{(?:[^{}]|(?R))*\}', result, re.DOTALL)
        logger.info(json_format_match[0])
        try:
            json_format_match = json.loads(json_format_match[0]) if len(json_format_match) > 0 else None
        except Exception as e:
            logger.error("json:",e)
        return json_format_match
    
    @staticmethod
    def compare_real_profile_with_jd(profile_info, jd):
        logger.info("compare_real_profile_with_jd")
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
        ]

        model = genai.GenerativeModel(model_name=GEMINI_API_VERSION,
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        conversation = model.start_chat()

        conversation.send_message('''instructions = Based on the given job description below and the given profile, your responsibility is to compare and give me the score on 100 scale.              
                                  For the information not mentioned, don't underrate the matching-score. The reason shpuld include all aspects and wall-explained.
                                  Important note: Do not strongly rely on the mentioned expirence. Do rely on the skills that they might achieve when doing that job. Because not mentioned no not mean not acquired.
        Answer must be structured like this and contain only this structured:
        {
        "overall": "$overall_score",
        "experience": "$experience_score",
        "skills": "$skills_score",
        "languages": "$languages_score",
        "education": "$education_score"              
        }
        Here is the job description: ''' + str(jd) + "Here is the profile:" + str(profile_info))
        logger.info(f"GEMINI: {conversation.last.text}")
        return conversation.last.text
        
    
    def compare_real_profile_with_jd_custom_note(self, note):
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048     
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
        ]

        model = genai.GenerativeModel(model_name=GEMINI_API_VERSION,
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        conversation = model.start_chat()
        
        conversation.send_message('''instructions = Based on the given job description below and the given profile, your responsibility is to compare and give me the score on 100 scale.              
                                  give me overall score of a profile as well as detail score of each evaluation criteria (experience, skills, languages), if criteria is not mentioned then score is 0.
                                  Important note:''' + note +
        '''
        Answer must be structured like this:
        {
        "overall": "$overall_score",
        "detail": {
            "experience": "$experience_score",
            "skills": "$skills_score",
            "languages": "$languages_score"
        }
        }
        Here is the job description: ''' + str(self.jd) + "Here is the profile:" + str(self.profile_info))
        logger.info(f"GEMINI: {conversation.last.text}")
        return conversation.last.text
