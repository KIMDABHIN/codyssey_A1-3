import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai


PROJECT_ROOT = Path(__file__).resolve().parent.parent

app = FastAPI()


# -----------------------------
# 정적 파일
# -----------------------------

app.mount(
    "/css",
    StaticFiles(directory=str(PROJECT_ROOT / "css")),
    name="css"
)

app.mount(
    "/js",
    StaticFiles(directory=str(PROJECT_ROOT / "js")),
    name="js"
)

app.mount(
    "/css",
    StaticFiles(directory=str(PROJECT_ROOT / "css")),
    name="css"
)

app.mount(
    "/js",
    StaticFiles(directory=str(PROJECT_ROOT / "js")),
    name="js"
)


# -----------------------------
# 홈페이지
# -----------------------------

@app.get("/")
def homepage():
    return FileResponse(
        str(PROJECT_ROOT / "index.html")
    )


# -----------------------------
# AI 분석 데이터
# -----------------------------

class NutritionData(BaseModel):
    productName: str
    category: str
    nutrition: dict


# -----------------------------
# API 테스트
# -----------------------------

@app.get("/api")
def api_home():
    return {
        "message": "한눈영양 API가 정상적으로 작동합니다."
    }


# -----------------------------
# AI 영양 분석
# -----------------------------

@app.post("/api")
def analyze_nutrition(data: NutritionData):

    try:
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            return {
                "error": "GEMINI_API_KEY 환경변수가 설정되지 않았습니다."
            }

        product_name = data.productName.strip()
        category = data.category.strip()

        if not product_name or not category:
            return {
                "error": "제품명과 제품 유형을 입력해주세요."
            }

        nutrition = data.nutrition

        sugar = nutrition.get("sugar", "")
        sodium = nutrition.get("sodium", "")
        protein = nutrition.get("protein", "")
        fat = nutrition.get("fat", "")
        saturated_fat = nutrition.get("saturatedFat", "")

        client = genai.Client(
            api_key=api_key
        )

        prompt = f"""
당신은 식품 영양성분표를 쉽게 설명해주는 AI 영양 정보 도우미입니다.

의료적 진단이나 치료를 하지 말고,
일반적인 영양 정보와 식품 선택에 도움이 되는 내용을
쉽고 친절하게 설명해주세요.

제품명: {product_name}
제품 유형: {category}

당류: {sugar} g
나트륨: {sodium} mg
단백질: {protein} g
지방: {fat} g
포화지방: {saturated_fat} g

다음 형식으로 답변해주세요.

1. 한눈에 보는 평가
- 전체적인 영양 특징을 2~3문장으로 설명

2. 주의할 점
- 당류, 나트륨, 지방, 포화지방 등을 기준으로 설명

3. 이렇게 먹어보세요
- 부담을 줄이는 섭취 방법을 설명

4. 대체 식품
- 비교해볼 만한 식품 2~3가지를 제안

어려운 전문용어는 최대한 피하고,
사용자가 실제 식품을 고를 때 이해하기 쉬운 표현을 사용해주세요.

※ 본 결과는 일반적인 영양 정보 제공을 위한 참고용이며
의료적 진단이나 치료를 대신하지 않습니다.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return {
            "result": response.text
        }

    except Exception as e:

        print(
            "API ERROR:",
            repr(e)
        )

        return {
            "error": f"{type(e).__name__}: {e}"
        }
