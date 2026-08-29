import json
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler

from google import genai


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            request_path = self.path.split("?")[0]

            if request_path == "/":
                file_path = PROJECT_ROOT / "index.html"
            elif request_path == "/css/style.css":
                file_path = PROJECT_ROOT / "css" / "style.css"
            elif request_path == "/js/app.js":
                file_path = PROJECT_ROOT / "js" / "app.js"
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not Found")
                return

            if not file_path.exists():
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File Not Found")
                return

            content = file_path.read_bytes()

            if file_path.suffix == ".html":
                content_type = "text/html; charset=utf-8"
            elif file_path.suffix == ".css":
                content_type = "text/css; charset=utf-8"
            elif file_path.suffix == ".js":
                content_type = "application/javascript; charset=utf-8"
            else:
                content_type = "application/octet-stream"

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        except Exception as e:
            print("GET ERROR:", str(e))
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

    def do_POST(self):
        try:
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))

            product_name = data.get("productName", "").strip()
            category = data.get("category", "").strip()

            nutrition = data.get("nutrition", {})

            sugar = nutrition.get("sugar", "")
            sodium = nutrition.get("sodium", "")
            protein = nutrition.get("protein", "")
            fat = nutrition.get("fat", "")
            saturated_fat = nutrition.get("saturatedFat", "")

            if not product_name or not category:
                self.send_json(
                    400,
                    {
                        "error": "제품명과 제품 유형을 입력해주세요."
                    }
                )
                return

            api_key = os.environ.get("GEMINI_API_KEY")

            if not api_key:
                self.send_json(
                    500,
                    {
                        "error": "GEMINI_API_KEY 환경변수가 설정되지 않았습니다."
                    }
                )
                return

            client = genai.Client(api_key=api_key)

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

어려운 전문용어는 최대한 피해주세요.

※ 본 결과는 일반적인 영양 정보 제공을 위한 참고용이며
의료적 진단이나 치료를 대신하지 않습니다.
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            self.send_json(
                200,
                {
                    "result": response.text
                }
            )

        except json.JSONDecodeError:
            self.send_json(
                400,
                {
                    "error": "입력 데이터를 확인해주세요."
                }
            )

       except Exception as e:
    print("API ERROR:", repr(e))

    self.send_json(
        500,
        {
            "error": f"AI 분석 오류: {type(e).__name__}: {e}"
        }
    )
    def send_json(self, status_code, data):
        response = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status_code)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(response))
        )
        self.end_headers()

        self.wfile.write(response)