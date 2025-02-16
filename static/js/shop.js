document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    const productsGrid = document.getElementById('productsGrid');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const priceRange = document.getElementById('priceRange');
    const currentFilters = new URLSearchParams(window.location.search);
    let debounceTimer;

    // Load initial products and filter options
    if (!window.location.search) {
        // Only add ordering for initial load
        const params = new URLSearchParams();
        params.append('ordering', '-created_at');
        showLoading(true);
        fetchWithCsrf(`/api/products/?${params.toString()}`)
            .then(data => {
                updateProductsGrid(data);
                updatePagination(data);
                if (document.getElementById('resultsCount')) {
                    document.getElementById('resultsCount').textContent = `${data.count} produse`;
                }
                document.title = `Magazin (${data.count} produse) - Răsfățul Pescarului`;
            })
            .catch(error => {
                console.error('Error loading products:', error);
                showError('A apărut o eroare la încărcarea produselor. Te rugăm să reîncerci.');
                updateProductsGrid({ results: [] }); // Clear products grid
            })
            .finally(() => {
                showLoading(false);
            });
    } else {
        applyFilters();
    }
    loadFilterOptions();

    // Event listeners for filters
    filterForm.addEventListener('change', debounceSubmit);
    filterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        applyFilters();
    });

    // Price range slider
    if (priceRange) {
        const minPrice = document.getElementById('minPrice');
        const maxPrice = document.getElementById('maxPrice');
        
        noUiSlider.create(priceRange, {
            start: [
                parseInt(currentFilters.get('min_price')) || parseInt(minPrice.dataset.min),
                parseInt(currentFilters.get('max_price')) || parseInt(maxPrice.dataset.max)
            ],
            connect: true,
            range: {
                'min': parseInt(minPrice.dataset.min),
                'max': parseInt(maxPrice.dataset.max)
            },
            format: {
                to: value => Math.round(value),
                from: value => parseInt(value)
            }
        });

        priceRange.noUiSlider.on('update', function(values) {
            minPrice.value = values[0];
            maxPrice.value = values[1];
            document.getElementById('priceRangeLabel').innerHTML = 
                `${values[0]} Lei - ${values[1]} Lei`;
        });

        priceRange.noUiSlider.on('change', debounceSubmit);
    }

    // Mobile filter toggle
    document.getElementById('filterToggle')?.addEventListener('click', function() {
        const sidebar = document.getElementById('filterSidebar');
        sidebar.classList.toggle('show');
        document.body.classList.toggle('filter-open');
    });

    function debounceSubmit() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(applyFilters, 500);
    }

    async function loadFilterOptions() {
        try {
            const data = await fetchWithCsrf('/api/products/filter_options/');
            
            // Update price range
            if (priceRange && data.price_range) {
                const minPrice = document.getElementById('minPrice');
                const maxPrice = document.getElementById('maxPrice');
                minPrice.dataset.min = data.price_range.min_price;
                maxPrice.dataset.max = data.price_range.max_price;
                
                if (priceRange.noUiSlider) {
                    priceRange.noUiSlider.updateOptions({
                        range: {
                            'min': data.price_range.min_price,
                            'max': data.price_range.max_price
                        }
                    });
                }
            }

            // Update attribute filters
            data.attributes.forEach(attr => {
                const container = document.getElementById(`${attr.type}Filter`);
                if (container) {
                    container.innerHTML = attr.values.map(value => `
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" 
                                   name="attributes" value="${attr.name}:${value}"
                                   id="${attr.name}_${value}"
                                   ${currentFilters.getAll('attributes').includes(`${attr.name}:${value}`) ? 'checked' : ''}>
                            <label class="form-check-label" for="${attr.name}_${value}">
                                ${value}
                            </label>
                        </div>
                    `).join('');
                }
            });
        } catch (error) {
            console.error('Error loading filter options:', error);
            showError('A apărut o eroare la încărcarea opțiunilor de filtrare.');
        }
    }

    async function applyFilters(page = 1) {
        showLoading(true);
        
        try {
            let params = new URLSearchParams();
            
            // Check if we're applying filters from form or using URL params
            if (window.location.search && !page) {
                // If we have URL params and it's not a pagination request, use those
                params = new URLSearchParams(window.location.search);
            } else {
                // Get form data if available
                if (filterForm) {
                    const formData = new FormData(filterForm);
                    for (let [key, value] of formData.entries()) {
                        if (value) params.append(key, value);
                    }
                }
                
                // Add default sorting if not set
                if (!params.has('ordering')) {
                    params.append('ordering', '-created_at');
                }
                
                // Add price range if available
                if (priceRange && !params.has('min_price')) {
                    const [min, max] = priceRange.noUiSlider.get();
                    params.append('min_price', min);
                    params.append('max_price', max);
                }
                
                // Add page number if needed
                if (page > 1) {
                    params.append('page', page);
                }
            }

            // Update URL (only if not paginating)
            if (!page || page === 1) {
                const newUrl = `${window.location.pathname}?${params.toString()}`;
                window.history.pushState({}, '', newUrl);
            }

            // Fetch filtered products
            const data = await fetchWithCsrf(`/api/products/?${params.toString()}`);
            
            // Update products grid
            updateProductsGrid(data);
            
            // Update pagination
            updatePagination(data);
            
            // Update results count
            const resultsCount = document.getElementById('resultsCount');
            if (resultsCount) {
                resultsCount.textContent = `${data.count} produse`;
            }
            
            // Update page title
            document.title = `Magazin (${data.count} produse) - Răsfățul Pescarului`;
            
        } catch (error) {
            console.error('Error applying filters:', error);
            showError('A apărut o eroare la încărcarea produselor. Te rugăm să reîncerci.');
            updateProductsGrid({ results: [] }); // Clear products grid
        } finally {
            showLoading(false);
        }
    }

    function updateProductsGrid(data) {
        productsGrid.innerHTML = data.results.length ? data.results.map(product => `
            <div class="col">
                <div class="card h-100">
                    <img src="${product.image || '/static/images/product-placeholder.png'}" 
                         class="card-img-top" alt="${product.name}">
                    <div class="card-body">
                        <h5 class="card-title">${product.name}</h5>
                        <p class="card-text text-success fw-bold mb-2">${product.price} Lei</p>
                        <span class="badge ${product.stock_quantity > 0 ? 'bg-success' : 'bg-danger'} mb-2">
                            ${product.stock_quantity > 0 ? 'În stoc' : 'Stoc epuizat'}
                        </span>
                        <div class="d-grid gap-2">
                            <a href="/shop/product/${product.slug}/" class="btn btn-outline-success">
                                Vezi detalii
                            </a>
                            ${product.stock_quantity > 0 ? `
                                <form method="post" action="/cart/add/" class="d-grid">
                                    <input type="hidden" name="csrfmiddlewaretoken" value="${getCsrfToken()}">
                                    <input type="hidden" name="product_id" value="${product.id}">
                                    <input type="hidden" name="quantity" value="1">
                                    <button type="submit" class="btn btn-success">
                                        <i class="fas fa-shopping-cart me-2"></i>Adaugă în coș
                                    </button>
                                </form>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `).join('') : `
            <div class="col-12">
                <div class="alert alert-info">
                    Nu am găsit niciun produs care să corespundă criteriilor tale de căutare.
                </div>
            </div>
        `;
    }

    function updatePagination(data) {
        const pagination = document.getElementById('pagination');
        if (!pagination) return;

        const totalPages = Math.ceil(data.count / data.results.length);
        const currentPage = Math.floor(data.results.length / data.results.length) + 1;

        if (totalPages <= 1) {
            pagination.innerHTML = '';
            return;
        }

        let html = `
            <nav aria-label="Page navigation" class="mt-4">
                <ul class="pagination justify-content-center">
        `;

        // Previous button
        if (data.previous) {
            html += `
                <li class="page-item">
                    <a class="page-link" href="#" data-page="${currentPage - 1}">
                        <i class="fas fa-chevron-left"></i>
                    </a>
                </li>
            `;
        }

        // Page numbers
        for (let i = 1; i <= totalPages; i++) {
            if (
                i === 1 || i === totalPages ||
                (i >= currentPage - 2 && i <= currentPage + 2)
            ) {
                html += `
                    <li class="page-item ${i === currentPage ? 'active' : ''}">
                        <a class="page-link" href="#" data-page="${i}">${i}</a>
                    </li>
                `;
            } else if (
                i === currentPage - 3 || i === currentPage + 3
            ) {
                html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
        }

        // Next button
        if (data.next) {
            html += `
                <li class="page-item">
                    <a class="page-link" href="#" data-page="${currentPage + 1}">
                        <i class="fas fa-chevron-right"></i>
                    </a>
                </li>
            `;
        }

        html += `
                </ul>
            </nav>
        `;

        pagination.innerHTML = html;

        // Add click handlers
        pagination.querySelectorAll('.page-link[data-page]').forEach(link => {
            link.addEventListener('click', e => {
                e.preventDefault();
                applyFilters(parseInt(e.target.dataset.page));
            });
        });
    }

    function showLoading(show) {
        if (loadingSpinner) {
            loadingSpinner.style.display = show ? 'block' : 'none';
        }
        productsGrid.style.opacity = show ? '0.5' : '1';
    }

    function showError(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        document.querySelector('.container').insertBefore(alert, productsGrid);
    }

    function getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]').content;
    }

    async function fetchWithCsrf(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        };
        
        const response = await fetch(url, { ...defaultOptions, ...options });
        if (!response.ok) {
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                const error = await response.json();
                throw new Error(error.detail || `HTTP error! status: ${response.status}`);
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }
});
