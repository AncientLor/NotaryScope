let notaries = [];
let currentPage = 1;
let perPage = 25;
let filtered = [];
let stateSelect = "CA";

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
    // deepcode ignore DOMXSS: Static input data controlled by server.
    card.innerHTML = `
      <div class="flex flex-col sm:flex-row justify-between" style="margin-bottom: 10px; align-items: flex-end;">
        <p title="Notary Name" class="text" style="font-size: 17px; font-weight: bolder; color: #dddddd;">${n["Notary Name"] || "Unnamed"}</p>
        <p title="Commission Number" class="text-m" style="font-weight: 400; font-style: normal; color: #ffbf00;">#${n["Commission Nbr"]}</p>
      </div>
      <hr style="margin-bottom: 10px; border-top: 3px solid rgba(154, 135, 183, 0.8);">
      <div class="flex flex-col sm:flex-col justify-center items-left">
        <p id="notary-business" title="Business Title" class="text-sm mb-2" style="color: #dddddd;">💼 ${n["Business Name"] || "Independent"}</p>
        <p id="notary-location" title="City of Operation" class="text-sm mb-2" style="color: #dddddd;">📍 ${n["City"]}, ${n["State"]}</p>
      </div>
      <p id="notary-expiration" title="Expiration Date" class="text-sm mb-2" style="color: #dddddd;">⏳ <i>Valid until ${n["Expiration Date"]}<i></p>
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

document.getElementById('stateSelect').addEventListener('change', (e) => {
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

