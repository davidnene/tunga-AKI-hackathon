import streamlit as st
import pandas as pd
import json

from agent import query_agent, create_agent

def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response)


def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)

def main():
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "data" not in st.session_state:
        st.session_state.data = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    st.title("👨‍💻 :blue[Insurance Data Chatbot]")
    st.subheader("""
                 Generating Complex Analytical Insights from insurance data\n  
                 - Saves time used in analytical work by 80%\n
                 - Able to perform complex analysis and generate tables and graphs upon request
                 """)
    st.divider()
    with st.sidebar:
        st.subheader("Data Upload")
        st.session_state.data = st.file_uploader("Upload your Insurance CSV")
        if st.button("Initiate agent"):
            with st.spinner("Initiating.."):
                st.session_state.agent = create_agent(st.session_state.data)
                st.success('Agent successfully initiated!', icon="✅")
        st.divider()
        st.markdown(
            """
                **:blue[Project Contributors]**\n
                David Nene, MSc - Software Engineer | AI


                Derrick Lubanga, MSc - Data Scientist


                Linda Kelida, MSc - Data Engineer

                
                Chepkirui Tonui, MSc - BI Analyst

            """
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["content"] is not None:
                st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        try:
            if not prompt and not st.session_state.data:
                st.warning("Please upload csv and initiate agent", icon='⚠️')
            elif not prompt and st.session_state.data !=None:
                st.warning("Please ask a question", icon='⚠️')
            else:
            # Display user message in chat message container
                st.chat_message("user").markdown(prompt)
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                response = query_agent(agent=st.session_state.agent, query=prompt)
                decoded_response = decode_response(response)
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    write_response(decoded_response)
                # Add assistant response to chat history
                if response == str:
                    st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.write(e.args[0])
            st.warning("Please upload csv and initiate agent", icon='⚠️')
    if st.session_state.messages != []:
        if st.button("Clear chat"):
            st.session_state.messages = []


if __name__ == "__main__":
    main()


