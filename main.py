import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"

st.set_page_config(page_title="University SOP Generator", layout="wide")

st.title("University Statement of Purpose (SOP) Generator")

# User inputs
st.subheader("Please provide the following information:")
name = st.text_input("Your Full Name")
university_name = st.text_input("University Name")
program = st.text_input("Program You're Applying To")
inspiring_anecdote = st.text_area("An anecdote that inspired you to take up this course")
academic_background = st.text_area("Academic Background (include college name, course, subjects, projects, internships)")
professional_experience = st.text_area("Professional Experience (if any)")
why_masters = st.text_area("Why do you want to pursue this Masters program and why now?")
short_term_goals = st.text_area("Short-term Career Goals (0-5 years after graduation)")
long_term_goals = st.text_area("Long-term Career Goals (10-15 years after graduation)")
university_specifics = st.text_area("Why this specific university? (mention faculty, research areas, curriculum)")
extracurricular_activities = st.text_area("Extracurricular Activities and their impact")
conclusion = st.text_area("Brief conclusion on why you should be accepted")
additional_details = st.text_area("Any additional details you'd like to include")

# Word count input
st.subheader("Desired Word Count")
min_words = st.number_input("Minimum words", min_value=500, max_value=2000, value=800, step=50)
max_words = st.number_input("Maximum words", min_value=500, max_value=2000, value=1000, step=50)

if min_words >= max_words:
    st.error("Minimum word count must be less than maximum word count.")

# Generate SOP button
if st.button("Generate SOP"):
    if not all([name, university_name, program, inspiring_anecdote, academic_background, why_masters, short_term_goals, long_term_goals, university_specifics]):
        st.error("Please fill in all required fields before generating the SOP.")
    elif min_words >= max_words:
        st.error("Please adjust the word count range.")
    else:
        # LLM setup
        llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0.7)

        # Prompt template
        template = """
        Create a compelling and well-structured Statement of Purpose (SOP) essay for {name}'s application to the {program} program at {university_name}. The essay MUST be between {min_words} and {max_words} words. Use the following information to craft a cohesive narrative:

        - Inspiring anecdote: {inspiring_anecdote}
        - Academic background: {academic_background}
        - Professional experience: {professional_experience}
        - Motivation for Masters: {why_masters}
        - Short-term career goals: {short_term_goals}
        - Long-term career goals: {long_term_goals}
        - Reasons for choosing this university: {university_specifics}
        - Extracurricular activities: {extracurricular_activities}
        - Conclusion: {conclusion}
        - Additional details: {additional_details}

        Write a comprehensive, flowing essay that incorporates all the provided information seamlessly. The essay should not be divided into sections or have any question-like structures. Instead, it should read as a single, coherent narrative that naturally progresses through the applicant's journey, motivations, and aspirations.

        Begin with the inspiring anecdote and use it to transition into the applicant's academic and professional background. Weave in their motivations for pursuing this specific Masters program, connecting it to their past experiences and future goals. Discuss both short-term and long-term career objectives, showing how they align with the program and the university's offerings.

        Highlight the reasons for choosing this particular university, mentioning specific faculty, research areas, or curriculum aspects that appeal to the applicant. Incorporate information about extracurricular activities and their impact, demonstrating a well-rounded personality.

        Throughout the essay, maintain a tone that is professional yet personal, showcasing the applicant's passion for the field and readiness for graduate study. Conclude by summarizing the key points and reinforcing why the applicant is an excellent fit for the program.

        IMPORTANT: The final SOP MUST be between {min_words} and {max_words} words. Craft a cohesive narrative that fits within this word count while covering all key information provided.
        """

        prompt = PromptTemplate(
            input_variables=["name", "university_name", "program", "inspiring_anecdote", "academic_background", "professional_experience", "why_masters", "short_term_goals", "long_term_goals", "university_specifics", "extracurricular_activities", "conclusion", "additional_details", "min_words", "max_words"],
            template=template
        )

        # Create and run the chain
        chain = prompt | llm | StrOutputParser()
        
        with st.spinner(f"Generating SOP ({min_words}-{max_words} words)... This may take a minute."):
            sop = chain.invoke({
                "name": name,
                "university_name": university_name,
                "program": program,
                "inspiring_anecdote": inspiring_anecdote,
                "academic_background": academic_background,
                "professional_experience": professional_experience,
                "why_masters": why_masters,
                "short_term_goals": short_term_goals,
                "long_term_goals": long_term_goals,
                "university_specifics": university_specifics,
                "extracurricular_activities": extracurricular_activities,
                "conclusion": conclusion,
                "additional_details": additional_details,
                "min_words": min_words,
                "max_words": max_words
            })

            # Check word count and regenerate if necessary
            word_count = len(sop.split())
            attempts = 0
            while (word_count < min_words or word_count > max_words) and attempts < 3:
                if word_count < min_words:
                    template += f"\nThe previous essay was too short. Please expand on the content to reach at least {min_words} words while maintaining a cohesive narrative."
                elif word_count > max_words:
                    template += f"\nThe previous essay was too long. Please condense the content to stay under {max_words} words while maintaining all key points and a flowing narrative."
                
                prompt = PromptTemplate(
                    input_variables=["name", "university_name", "program", "inspiring_anecdote", "academic_background", "professional_experience", "why_masters", "short_term_goals", "long_term_goals", "university_specifics", "extracurricular_activities", "conclusion", "additional_details", "min_words", "max_words"],
                    template=template
                )
                chain = prompt | llm | StrOutputParser()
                sop = chain.invoke({
                    "name": name,
                    "university_name": university_name,
                    "program": program,
                    "inspiring_anecdote": inspiring_anecdote,
                    "academic_background": academic_background,
                    "professional_experience": professional_experience,
                    "why_masters": why_masters,
                    "short_term_goals": short_term_goals,
                    "long_term_goals": long_term_goals,
                    "university_specifics": university_specifics,
                    "extracurricular_activities": extracurricular_activities,
                    "conclusion": conclusion,
                    "additional_details": additional_details,
                    "min_words": min_words,
                    "max_words": max_words
                })
                word_count = len(sop.split())
                attempts += 1

        # Display the generated SOP
        st.subheader("Generated Statement of Purpose (SOP)")
        st.markdown(sop)

        # Word count display
        st.info(f"Word count: {word_count}")

        # Download button for the SOP
        st.download_button(
            label="Download SOP as Text",
            data=sop,
            file_name=f"{name}_{university_name}_{program}_SOP.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown("Created with Streamlit and OpenAI")
