import streamlit as st
import google.genai as genai

# 1. Gemini 설정 (Secrets에서 키를 가져옴)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Streamlit Secrets에 GOOGLE_API_KEY를 등록해 주세요!")

st.set_page_config(page_title="네오소프트뱅크 AI 가이드", page_icon="🏥")

# 2. 이미지 주소 설정
MY_ID = "kjw10won-crypto"
MY_REPO = "chatbot"
IMG_BASE = f"https://raw.githubusercontent.com/{MY_ID}/{MY_REPO}/main/"

# 3. 응답 템플릿 정의
RESPONSE_TEMPLATES = {
    "접수": """
### 🩺 당일 진료 접수 방법

**주요 절차:** 환자 조회 → 접수 버튼 클릭 → 진료실 지정 → 확인

**상세 절차:**

1️⃣ **환자 조회**
   - 메인 화면 상단 검색창에서 **환자 성명** 또는 **차트 번호** 입력
   - 검색 결과에서 해당 환자 선택 (더블 클릭)

2️⃣ **상세 정보 확인**
   - 환자의 상세 정보가 화면에 나타남

3️⃣ **접수 버튼 클릭**
   - 화면 하단의 **[접수]** 버튼 클릭

4️⃣ **진료실 선택**
   - 팝업창에서 진료를 받을 **진료실(원장님)** 선택
   - **확인** 버튼 클릭하면 접수 완료 ✅

> 📞 문제 발생 시 담당자에게 문의하세요.
""",
    "취소": """
### ❌ 접수 취소 방법

**주요 절차:** 접수 현황판 확인 → 환자 선택 → 삭제 버튼 클릭 → 완료

**상세 절차:**

1️⃣ **접수 현황판 확인**
   - 메인 화면에서 **접수 현황판** 또는 **대기 환자 목록** 확인

2️⃣ **환자 선택**
   - 접수를 취소할 환자를 선택 (클릭)

3️⃣ **취소 버튼 클릭**
   - 하단의 **[접수취소]** 또는 **[삭제]** 버튼 클릭

4️⃣ **확인**
   - 정말 취소하시겠습니까? 라는 확인 메시지에서 **예** 선택
   - 접수 취소 완료 ✅

> ⚠️ 취소된 접수는 복구되지 않습니다. 신중하게 진행하세요.
""",
    "환자 등록": """
### 📝 신규 환자 등록 방법

**주요 절차:** 인적사항 입력 → 중복확인 → 자격조회 → 저장

**상세 절차:**

1️⃣ **환자 정보 입력**
   - 성명, 주민등록번호, 주소 등 **인적사항 입력**
   - 연락처(휴대폰, 집전화) 입력

2️⃣ **중복확인**
   - **[중복확인]** 버튼 클릭
   - 기존 환자 중 중복 확인

3️⃣ **자격조회**
   - **[자격조회]** 버튼으로 보험 자격 확인
   - 본인부담금 등 요금 정보 확인

4️⃣ **저장**
   - 모든 정보 확인 후 **[저장]** 버튼 클릭
   - 신규 환자 등록 완료 ✅

> 💡 자격조회 미확인 시 수납이 지연될 수 있습니다.
""",
    "환자 정보 수정": """
### 🔄 환자 정보 수정 방법

**주요 절차:** 환자 검색 → 더블 클릭 → 정보 수정 → 저장

**상세 절차:**

1️⃣ **환자 검색**
   - 메인 화면 검색창에 **환자 성명** 또는 **차트 번호** 입력

2️⃣ **환자 상세 정보 열기**
   - 검색 결과에서 환자를 **더블 클릭**

3️⃣ **정보 수정**
   - 연락처, 주소 등 수정이 필요한 **항목 수정**
   - 변경 사항 확인

4️⃣ **저장**
   - **[저장]** 또는 **[수정완료]** 버튼 클릭
   - 환자 정보 수정 완료 ✅

> 📌 개인정보 보호법에 따라 민감 정보는 관리자만 수정 가능합니다.
"""
}

st.title("🏥 네오소프트뱅크 AI 고객지원")
st.write("Gemini AI가 탑재되어 무엇이든 물어볼 수 있습니다.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "img" in message:
            st.image(message["img"])

# 사용자 입력
if prompt := st.chat_input("질문을 입력하세요 (예: 환자 취소는 어떻게 해?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. 템플릿 우선 확인
        full_response = ""
        template_used = False
        
        # 템플릿 키워드 매칭
        if any(k in prompt for k in ["접수", "진료 받는 법"]):
            full_response = RESPONSE_TEMPLATES.get("접수")
            template_used = True
        elif any(k in prompt for k in ["취소", "삭제"]):
            full_response = RESPONSE_TEMPLATES.get("취소")
            template_used = True
        elif any(k in prompt for k in ["등록", "신규"]):
            full_response = RESPONSE_TEMPLATES.get("환자 등록")
            template_used = True
        elif any(k in prompt for k in ["수정", "조회"]):
            full_response = RESPONSE_TEMPLATES.get("환자 정보 수정")
            template_used = True
        
        # 템플릿 없으면 AI에게 요청
        if not template_used:
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"너는 네오소프트뱅크의 병원 프로그램 상담원이야. 친절하게 답해줘: {prompt}"
                )
                full_response = response.text
            except Exception as e:
                full_response = "죄송합니다! 현재 접속자가 많아 AI 답변이 잠시 지연되고 있습니다. 하지만 요청하신 매뉴얼은 위의 기본 가이드를 참고해주세요!"

        # 2. 키워드 기반 이미지 매칭 (템플릿과 무관하게 작동)
        img_url = None
        if any(k in prompt for k in ["등록", "신규"]):
            img_url = IMG_BASE + "regist.png"
        elif any(k in prompt for k in ["수정", "조회"]):
            img_url = IMG_BASE + "modify.png"
        elif "접수" in prompt and "취소" not in prompt:
            img_url = IMG_BASE + "reception.png"
        elif "취소" in prompt:
            img_url = IMG_BASE + "cancel.png"

        # 3. 결과 출력
        st.markdown(full_response)
        if img_url:
            st.image(img_url)
            st.session_state.messages.append({"role": "assistant", "content": full_response, "img": img_url})
        else:
            st.session_state.messages.append({"role": "assistant", "content": full_response})
