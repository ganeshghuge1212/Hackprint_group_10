// API Configuration
const API_URL = 'http://localhost:8000';

// DOM Elements
const scrapeForm = document.getElementById('scrapeForm');
const urlInput = document.getElementById('urlInput');
const scrapeBtn = document.getElementById('scrapeBtn');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');
const exampleButtons = document.querySelectorAll('.example-btn');
const tabButtons = document.querySelectorAll('.tab-btn');

// Example URL Buttons
exampleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        urlInput.value = btn.dataset.url;
        urlInput.focus();
    });
});

// Tab Switching
tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;

        // Update active tab button
        tabButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update active tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
    });
});

// Form Submission
scrapeForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = urlInput.value.trim();
    if (!url) return;

    await scrapeWebsite(url);
});

// Main Scraping Function
async function scrapeWebsite(url) {
    try {
        // Show loading, hide error and results
        loading.classList.add('active');
        errorMessage.classList.remove('active');
        resultsSection.classList.remove('active');
        scrapeBtn.disabled = true;

        // Make API request
        const response = await fetch(`${API_URL}/scrape`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to scrape website');
        }

        if (data.success) {
            displayResults(data.data);
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }

    } catch (error) {
        showError(error.message);
    } finally {
        loading.classList.remove('active');
        scrapeBtn.disabled = false;
    }
}

// Display Results
function displayResults(data) {
    // Display statistics
    displayStats(data.stats);

    // Display metadata
    displayMetadata(data.metadata);

    // Display headings
    displayHeadings(data.text.headings);

    // Display paragraphs
    displayParagraphs(data.text.paragraphs);

    // Display images
    displayImages(data.images);

    // Display links
    displayLinks(data.links);

    // Display tables
    displayTables(data.tables);

    // Show results section
    resultsSection.classList.add('active');

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Display Statistics
function displayStats(stats) {
    const statsGrid = document.getElementById('statsGrid');
    statsGrid.innerHTML = `
        <div class="stat-card">
            <span class="stat-value">${stats.total_headings}</span>
            <span class="stat-label">Headings</span>
        </div>
        <div class="stat-card">
            <span class="stat-value">${stats.total_paragraphs}</span>
            <span class="stat-label">Paragraphs</span>
        </div>
        <div class="stat-card">
            <span class="stat-value">${stats.total_images}</span>
            <span class="stat-label">Images</span>
        </div>
        <div class="stat-card">
            <span class="stat-value">${stats.total_links}</span>
            <span class="stat-label">Links</span>
        </div>
        <div class="stat-card">
            <span class="stat-value">${stats.total_tables}</span>
            <span class="stat-label">Tables</span>
        </div>
    `;
}

// Display Metadata
function displayMetadata(metadata) {
    const metadataContent = document.getElementById('metadataContent');
    metadataContent.innerHTML = '';

    const metadataItems = [
        { label: 'Title', value: metadata.title || 'N/A' },
        { label: 'Description', value: metadata.description || 'N/A' },
        { label: 'Keywords', value: metadata.keywords || 'N/A' },
        { label: 'Author', value: metadata.author || 'N/A' }
    ];

    metadataItems.forEach(item => {
        const div = document.createElement('div');
        div.className = 'metadata-item';
        div.innerHTML = `
            <div class="metadata-label">${item.label}</div>
            <div class="metadata-value">${escapeHtml(item.value)}</div>
        `;
        metadataContent.appendChild(div);
    });
}

// Display Headings
function displayHeadings(headings) {
    const headingsContent = document.getElementById('headingsContent');
    headingsContent.innerHTML = '';

    let hasHeadings = false;

    for (let level = 1; level <= 6; level++) {
        const key = `h${level}`;
        const items = headings[key];

        if (items && items.length > 0) {
            hasHeadings = true;
            const div = document.createElement('div');
            div.className = 'heading-group';

            const title = document.createElement('h3');
            title.textContent = `Heading ${level}`;
            div.appendChild(title);

            const ul = document.createElement('ul');
            items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                ul.appendChild(li);
            });
            div.appendChild(ul);

            headingsContent.appendChild(div);
        }
    }

    if (!hasHeadings) {
        headingsContent.innerHTML = '<div class="empty-state">No headings found</div>';
    }
}

// Display Paragraphs
function displayParagraphs(paragraphs) {
    const paragraphsContent = document.getElementById('paragraphsContent');
    paragraphsContent.innerHTML = '';

    if (paragraphs && paragraphs.length > 0) {
        // Limit to first 50 paragraphs to avoid overwhelming the UI
        const displayParagraphs = paragraphs.slice(0, 50);

        displayParagraphs.forEach(para => {
            const div = document.createElement('div');
            div.className = 'paragraph-item';
            div.textContent = para;
            paragraphsContent.appendChild(div);
        });

        if (paragraphs.length > 50) {
            const note = document.createElement('div');
            note.className = 'empty-state';
            note.textContent = `Showing first 50 of ${paragraphs.length} paragraphs`;
            paragraphsContent.appendChild(note);
        }
    } else {
        paragraphsContent.innerHTML = '<div class="empty-state">No paragraphs found</div>';
    }
}

// Display Images
function displayImages(images) {
    const imagesContent = document.getElementById('imagesContent');
    imagesContent.innerHTML = '';

    if (images && images.length > 0) {
        images.forEach(img => {
            const div = document.createElement('div');
            div.className = 'image-item';

            const imgEl = document.createElement('img');
            imgEl.src = img.url;
            imgEl.alt = img.alt || 'Image';
            imgEl.onerror = function () {
                this.style.display = 'none';
                const errorMsg = document.createElement('div');
                errorMsg.style.padding = '2rem';
                errorMsg.style.textAlign = 'center';
                errorMsg.style.color = 'var(--text-muted)';
                errorMsg.textContent = 'Failed to load image';
                this.parentElement.appendChild(errorMsg);
            };

            div.appendChild(imgEl);

            const info = document.createElement('div');
            info.className = 'image-info';
            info.innerHTML = `
                <div class="image-alt">${escapeHtml(img.alt || 'No alt text')}</div>
                <div class="image-url">${escapeHtml(img.url)}</div>
            `;
            div.appendChild(info);

            imagesContent.appendChild(div);
        });
    } else {
        imagesContent.innerHTML = '<div class="empty-state">No images found</div>';
    }
}

// Display Links
function displayLinks(links) {
    displayLinksList(links.internal, 'internalLinksContent');
    displayLinksList(links.external, 'externalLinksContent');
}

function displayLinksList(linkArray, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    if (linkArray && linkArray.length > 0) {
        // Limit to first 100 links
        const displayLinks = linkArray.slice(0, 100);

        displayLinks.forEach(link => {
            const div = document.createElement('div');
            div.className = 'link-item';

            const textDiv = document.createElement('div');
            textDiv.style.flex = '1';
            textDiv.innerHTML = `
                <div class="link-text">${escapeHtml(link.text || 'No text')}</div>
                <div class="link-url">${escapeHtml(link.url)}</div>
            `;

            const visitBtn = document.createElement('a');
            visitBtn.href = link.url;
            visitBtn.target = '_blank';
            visitBtn.rel = 'noopener noreferrer';
            visitBtn.className = 'link-visit';
            visitBtn.textContent = 'Visit →';

            div.appendChild(textDiv);
            div.appendChild(visitBtn);
            container.appendChild(div);
        });

        if (linkArray.length > 100) {
            const note = document.createElement('div');
            note.className = 'empty-state';
            note.textContent = `Showing first 100 of ${linkArray.length} links`;
            container.appendChild(note);
        }
    } else {
        container.innerHTML = '<div class="empty-state">No links found</div>';
    }
}

// Display Tables
function displayTables(tables) {
    const tablesContent = document.getElementById('tablesContent');
    tablesContent.innerHTML = '';

    if (tables && tables.length > 0) {
        tables.forEach((tableData, index) => {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-wrapper';

            const table = document.createElement('table');

            // Add headers if available
            if (tableData.headers && tableData.headers.length > 0) {
                const thead = document.createElement('thead');
                const headerRow = document.createElement('tr');

                tableData.headers.forEach(header => {
                    const th = document.createElement('th');
                    th.textContent = header;
                    headerRow.appendChild(th);
                });

                thead.appendChild(headerRow);
                table.appendChild(thead);
            }

            // Add rows
            if (tableData.rows && tableData.rows.length > 0) {
                const tbody = document.createElement('tbody');

                tableData.rows.forEach(row => {
                    const tr = document.createElement('tr');

                    row.forEach(cell => {
                        const td = document.createElement('td');
                        td.textContent = cell;
                        tr.appendChild(td);
                    });

                    tbody.appendChild(tr);
                });

                table.appendChild(tbody);
            }

            wrapper.appendChild(table);
            tablesContent.appendChild(wrapper);
        });
    } else {
        tablesContent.innerHTML = '<div class="empty-state">No tables found</div>';
    }
}

// Show Error
function showError(message) {
    errorMessage.textContent = `Error: ${message}`;
    errorMessage.classList.add('active');
    resultsSection.classList.remove('active');
}

// Utility: Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Check API Health on Load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (!response.ok) {
            showError('Backend server is not running. Please start the server first.');
        }
    } catch (error) {
        showError('Cannot connect to backend server. Please ensure the server is running at http://localhost:8000');
    }
});
