

import streamlit as st

def main():
    # Set page layout
    st.set_page_config(layout="wide")

    # Create columns for the logos
    col1, col2 = st.columns([1, 1])

    # Logo in the first column
    with col1:
        st.image("images/Tunga.png", width=150)

    # Second logo in the second column
    with col2:
        st.image("images/strathlogo.png", width=150)  

    st.title("Welcome to Tunga Tech Team")

    st.write("## Team Overview")
    #st.write("Tunga is a dynamic team of Research Scholars from Strathmore University @iLab Africa. We are dedicated to pushing the boundaries of technology, focusing on cutting-edge data science solutions and artificial intelligence. Our team collaborates on innovative projects, leveraging the power of Large Language Models (LLMs) to tackle complex challenges and drive meaningful impact.")


    st.write("""
        <div style="text-align: justify">
            Tunga is a dynamic team of Research Scholars from Strathmore University @iLab Africa. We are dedicated to pushing the boundaries of technology, focusing on cutting-edge data science solutions and artificial intelligence. Our team collaborates on innovative projects, leveraging the power of Large Language Models (LLMs) to tackle complex challenges and drive meaningful impact.Empowering insights.
        </div>
    """, unsafe_allow_html=True)

    
    st.write("## Projects Showcase")
    projects = [
        "1. Medical Drugs Prescription Information Retrieval Optimization with Meditron-70b and Neo4J Knowledge Graphs",
        "2. Optimizing Drug Allocation & Pricing Comparisons Using Data Science Technques",
        "3. Movie Recomender Engine",
        "4. Text-Prompted Video Search: Harnessing AI for Efficient Retrieval"
    ]
    st.write("Some projects we have worked on using LLMs:")
    for project in projects:
        st.write(f"- {project}")

    st.write("## Meet Our Team")

    # Placeholder team members
    team_members = [
        {"name": "David Nene", "image": "images/david.png", "career": "Software Engineer | AI", "degree": "MSc. Data Science and Analytics, Strathmore University"},
        {"name": "Linda Kelida", "image": "images/linda.png", "career": "Machine Learning Engineer", "degree": "MSc. Data Science and Analytics, Strathmore University"},
        {"name": "Derrick Lubanga", "image": "images/derrick.png", "career": "Data Scientist", "degree": "MSc. Data Science and Analytics, Strathmore University"},
        {"name": "Sharon Tonui", "image": "images/sharon.png", "career": "BI Analyst", "degree": "MSc. Data Science and Analytics, Strathmore University"}
    ]

    # Display team members side by side in a row
    cols = st.columns(len(team_members))

    for i, member in enumerate(team_members):
        with cols[i]:
            st.write(f"### {member['name']}")
            st.image(member["image"], caption=f"{member['degree']}", width=200)
            st.write(f"**Profession:** {member['career']}")

if __name__ == "__main__":
    main()
