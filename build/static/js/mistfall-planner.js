const classData = [
  { name: "Mercenary", role: "Frontline brawler", solo: 86, squad: 78, burst: 60, control: 54, frontline: 92, risk: "low" },
  { name: "Blackarrow", role: "Ranged pressure", solo: 74, squad: 84, burst: 78, control: 64, frontline: 58, risk: "medium" },
  { name: "Shadowstrix", role: "Assassin skirmisher", solo: 82, squad: 70, burst: 90, control: 58, frontline: 62, risk: "high" },
  { name: "Sorcerer", role: "Area damage caster", solo: 66, squad: 88, burst: 92, control: 82, frontline: 40, risk: "high" },
  { name: "Seer", role: "Support and information", solo: 58, squad: 92, burst: 42, control: 86, frontline: 38, risk: "medium" },
  { name: "Withered Knight", role: "Durable initiator", solo: 78, squad: 86, burst: 64, control: 76, frontline: 88, risk: "medium" }
];

function riskScore(classRisk, selectedRisk) {
  const order = { low: 1, medium: 2, high: 3 };
  const distance = Math.abs(order[classRisk] - order[selectedRisk]);
  return 30 - distance * 12;
}

function scoreClass(item, values) {
  let score = values.format === "solo" ? item.solo : values.format === "squad" ? item.squad : Math.round((item.solo + item.squad) / 2);
  if (values.style !== "balanced") {
    score = Math.round(score * 0.55 + item[values.style] * 0.45);
  }
  score += riskScore(item.risk, values.risk);
  if (values.experience === "new" && item.risk === "high") score -= 12;
  if (values.experience === "advanced" && item.risk === "high") score += 8;
  return Math.max(0, Math.min(100, score));
}

function renderResult(container, ranked, values) {
  const top = ranked[0];
  container.innerHTML = `
    <p class="kicker">Recommended class</p>
    <h3>${top.name}</h3>
    <p><strong>${top.role}</strong></p>
    <p>${top.name} fits your ${values.format} run because the scoring model balances class role, selected combat rhythm, risk tolerance, and experience level.</p>
    <div class="result-list">
      ${ranked.slice(0, 4).map(item => `
        <div class="result-item">
          <strong>${item.name}</strong>
          <div class="score-bar" aria-label="${item.score} out of 100"><span style="--score:${item.score}%"></span></div>
          <small>${item.score}/100 · ${item.role}</small>
        </div>
      `).join("")}
    </div>
    <p class="empty-state">Model note: this is a fan-made recommendation and should be rechecked when verified Mistfall Hunter class balance data changes.</p>
  `;
}

document.querySelectorAll("[data-planner-form]").forEach((form) => {
  const result = form.parentElement.querySelector("[data-planner-result]");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    result.innerHTML = "<p class='empty-state'>Calculating class fit...</p>";
    const values = Object.fromEntries(new FormData(form).entries());
    const ranked = classData
      .map((item) => ({ ...item, score: scoreClass(item, values) }))
      .sort((a, b) => b.score - a.score);
    window.setTimeout(() => renderResult(result, ranked, values), 180);
  });
  form.addEventListener("reset", () => {
    if (result) {
      result.innerHTML = "<p class='empty-state'>Your recommendation will appear here. Try the default solo setup first if you are unsure.</p>";
    }
  });
});
