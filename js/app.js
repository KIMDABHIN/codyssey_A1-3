
const analyzeButton = document.getElementById("analyzeButton");

const loading = document.getElementById("loading");
const errorMessage = document.getElementById("errorMessage");
const result = document.getElementById("result");
const resultContent = document.getElementById("resultContent");


analyzeButton.addEventListener("click", async () => {
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


    if (!productName || !category) {
        errorMessage.textContent =
            "⚠️ 제품명과 제품 유형을 입력해주세요.";

        errorMessage.classList.remove("hidden");
        return;
    }


    errorMessage.classList.add("hidden");
    result.classList.add("hidden");
    resultContent.textContent = "";

    loading.classList.remove("hidden");


    try {
        const response = await fetch("/api", {
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


        const data = await response.json();
        console.log("AI 응답:", data);


        if (!response.ok) {
            throw new Error(
                data.error || "AI 분석 요청에 실패했습니다."
            );
        }


        resultContent.textContent = data.result;

        result.classList.remove("hidden");


    } catch (error) {
        console.error("AI 분석 오류:", error);

        errorMessage.textContent =
            "⚠️ AI 분석에 실패했습니다. 잠시 후 다시 시도해주세요.";

        errorMessage.classList.remove("hidden");


    } finally {
        loading.classList.add("hidden");
    }
});

