const plannerConfigElement = document.getElementById("planner-config");
const plannerConfig = plannerConfigElement ? JSON.parse(plannerConfigElement.textContent) : null;
const classData = plannerConfig ? plannerConfig.classes : [];
const plannerText = plannerConfig ? plannerConfig.text : {};

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

function interpolate(template, values) {
  return template.replace(/\{(\w+)\}/g, (_, key) => values[key] ?? "");
}

function renderResult(container, ranked, values) {
  const top = ranked[0];
  const formatLabel = plannerText.options.format[values.format] || values.format;
  container.innerHTML = `
    <p class="kicker">${plannerText.recommended}</p>
    <h3>${top.name}</h3>
    <p><strong>${top.role}</strong></p>
    <p>${interpolate(plannerText.fit, { name: top.name, format: formatLabel })}</p>
    <div class="result-list">
      ${ranked.slice(0, 4).map(item => `
        <div class="result-item">
          <strong>${item.name}</strong>
          <div class="score-bar" aria-label="${interpolate(plannerText.score_label, { score: item.score })}"><span style="--score:${item.score}%"></span></div>
          <small>${interpolate(plannerText.score_text, { score: item.score, role: item.role })}</small>
        </div>
      `).join("")}
    </div>
    <p class="empty-state">${plannerText.note}</p>
  `;
}

document.querySelectorAll("[data-planner-form]").forEach((form) => {
  const result = form.parentElement.querySelector("[data-planner-result]");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    result.innerHTML = `<p class="empty-state">${plannerText.calculating}</p>`;
    const values = Object.fromEntries(new FormData(form).entries());
    const ranked = classData
      .map((item) => ({ ...item, score: scoreClass(item, values) }))
      .sort((a, b) => b.score - a.score);
    window.setTimeout(() => renderResult(result, ranked, values), 180);
  });
  form.addEventListener("reset", () => {
    if (result) {
      result.innerHTML = `<p class="empty-state">${plannerText.empty}</p>`;
    }
  });
});
