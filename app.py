import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="어린이를 위한 AI 그림 생성기",
    page_icon="🎨",
    layout="wide"
)

# OpenAI 클라이언트 설정
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 사이드바 설정
with st.sidebar:
    st.header("설정 패널")
    
    # 그림체 선택 (다중 선택 가능)
    selected_styles = st.multiselect(
        "그림 스타일 선택",
        options=["카툰", "수채화", "디지털 아트", "유화", "일러스트"],
        default=["카툰"]
    )
    
    # 이미지 크기 선택 (단일 선택)
    image_size = st.radio(
        "이미지 크기 선택",
        options=["1024x1024", "1024x1792", "1792x1024"],
        index=0
    )

# 기본 안전 필터 프롬프트
safety_prompt = """
초등학생을 위한 선정적이지 않고 건전하며 폭력적이지 않은 그림, 
고품질 4K 해상도, 전문적인 작품, 생동감 있는 색상, 안전한 콘텐츠, 
밝고 친근한 분위기, 교육적으로 적합한 내용
""".strip().replace("\n", " ")

# 화면 분할
left_col, right_col = st.columns([1, 1])

with left_col:
    st.header("프롬프트 입력")
    user_prompt = st.text_area(
        "그림 설명을 입력하세요:",
        height=200,
        placeholder="예) 숲 속 동물들이 함께 놀고 있는 모습"
    )
    
    generate_button = st.button("그림 생성하기", type="primary")

with right_col:
    st.header("생성 결과")
    image_placeholder = st.empty()

# 그림 생성 함수
def generate_image(prompt, size, styles):
    try:
        # 스타일 조합
        style_text = ", ".join(styles) if styles else ""
        
        # 최종 프롬프트 조립
        full_prompt = f"{prompt} - {style_text} {safety_prompt}"
        
        # DALL-E 3 호출
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size=size,
            quality="hd",
            n=1
        )
        
        return response.data[0].url
    except Exception as e:
        st.error(f"그림 생성 중 오류 발생: {str(e)}")
        return None

# 버튼 클릭 처리
if generate_button:
    if not user_prompt:
        st.warning("그림 설명을 입력해주세요!")
    else:
        with st.spinner("AI가 그림을 그리는 중입니다..."):
            image_url = generate_image(
                prompt=user_prompt,
                size=image_size,
                styles=selected_styles
            )
            
            if image_url:
                image_placeholder.image(
                    image_url,
                    caption="생성된 그림",
                    use_column_width=True
                )
                st.success("그림 생성 완료! 🎉")

# 기본 사용법 안내
with st.expander("사용 방법 안내"):
    st.markdown("""
    1. 왼쪽 입력창에 원하는 그림 설명을 작성해주세요
    2. 사이드바에서 원하는 그림 스타일과 크기를 선택해주세요
    3. [그림 생성하기] 버튼을 클릭하면 AI가 그림을 만들어줍니다
    4. 우측 화면에서 생성된 결과를 확인할 수 있습니다

    **주의사항:**
    - 초등학생에게 부적합한 내용은 자동으로 필터링됩니다
    - 최고 화질(HD)로 자동 설정되어 있습니다
    - 생성에는 약 10-30초 정도 소요됩니다
    """)

# 사이드바 하단에 추가 정보 표시
st.sidebar.markdown("---")
st.sidebar.info(
    "이 애플리케이션은 OpenAI의 DALL-E 3 모델을 사용하며, "
    "모든 생성 결과는 자동 안전 필터링을 거칩니다."
)