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
      <h4 class="text-l font-bold mb-1" style="color: #E5E5E5; line-height: 1.0;">${n["Notary Name"] || "Unnamed"}</h4>
      <div style="line-height: 1.5">
        <span class="text-sm text-gray-500 dark:text-gray-300 mb-1" style="color: #FFCB3C;">#${n["Commission Nbr"]}</span>
        <span class="text-sm" style="color: #BFBDC1;"><i> | Expires ${n["Expiration Date"]}</i></span>
      </div>
      <p class="text-sm text-gold-600" style="color: #E5E5E5;">🏢 ${n["Business Name"] || "Independent"}</p>
      <p class="text-sm" style="color: #E5E5E5;">📍 ${n["City"]}, ${n["State"]} ${n["Zip Code"]}</p>
      
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

