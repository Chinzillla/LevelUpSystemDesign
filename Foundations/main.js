const app = document.getElementById("app");
const button = document.getElementById("get-data");
const result = document.getElementById("result");

app.textContent = "Hello, world!";

button.addEventListener("click", async () => {
    result.textContent = "Loading...";

    try {
        const response = await fetch("http://127.0.0.1:5000/")

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        result.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        result.textContent = `Error: ${error.message}`; 
    }
});
