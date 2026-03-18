/**
 * Global Search - Cmd+K / Ctrl+K
 * Lazy loads MiniSearch on first use
 * Customize SEARCH_* arrays in search-data.js
 */

(function() {
    'use strict';

    let searchReady = false;
    let miniSearch = null;
    let searchIndex = [];
    let selectedIndex = -1;
    let lastFocusedElement = null;

    // DOM elements (cached after init)
    let modal, input, results, statusEl;

    /**
     * Load script dynamically
     */
    function loadScript(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    /**
     * Build search index from available sources
     * Customize by adding your own window.SEARCH_* arrays
     */
    function buildIndex() {
        const items = [];

        // Features
        if (window.SEARCH_FEATURES) {
            items.push(...window.SEARCH_FEATURES);
        }

        // FAQ
        if (window.SEARCH_FAQ) {
            items.push(...window.SEARCH_FAQ);
        }

        // Docs
        if (window.SEARCH_DOCS) {
            items.push(...window.SEARCH_DOCS);
        }

        // Custom items
        if (window.SEARCH_CUSTOM) {
            items.push(...window.SEARCH_CUSTOM);
        }

        return items;
    }

    /**
     * Initialize search (called on first Cmd+K)
     */
    async function initSearch() {
        if (searchReady) return true;

        // Build index
        searchIndex = buildIndex();

        if (searchIndex.length === 0) {
            console.warn('Search: No items to index');
            return false;
        }

        // Try to load MiniSearch from CDN
        if (!window.MiniSearch) {
            try {
                await loadScript('https://cdn.jsdelivr.net/npm/minisearch@7/dist/umd/index.min.js');
            } catch (e) {
                console.warn('Search: MiniSearch CDN failed, using fallback');
            }
        }

        // Initialize MiniSearch or fallback
        if (window.MiniSearch) {
            miniSearch = new MiniSearch({
                fields: ['title', 'content', 'category'],
                storeFields: ['title', 'type', 'url', 'category'],
                searchOptions: {
                    fuzzy: 0.2,
                    prefix: true,
                    boost: { title: 2 }
                }
            });
            miniSearch.addAll(searchIndex);
        } else {
            // Fallback: simple substring search
            miniSearch = {
                search: (query) => {
                    const q = query.toLowerCase();
                    return searchIndex.filter(item =>
                        item.title.toLowerCase().includes(q) ||
                        item.content.toLowerCase().includes(q) ||
                        (item.category && item.category.toLowerCase().includes(q))
                    ).map(item => ({ ...item, score: 1 }));
                }
            };
        }

        searchReady = true;
        return true;
    }

    /**
     * Perform search and return results
     */
    function search(query) {
        if (!searchReady || !query.trim()) return [];

        const searchResults = miniSearch.search(query);

        // Group by type and limit
        const grouped = {};
        searchResults.forEach(r => {
            const type = r.type || 'item';
            if (!grouped[type]) grouped[type] = [];
            if (grouped[type].length < 5) {
                grouped[type].push(r);
            }
        });

        // Flatten all groups
        return Object.values(grouped).flat();
    }

    /**
     * Render search results
     */
    function renderResults(items) {
        if (!results) return;

        selectedIndex = -1;

        if (items.length === 0) {
            results.innerHTML = '<li class="search-no-results">No results found</li>';
            announceResults(0);
            return;
        }

        const typeIcons = {
            feature: '⚡',
            faq: '❓',
            doc: '📖',
            install: '📦',
            provider: '🔌',
            default: '📄'
        };

        results.innerHTML = items.map((item, i) => `
            <li class="search-result-item"
                role="option"
                id="search-result-${i}"
                data-url="${item.url}"
                tabindex="-1">
                <span class="search-result-type">${typeIcons[item.type] || typeIcons.default} ${item.type || 'item'}</span>
                <span class="search-result-title">${escapeHtml(item.title)}</span>
                ${item.category ? `<span class="search-result-category">${item.category}</span>` : ''}
            </li>
        `).join('');

        // Add click handlers
        results.querySelectorAll('.search-result-item').forEach((el, i) => {
            el.addEventListener('click', () => navigateTo(items[i].url));
        });

        announceResults(items.length);
    }

    /**
     * Announce results to screen readers
     */
    function announceResults(count) {
        if (statusEl) {
            statusEl.textContent = count === 0
                ? 'No results found'
                : `${count} result${count > 1 ? 's' : ''} found. Use arrow keys to navigate.`;
        }
    }

    /**
     * Navigate to result URL
     */
    function navigateTo(url) {
        closeModal();
        window.location.href = url;
    }

    /**
     * Update selected item
     */
    function updateSelection(newIndex) {
        const items = results.querySelectorAll('.search-result-item');
        if (items.length === 0) return;

        // Wrap around
        if (newIndex < 0) newIndex = items.length - 1;
        if (newIndex >= items.length) newIndex = 0;

        // Update aria-selected
        items.forEach((el, i) => {
            el.setAttribute('aria-selected', i === newIndex ? 'true' : 'false');
        });

        // Scroll into view
        items[newIndex].scrollIntoView({ block: 'nearest' });

        selectedIndex = newIndex;
    }

    /**
     * Handle keyboard navigation
     */
    function handleKeydown(e) {
        const items = results.querySelectorAll('.search-result-item');

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                updateSelection(selectedIndex + 1);
                break;

            case 'ArrowUp':
                e.preventDefault();
                updateSelection(selectedIndex - 1);
                break;

            case 'Enter':
                e.preventDefault();
                if (selectedIndex >= 0 && items[selectedIndex]) {
                    const url = items[selectedIndex].dataset.url;
                    if (url) navigateTo(url);
                }
                break;

            case 'Home':
                e.preventDefault();
                updateSelection(0);
                break;

            case 'End':
                e.preventDefault();
                updateSelection(items.length - 1);
                break;

            case 'Escape':
                e.preventDefault();
                closeModal();
                break;
        }
    }

    /**
     * Open search modal
     */
    async function openModal() {
        if (!modal) return;

        // Initialize search on first open
        const ready = await initSearch();
        if (!ready) {
            console.error('Search: Failed to initialize');
            return;
        }

        // Save current focus
        lastFocusedElement = document.activeElement;

        // Show modal
        modal.hidden = false;
        document.body.style.overflow = 'hidden';

        // Focus input
        setTimeout(() => {
            input.value = '';
            input.focus();
            renderResults([]);
        }, 10);
    }

    /**
     * Close search modal
     */
    function closeModal() {
        if (!modal) return;

        modal.hidden = true;
        document.body.style.overflow = '';

        // Restore focus
        if (lastFocusedElement) {
            lastFocusedElement.focus();
        }
    }

    /**
     * Escape HTML
     */
    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    /**
     * Focus trap for accessibility
     */
    function trapFocus(e) {
        if (!modal || modal.hidden) return;

        const focusable = modal.querySelectorAll(
            'input, button, [tabindex]:not([tabindex="-1"])'
        );
        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first.focus();
        }
    }

    /**
     * Initialize when DOM is ready
     */
    function init() {
        // Get DOM elements
        modal = document.getElementById('search-modal');
        input = document.getElementById('search-input');
        results = document.getElementById('search-results');
        statusEl = document.getElementById('search-status');

        if (!modal || !input || !results) {
            console.warn('Search: Modal elements not found');
            return;
        }

        // Input handler with debounce
        let debounceTimer;
        input.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const items = search(e.target.value);
                renderResults(items);
            }, 150);
        });

        // Keyboard navigation
        input.addEventListener('keydown', handleKeydown);

        // Close on backdrop click
        modal.querySelector('.search-modal-backdrop')?.addEventListener('click', closeModal);

        // Global keyboard shortcut: Cmd+K / Ctrl+K
        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                if (modal.hidden) {
                    openModal();
                } else {
                    closeModal();
                }
            }
        });

        // Focus trap
        modal.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                trapFocus(e);
            }
        });

        // Search trigger button
        document.querySelectorAll('.search-trigger').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                openModal();
            });
        });
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
