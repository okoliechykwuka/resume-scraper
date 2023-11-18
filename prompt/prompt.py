


roles_extraction_qa = """
                       Thoroughly review the document to identify any explicitly stated or implied key roles and corresponding criteria required for the project team.
                       Extract and infer the educational, professional qualifications, and experience requirements for each role, even if they are not directly listed. 
                       Please provide this information structured in a JSON format with generic keys such as 'Role', 'EducationalQualifications', 'ProfessionalQualifications', and 'Experience'. 
                       This should reflect both clear and deduced criteria to maintain consistency across document with varying levels of detail.

                       The expected response should look like this, filled with either specified or inferred details as per the document:
                       {
                        "Role1": {
                          "EducationalQualifications": ["List out required or inferred degrees or certifications"],
                          "ProfessionalQualifications": ["List out required or deduced professional credentials"],
                          "Experience": ["Specify listed or deduced years of experience", "Note explicit or relevant industry or project experience"]
                        },
                        "Role2": {
                          "EducationalQualifications": ["List out required or inferred degrees or certifications"],
                          "ProfessionalQualifications": ["List out required or deduced professional credentials"],
                          "Experience": ["Specify listed or deduced years of experience", "Note explicit or relevant industry or project experience"]
                        },
                        // Additional roles should follow the same structure
                      }
                   """
                   

cv_prompt = """
   Create a realistic dummy resume for a specified role based on 'ROLE REQUIREMENTS (RFP)'.

        **INSTRUCTIONS**:
        - Input: Role and requirements in JSON format.
        - Sections: Professional summary, extensive work history, education, certifications, skills/technologies, awards, publications, and other pertinent sections. Include specific achievements and examples in each section.
        - Formatting: Ensure headers, bullet points, and section separation for LaTeX/markdown compatibility. Use clear, professional formatting.
        - Tailoring: Resume content should be specifically tailored to the role, demonstrating how the candidate's experiences and qualifications align with the role requirements.
        - Achievements: Emphasize quantifiable achievements in the professional experience and awards sections, such as percentages, project sizes, budgets handled, or specific outcomes.
        - Personalization: Add details that make the resume unique to the individual, such as specific projects worked on, unique skills or experiences that set the candidate apart.

        **ROLE REQUIREMENTS (RFP)**:
        
        ```{0}```

        **DUMMY RESUME TEMPLATE 1**:
    \`\`\`
     {{
    "basics": {{
        "name": "Okolie Chukwuka",
        "email": "chukypedro15@gmail.com",
        "phone": "+234-9038185240",
        "website": "okoliechykwuka.github.io/portfolio",
        "address": "Greenville Estate, Ijoyin PowerLine, Ajah, Lagos"
    }},
    "education": [
        {{
            "institution": "University of Benin",
            "area": "Physics",
            "additionalAreas": [],
            "studyType": "Bachelor's degree",
            "startDate": "September 2012",
            "endDate": "October 2016",
            "score": "",
            "location": ""
        }},
        {{
            "institution": "National Youth Service Corps",
            "area": "",
            "additionalAreas": [],
            "studyType": "Discharge Certificate",
            "startDate": "June 2019",
            "endDate": "May 2020",
            "score": "",
            "location": ""
        }}
    ],
    "awards": [
        {{
            "title": "Data Analysis with Python - Jovian.ai",
            "date": "October 2021",
            "awarder": "Jovian.ai",
            "summary": "Completed the Data Analysis with Python course"
        }},
        {{
            "title": "Machine Learning with Python: Zero to GBMs",
            "date": "January 2021",
            "awarder": "Udemy",
            "summary": "Completed the Machine Learning with Python course"
        }},
        {{
            "title": "Deep Learning with PyTorch: Zero to GANs",
            "date": "March 2021",
            "awarder": "Udemy",
            "summary": "Completed the Deep Learning with PyTorch course"
        }},
        {{
            "title": "Build Better Generative Adversarial Networks (GANs)",
            "date": "April 2021",
            "awarder": "Udemy",
            "summary": "Completed the Build Better Generative Adversarial Networks course"
        }},
        {{
            "title": "AI for Medical Diagnosis (Coursera)",
            "date": "May 2021",
            "awarder": "Coursera",
            "summary": "Completed the AI for Medical Diagnosis course"
        }}
    ],
    "projects": [
        {{
            "name": "AI Application for Text Document Analysis",
            "description": "Developed AI application using LLM for extracting insights, summarizing, and performing calculations on large text documents.",
            "keywords": [
                "AI",
                "LLM",
                "text document analysis"
            ],
            "url": ""
        }},
        {{
            "name": "Chatbot Development using ChatGPT API",
            "description": "Created chatbot using ChatGPT API for effective user communication.",
            "keywords": [
                "Chatbot",
                "ChatGPT API",
                "user communication"
            ],
            "url": ""
        }},
        {{
            "name": "Deep Learning Framework for Malware Classification",
            "description": "Designed and implemented deep learning framework for malware classification.",
            "keywords": [
                "Deep learning",
                "malware classification"
            ],
            "url": ""
        }},
        {{
            "name": "Machine Learning and Deep Learning Custom Applications",
            "description": "Developed customized machine learning and deep learning applications for clients.",
            "keywords": [
                "Machine learning",
                "deep learning",
                "custom applications"
            ],
            "url": ""
        }},
        {{
            "name": "Face Recognition System for Nigerian Borders",
            "description": "Led ML Engineers in developing Face Recognition System with 99.7% accuracy for validating migrants at Nigerian borders.",
            "keywords": [
                "Face Recognition System",
                "migrants validation",
                "Nigerian borders"
            ],
            "url": ""
        }},
        {{
            "name": "AI Credit System Development",
            "description": "Contributed to the development of AI credit system (DECIDE) for informed credit decisions.",
            "keywords": [
                "AI credit system",
                "DECIDE",
                "credit decisions"
            ],
            "url": ""
        }},
        {{
            "name": "Credit Risk and Machine Learning Models",
            "description": "Built credit risk and machine learning models for banking and non-banking establishments.",
            "keywords": [
                "Credit risk models",
                "machine learning models",
                "banking",
                "non-banking"
            ],
            "url": ""
        }},
        {{
            "name": "AI Solution for Farms",
            "description": "Designed AI solution for generating insights for farms using image processing and deep learning.",
            "keywords": [
            "AI solution",
            "farms",
            "image processing",
            "deep learning"
            ],
            "url": ""
        }},
        {{
            "name": "Mobile Data Analysis",
            "description": "Interpreted data to derive actionable insights for executive decision-making.",
            "keywords": [
            "Mobile data analysis",
            "actionable insights",
            "executive decision-making"
            ],
            "url": ""
        }}
            ],
            "skills": [
        {{
            "name": "Machine Learning",
            "keywords": [
            "AI application",
            "LLM",
            "deep learning framework",
            "customized machine learning"
            ]
        }},
        {{
            "name": "Software Development",
            "keywords": [
            "chatbot",
            "Python",
            "AI microservices",
            "software developer"
            ]
        }},
        {{
            "name": "Data Analysis",
            "keywords": [
            "data scraping",
            "data mining",
            "data visualization",
            "data validation"
            ]
        }},
        {{
            "name": "Deep Learning",
            "keywords": [
            "image processing",
            "AI models integration",
            "crop yield detection",
            "disease detection"
            ]
        }}
            ],
            "work": [
        {{
            "company": "Fiverr",
            "position": "Machine Learning Engineer | Data Scientist",
            "startDate": "January 2019",
            "endDate": "Present",
            "location": "",
            "highlights": [
            "Developed AI application using LLM for extracting insights, summarizing, and performing calculations on large text documents.",
            "Created chatbot using ChatGPT API for effective user communication.",
            "Designed and implemented deep learning framework for malware classification.",
            "Gathered and analyzed data through data scraping and mining techniques.",
            "Developed customized machine learning and deep learning applications for clients.",
            "Achieved high client satisfaction with growing client base and positive feedback."
            ]
        }},
        {{
            "company": "Goldaris Technology",
            "position": "Lead Machine Learning Engineer",
            "startDate": "January 2022",
            "endDate": "March 2023",
            "location": "",
            "highlights": [
            "Guided 8+ immigration officers to improve their proficiency in Python, Data Structures, and Algorithms.",
            "Led ML Engineers in developing Face Recognition System with 99.7% accuracy for validating migrants at Nigerian borders.",
            "Supervised AI microservices operations and established real-time pipeline for monitoring machine learning model performance."
            ]
        }},
        {{
            "company": "Indicina",
            "position": "Machine Learning Engineer and Software Developer",
            "startDate": "January 2021",
            "endDate": "July 2021",
            "location": "",
            "highlights": [
            "Contributed to the development of AI credit system (DECIDE) for informed credit decisions.",
            "Built credit risk and machine learning models for banking and non-banking establishments.",
            "Conducted data mining, analysis, visualization, and trained machine learning models.",
            "Elevated digital lending engine by 45%, increasing profits and customer retention."
            ]
        }},
        {{
            "company": "AirSmat",
            "position": "AI Engineer and Software Developer",
            "startDate": "January 2020",
            "endDate": "November 2020",
            "location": "",
            "highlights": [
            "Designed AI solution for generating insights for farms using image processing and deep learning.",
            "Integrated AI models into drone-powered software for crop yield, weed, and disease detection."
            ]
        }},
        {{
            "company": "Great Brand Nigeria Limited",
            "position": "Mobile Analyst",
            "startDate": "November 2017",
            "endDate": "May 2019",
            "location": "",
            "highlights": [
            "Interpreted data to derive actionable insights for executive decision-making.",
            "Developed visualizations and charts to illustrate key insights and trends.",
            "Utilized statistical techniques for hypothesis testing and data validation."
            ]
        }}
            ]
            }}
         
    \`\`\`

    Fill each section with realistic and tailored content for the specified role, creating a comprehensive and convincing resume. If no role is specified in the document, do not generate a resume.
    Note: Add a lot of work history and ensure that all the filled information are realistic and valid(pick realistic names that exist in the real world).
    Always Use Random name for the candidate different from **Jessica Claire**
        
"""
