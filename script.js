let notaries = [];
let currentPage = 1;
let perPage = 25;
let filtered = [];

// Load data and initialize
async function loadData() {
  const response = await fetch('notaries.json');
  notaries = await response.json();
  filtered = [...notaries];
  renderCards();
}

function toCamelCase(text) {
  return text.split(/[-_\s]/)
    .map((word, index) => {
      if (index === 0) {
        return word.toLowerCase();
      }
      return word.charAt(0).toUpperCase + word.slice(1).toLowerCase;
    })
    .join('');
}

function renderCards() {
  const container = document.getElementById('cards-container');
  container.innerHTML = "";

  const start = (currentPage - 1) * perPage;
  const end = start + perPage;
  const currentItems = filtered.slice(start, end);

  currentItems.forEach(n => {
    const card = document.createElement('div');
    card.className = "bg-white dark:bg-gray-800 p-4 rounded-2xl shadow border dark:border-gray-700";
    card.innerHTML = `
      <div class="flex flex-col sm:flex-row justify-between" style="align-items: flex-end; margin-bottom: 2px">
        <h2 class="text-l" style="text-align: left; font-weight: bolder; color: #E5E5E5;">${n["Notary Name"] || "Unnamed"}</h2>
        <p class="text-sm" style="text-align: right; font-weight: 600; font-style: italic; color: #FFCB3C;">#${n["Commission Nbr"]}</p>
      </div>
      <hr style="border-top: 2.5px solid rgba(229, 229, 229, 0.51);">
      <div style="margin-bottom: 2px; margin-top: 1px;">
        <p class="text-sm" style="color: #BFBDC1;">Expires ${n["Expiration Date"]}</p>
      </div>
      <p class="text-sm text-gold-600" style="color: #E5E5E5;">🏢 ${n["Business Name"] || "Independent"}</p>
      <div>
        <span class="text-sm">📍 </span>
        <span class="text-sm" style="color: #E5E5E5;">${n["City"]}, ${n["State"]}</address></span>
      </div>    
    `;
    container.appendChild(card);
  });

  updatePagination();
}

function updatePagination() {
  const totalPages = Math.ceil(filtered.length / perPage);
  document.getElementById('pageInfo').textContent = `Page ${currentPage} of ${totalPages}`;
  document.getElementById('prevPage').disabled = currentPage === 1;
  document.getElementById('nextPage').disabled = currentPage >= totalPages;
}

document.getElementById('prevPage').addEventListener('click', () => {
  if (currentPage > 1) {
    currentPage--;
    renderCards();
  }
});

document.getElementById('nextPage').addEventListener('click', () => {
  const totalPages = Math.ceil(filtered.length / perPage);
  if (currentPage < totalPages) {
    currentPage++;
    renderCards();
  }
});

document.getElementById('perPage').addEventListener('change', (e) => {
  perPage = parseInt(e.target.value);
  currentPage = 1;
  renderCards();
});

document.getElementById('search').addEventListener('input', (e) => {
  const term = e.target.value.toLowerCase();
  filtered = notaries.filter(n =>
    Object.values(n).some(v => v.toLowerCase().includes(term))
  );
  currentPage = 1;
  renderCards();
});

loadData();

