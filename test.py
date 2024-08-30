from helpers import gemini_processing
from scripts import t_0_gemini_linkedin_keywords
import json

params = json.loads("""
{
    "task_id": "00002",
    "script_id": 0,
    "pusher-channel-name": "private-heppai-container-0",
    "pusher-event-name": "private-heppai-event-00002",
    "content": {
        "company_description": "Design and develop robust, scalable, and high-performance software applications using GoLang. Identify, prioritize, and execute tasks in the software development life cycle. Automate tasks through appropriate tools and scripting. Collaborate with a cross-functional team to define, design, and ship new features and functionalities. Lead the architecture and coding standards efforts, ensuring clean & efficient code. Implement modern best practices and patterns in software development. Mentor junior software engineers, providing guidance and support to foster their growth and development. Conduct code reviews, ensuring coding standards, best practices, and security guidelines are adhered to. Troubleshoot, debug, and upgrade existing software. Stay up-to-date with emerging trends and technologies in software development to continuously improve our products and processes.",
        "job_description": "Bachelor's degree in Computer Science, Engineering, or a related field. Strong background in backend development with clear architecture mindset. Solid understanding of programming principles, financial transaction consistency, and Git version control. Strong understanding of software development life cycle and agile methodologies. Proven experience in designing scalable and maintainable architectures. Excellent problem-solving skills and ability to think analytically. Strong communication and teamwork skills, with the ability to collaborate effectively with cross-functional teams. A passion for mentoring and guiding junior team members. A continuous learner, open to embracing new technologies and development practices. Aspirations to be/become a Team Lead is a pre."
    }
}""")

result = t_0_gemini_linkedin_keywords.run(**params)
