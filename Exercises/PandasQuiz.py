import streamlit as st
import pandas as pd
import random
import time
import datetime
import requests

plt = False
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    pass


# load question set
df = pd.read_csv("PandasMethods.csv", index_col=0)
n_choices = 7


def new_question():
    assert n_choices>1, "You need at least 1 choice!!!"
    
    # get random section and random samples
    category = random.choice(df["category"].unique())
    choices = df[df['category']==category].sample(n_choices)
    target = choices.sample().iloc[0]

    st.session_state['answer'] = target['method']
    st.session_state['choices'] = [f"{q}" for q in choices['method']]
    st.session_state['time'] = datetime.datetime.now()
    st.session_state['url'] = target['method_url']
    #st.write('Match the pandas method to the following text:')
    #st.write(f"""This is from the {target['section']} of {target['category']}""")
    st.header(target['question'])
    for choice in choices['method']:
        st.button(f'`{choice}`', on_click=check_question, args=(choice,))
    
    

def check_question(choice):
    st.session_state['n_answered'] += 1
    if 'post_url' in st.secrets:
        requests.post(st.secrets['post_url'], data={
            "secret": st.secrets['secret'],
            "question": st.session_state['answer'],
            "answer": choice,
            "delta": (datetime.datetime.now() - st.session_state.time) // datetime.timedelta(microseconds=1),
        })
    answer_link = f"""More info: [{st.session_state['answer']}](https://pandas.pydata.org/pandas-docs/stable/reference/{st.session_state['url']})"""
    if choice == st.session_state['answer']:
        st.session_state['n_correct'] += 1
        st.success(
            f"""CORRECT! {answer_link}""",
            icon="✅",
        )
        if hasattr(st, "baloons"):
            st.baloons()
    else:
        st.error(
            f"""INCORRECT! {answer_link}""",
            icon="❌",
        )
    time.sleep(1)
    return True


# Setup
st.set_page_config(
    page_title="Pandas Methods Quiz",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
columns = list(st.columns((10, 2)))


if "n_answered" not in st.session_state:
    st.session_state['n_answered'] = 0
    st.session_state['n_correct'] = 0


# UI
with columns[0]:
    st.title('🐼 Pandas Methods Quiz 🐼')
    new_question()

with columns[-1]:
    if plt and st.session_state['n_answered'] > 0:
        fig, ax = plt.subplots()
        ax.pie(
            [
                st.session_state['n_correct'],
                st.session_state['n_answered'] - st.session_state['n_correct'],
            ],
            labels=[
                "Correct",
                "Incorrect",
            ],
            colors=[
                "Green",
                "Red",
            ],
        )
        ax.set_facecolor('#00000000')
        fig.set_facecolor('#00000000')
        st.pyplot(fig=fig, clear_figure=None, use_container_width=True)



st.write(":grey[Anonymous usage satistics may be collected.]", align='right')