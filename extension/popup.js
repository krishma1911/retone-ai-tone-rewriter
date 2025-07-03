document.getElementById("rewriteBtn").addEventListener("click", async () => {
  const text = document.getElementById("inputText").value;
  const tone = document.getElementById("toneSelect").value;

  const response = await fetch("http://localhost:5000/rewrite", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text, tone })
  });

  const data = await response.json();
  document.getElementById("output").textContent = data.result || "Error rewriting text.";
});
