```python
import json
import os

from http.server import BaseHTTPRequestHandler

from google import genai


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            data = json.loads(body.decode("utf-8"))

            product_name = data.get("productName", "").strip()
            category = data.get("category", "").strip()
            sugar = data.get("sugar", "")
            sodium = data.get("sodium", "")
            protein = data.get("protein", "")
            fat = data.get("fat", "")
            saturated_fat = data.get("saturatedFat", "")

            if not product_name or not category:
                self.send_json(
                    400,
                    {"error": "제품명과 제품 유형을 입력해주세요."}
                )
                return

            api_key = os.environ.get("GEMINI_API_KEY")

            if not api_key:
                self.send_json(
                    500,
                    {"error": "GEMINI_API_KEY 환경변수가 설정되지 않았습니다."}
                )
                return

            client = genai.Client(api_key=api_key)

            prompt = f"""
당신은 식품 영양성분표를 쉽게 설명해주는 AI 영양 정보 도우미입니다.

의료적 진단이나 치료를 하지 말고,
일반적인 영양 정보와 식품 선택에 도움이 되는 내용을 쉽고 친절하게 설명해주세요.

다음 식품의 영양성분을 분석해주세요.

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
- 당류, 나트륨, 지방, 포화지방 등을 기준으로 주의할 부분
- 특별히 주의가 필요할 수 있는 사람을 일반적인 수준에서 설명

3. 이렇게 먹어보세요
- 부담을 줄이는 섭취 방법이나 함께 선택하면 좋은 식품

4. 대체 식품
- 비슷한 종류 중 영양 측면에서 비교해볼 만한 식품 2~3가지

어려운 전문용어는 최대한 피하고,
사용자가 실제 식품을 고를 때 이해하기 쉬운 표현을 사용해주세요.

마지막에는 다음 문구를 반드시 포함해주세요.

※ 본 결과는 일반적인 영양 정보 제공을 위한 참고용이며 의료적 진단을 대신하지 않습니다.
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result = response.text

            self.send_json(
                200,
                {"result": result}
            )

        except json.JSONDecodeError:
            self.send_json(
                400,
                {"error": "입력 데이터를 확인해주세요."}
            )

        except Exception as e:
            print("API ERROR:", str(e))

            self.send_json(
                500,
                {"error": "AI 분석 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}
            )

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def send_json(self, status_code, data):
        response = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(response)
```

