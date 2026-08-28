```javascript
const analyzeButton = document.getElementById("analyzeButton");

const loading = document.getElementById("loading");
const errorMessage = document.getElementById("errorMessage");
const result = document.getElementById("result");
const resultContent = document.getElementById("resultContent");


analyzeButton.addEventListener("click", async () => {

    // 입력값 가져오기
    const productName =
        document.getElementById("productName").value.trim();

    const category =
        document.getElementById("category").value;

    const sugar =
        document.getElementById("sugar").value;

    const sodium =
        document.getElementById("sodium").value;

    const protein =
        document.getElementById("protein").value;

    const fat =
        document.getElementById("fat").value;

    const saturatedFat =
        document.getElementById("saturatedFat").value;


    // 필수 입력값 확인
    if (!productName || !category) {

        errorMessage.textContent =
            "⚠️ 제품명과 제품 유형을 입력해주세요.";

        errorMessage.classList.remove("hidden");

        return;
    }


    // 이전 오류 및 결과 숨기기
    errorMessage.classList.add("hidden");
    result.classList.add("hidden");

    // 로딩 표시
    loading.classList.remove("hidden");

    // AI 분석 요청
    try {

        const response = await fetch("/api/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                productName,
                category,
                nutrition: {
                    sugar,
                    sodium,
                    protein,
                    fat,
                    saturatedFat
                }
            })

        });


        // 서버 오류 확인
        if (!response.ok) {
            throw new Error("API 요청에 실패했습니다.");
        }


        const data = await response.json();


        // AI 결과 화면에 표시
        resultContent.textContent = data.result;

        result.classList.remove("hidden");


    } catch (error) {

        console.error(error);

        errorMessage.textContent =
            "⚠️ 분석 결과를 가져오지 못했습니다. 잠시 후 다시 시도해주세요.";

        errorMessage.classList.remove("hidden");

    } finally {

        // 로딩 종료
        loading.classList.add("hidden");

    }

});
```

