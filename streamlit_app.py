import math
import random

import streamlit as st

st.set_page_config(page_title="팩토리얼로 나타내기", page_icon="🎲", layout="centered")

st.title("📘 팩토리얼로 나타내기")

st.markdown(
    "<style> .stButton>button { margin: 0 !important; padding: 0.23rem 0.4rem !important; min-width: 2.2rem !important; border-radius: 0 !important; } .stButton, .css-1lcbmhc, .css-1iyw2u7, div[data-testid='column'], div[data-testid='column'] > div { margin: 0 !important; padding: 0 !important; } .css-1lcbmhc > div { gap: 0 !important; }</style>",
    unsafe_allow_html=True,
)

def go_to_activity2():
    st.session_state.page = "activity2"

def go_to_activity3():
    st.session_state.page = "activity3"

if "example" not in st.session_state:
    n = random.randint(4, 10)
    st.session_state.example = {
        "n": n,
        "r": random.randint(2, n - 1),
    }

n = st.session_state.example["n"]
r = st.session_state.example["r"]

if "page" not in st.session_state:
    st.session_state.page = "activity1"

if st.session_state.page == "activity1":
    st.markdown("---")
    st.header("① 아래 두 수가 각각 무엇을 세는지 생각해보기")
    st.markdown(
        f"<div style='text-align:center; font-size:22px; font-weight:bold; margin-top:24px; margin-bottom:32px;'>학생 {n}명이 있다고 하자.</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div style='font-size:18px; font-weight:bold; margin-bottom:4px; margin-top:12px;'>{n}명 중 {r}명을 줄 세우는 경우의 수는?</div>",
        unsafe_allow_html=True,
    )
    if "selected_n_str" not in st.session_state:
        st.session_state.selected_n_str = ""
    if "selected_r_str" not in st.session_state:
        st.session_state.selected_r_str = ""

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**n 선택**")
        selected_n_str = st.text_input(
            "",
            value=st.session_state.selected_n_str,
            placeholder="2~10",
            key="selected_n_str",
        )
    with col2:
        st.markdown("**r 선택**")
        selected_r_str = st.text_input(
            "",
            value=st.session_state.selected_r_str,
            placeholder=f"2~{n-1}",
            key="selected_r_str",
        )

    selected_n = int(selected_n_str) if selected_n_str.isdigit() else None
    selected_r = int(selected_r_str) if selected_r_str.isdigit() else None

    if selected_n is not None:
        st.session_state.selected_n = selected_n
    else:
        st.session_state.pop("selected_n", None)

    if selected_r is not None:
        st.session_state.selected_r = selected_r
    else:
        st.session_state.pop("selected_r", None)

    if selected_n is not None and selected_r is not None:
        st.write(f"선택: {selected_n} P {selected_r}")
    else:
        st.write("선택: 아직 입력되지 않음")

    if selected_n is not None:
        display_answer = f"{selected_n}!"
    else:
        display_answer = ""

    st.markdown(
        f"<div style='font-size:18px; font-weight:bold; margin-top:16px; margin-bottom:4px;'>{n}명을 줄 세우는 경우의 수는?</div>",
        unsafe_allow_html=True,
    )
    answer_col1, answer_col2 = st.columns([1, 1])
    with answer_col1:
        st.write("")
    with answer_col2:
        if display_answer:
            st.markdown(
                f"<div style='font-size:24px; font-weight:bold; margin-top:0; margin-bottom:8px;'>{display_answer}</div>",
                unsafe_allow_html=True,
            )

    if selected_n is not None and selected_r is not None:
        if selected_n == n and selected_r == r:
            st.button("다음", on_click=go_to_activity2)
        else:
            st.error("입력한 값이 예시와 일치하지 않습니다. 다시 확인해 주세요.")
    else:
        st.info("정답을 입력한 후에 다음으로 넘어갈 수 있습니다.")

elif st.session_state.page == "activity2":
    activity_n = st.session_state.get("selected_n", n)
    activity_r = st.session_state.get("selected_r", r)

    st.markdown("---")
    st.header("② 상황을 조별로 상상해보기")
    st.markdown(
        f"* {activity_n}명이 일렬로 서 있고, 앞의 {activity_r}자리만 보고 경우를 구하려고 합니다."
    )
    st.markdown(
        f"* 뒤에 서 있는 {activity_n - activity_r}명의 순서는 경우의 수에 어떤 영향을 줄까요?"
    )
    if "influence_answer" not in st.session_state:
        st.session_state.influence_answer = ""
    influence_answer = st.radio(
        "이 질문의 답을 선택하세요.",
        ("", "영향을 준다", "영향을 주지 않는다"),
        index=0,
        format_func=lambda x: "선택하세요" if x == "" else x,
        key="influence_answer",
    )
    st.markdown(
        "* 만약 영향을 주지 않는다면 같은 경우의 수가 몇 번씩 세어지는지 설명해보세요."
    )

    answer_text = st.text_area(
        "",
        height=140,
        key="group_thought"
    )

    missing = activity_n - activity_r
    missing_texts = [f"{missing}!", str(math.factorial(missing))]
    normalized_answer = answer_text.replace(" ", "")
    answer_ok = any(token in normalized_answer for token in missing_texts)

    if "activity2_warning" in st.session_state:
        if influence_answer == "영향을 주지 않는다" and answer_ok:
            st.session_state.pop("activity2_warning", None)
        else:
            st.warning(st.session_state.activity2_warning)

    if st.button("다음"):
        if influence_answer == "영향을 주지 않는다" and answer_ok:
            st.session_state.page = "activity3"
            st.session_state.pop("activity2_warning", None)
        else:
            st.session_state.activity2_warning = "다시 확인해 주세요."

elif st.session_state.page == "activity3":
    activity_n = st.session_state.get("selected_n", n)
    activity_r = st.session_state.get("selected_r", r)

    st.markdown("---")
    st.header("nPr을 팩토리얼로 나타내보기")

    numerator = st.session_state.get("activity3_numerator", "")
    denominator = st.session_state.get("activity3_denominator", "")
    display_num = numerator.strip()
    display_den = denominator.strip()

    st.markdown(
        f"<div style='font-size:24px; font-weight:bold; text-align:center; margin-bottom:24px;'>" \
        f"{activity_n}P{activity_r} = " \
        f"<span style='display:inline-block; vertical-align:middle; text-align:center; min-width:160px;'>" \
        f"<div style='border-bottom:2px solid #333; padding:10px 14px;'>{display_num}</div>" \
        f"<div style='padding:10px 14px;'>{display_den}</div>" \
        f"</span>" \
        f"</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.text_input(
            "분자",
            key="activity3_numerator",
            value=numerator,
        )
    with col2:
        st.text_input(
            "분모",
            key="activity3_denominator",
            value=denominator,
        )

    if "activity3_ok" not in st.session_state:
        st.session_state.activity3_ok = False

    if st.button("다음"):
        correct_answer = (
            display_num == f"{activity_n}!" and
            display_den == f"{activity_n - activity_r}!"
        )
        if correct_answer:
            st.session_state.activity3_ok = True
            st.session_state.pop("activity3_warning", None)
        else:
            st.session_state.activity3_ok = False
            st.session_state.activity3_warning = "정답을 다시 확인해 주세요."

    if "activity3_warning" in st.session_state and st.session_state.activity3_warning:
        st.warning(st.session_state.activity3_warning)

    if st.session_state.activity3_ok:
        st.markdown("---")
        st.markdown("### 일반적인 nPr 형태")
        general_num = st.session_state.get("activity3_general_numerator", "")
        general_den = st.session_state.get("activity3_general_denominator", "")
        gen_col1, gen_col2 = st.columns(2)
        with gen_col1:
            st.text_input(
                "일반 분자",
                key="activity3_general_numerator",
                value=general_num,
            )
        with gen_col2:
            st.text_input(
                "일반 분모",
                key="activity3_general_denominator",
                value=general_den,
            )

        general_num = st.session_state.get("activity3_general_numerator", "")
        general_den = st.session_state.get("activity3_general_denominator", "")
        st.markdown(
            f"<div style='margin-top:24px; font-size:24px; font-weight:bold; text-align:center;'>" \
            f"nPr = " \
            f"<span style='display:inline-block; vertical-align:middle; text-align:center; min-width:160px;'>" \
            f"<div style='border-bottom:2px solid #333; padding:10px 14px;'>{general_num}</div>" \
            f"<div style='padding:10px 14px;'>{general_den}</div>" \
            f"</span>" \
            f"</div>",
            unsafe_allow_html=True,
        )
