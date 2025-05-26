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
      <h2 class="text-xl font-semibold mb-1">${n["Notary Name"] || "Unnamed"}</h2>
      <p class="text-sm text-gray-500 dark:text-gray-300 mb-2">${n["Business Name"] || "Independent"}</p>
      <p><strong>Commission #:</strong> ${n["Commission Nbr"]}</p></p>
      <p><strong>Address:</strong> ${n["Street Address"]}, ${n["City"]}, ${n["State"]} ${n["Zip Code"]}</p>
      <p><strong>County #:</strong> ${n["County Nbr"]}</p>
      <p><strong>Expires:</strong> ${n["Expiration Date"]}</p>
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

// Export current visible cards
document.getElementById('exportBtn').addEventListener('click', () => {
  const start = (currentPage - 1) * perPage;
  const end = start + perPage;
  const dataToExport = filtered.slice(start, end);

  const blob = new Blob([JSON.stringify(dataToExport, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = 'notary_cards_export.json';
  a.click();
  URL.revokeObjectURL(url);
});

// Print cards
document.getElementById('printBtn').addEventListener('click', () => {
  window.print();
});

// Share cards (Web Share API)
document.getElementById('shareBtn').addEventListener('click', async () => {
  const shareData = {
    title: 'Notary Business Cards',
    text: 'View these notary business cards.',
    url: window.location.href
  };

  try {
    if (navigator.share) {
      await navigator.share(shareData);
    } else {
      alert("Sharing not supported in this browser.");
    }
  } catch (err) {
    console.error("Share failed:", err);
  }
});

loadData();

