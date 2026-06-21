document.addEventListener("DOMContentLoaded", async () => {
    // Elements
    const locationSelect = document.getElementById("location-select");
    const cuisineSelect = document.getElementById("cuisine-select");
    const form = document.getElementById("filter-form");
    
    const heroSection = document.getElementById("hero-section");
    const loadingState = document.getElementById("loading-state");
    const summaryContainer = document.getElementById("summary-container");
    const summaryText = document.getElementById("summary-text");
    const resultsGrid = document.getElementById("results-grid");

    // Rank badges map
    const rankBadges = ["🥇 Top Match", "🥈 Great Alternative", "🥉 Hidden Gem", "4️⃣ Solid Choice", "5️⃣ Worth Trying"];

    // 1. Fetch dropdown data
    try {
        const [locRes, cuiRes] = await Promise.all([
            fetch("/api/locations"),
            fetch("/api/cuisines")
        ]);
        
        const locations = await locRes.json();
        const cuisines = await cuiRes.json();
        
        // Populate locations
        locationSelect.innerHTML = `<option value="" disabled selected>Select a city...</option>`;
        locations.forEach(loc => {
            locationSelect.innerHTML += `<option class="bg-surface" value="${loc}">${loc}</option>`;
        });
        
        // Populate cuisines
        cuisineSelect.innerHTML = `<option value="">Any Cuisine</option>`;
        cuisines.forEach(cui => {
            cuisineSelect.innerHTML += `<option class="bg-surface" value="${cui}">${cui}</option>`;
        });
        
    } catch (err) {
        console.error("Failed to fetch initial data", err);
    }

    // 2. Handle Form Submission
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        // Hide previous results, show loader
        resultsGrid.innerHTML = "";
        summaryContainer.classList.add("hidden");
        heroSection.classList.add("hidden");
        loadingState.classList.remove("hidden");

        const formData = new FormData(form);
        const requestData = {
            location: formData.get("location"),
            budget: formData.get("budget"),
            min_rating: parseFloat(formData.get("min_rating")),
            cuisine: formData.get("cuisine") || null,
            additional: formData.get("additional") || null
        };

        try {
            const res = await fetch("/api/recommend", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestData)
            });

            if (!res.ok) {
                throw new Error("Failed to fetch recommendations");
            }

            const data = await res.json();
            
            // Hide loader
            loadingState.classList.add("hidden");
            
            // Display summary
            summaryText.textContent = data.summary || "Here are the top restaurants we found for you.";
            summaryContainer.classList.remove("hidden");

            // Display cards
            if (data.recommendations.length === 0) {
                resultsGrid.innerHTML = `<div class="col-span-full text-center py-12"><p class="text-xl text-on-surface-variant">No restaurants found matching those criteria.</p></div>`;
                return;
            }

            data.recommendations.forEach((rec, index) => {
                const badge = rankBadges[index] || `#${rec.rank}`;
                
                const cardHtml = `
                <article class="glass-card rounded-2xl overflow-hidden flex flex-col h-full animate-fade-up delay-${(index % 3) * 100}">
                    <!-- Card Header (No food image as requested) -->
                    <div class="p-6 pb-2 relative">
                        <div class="inline-flex items-center gap-1 bg-white/5 px-3 py-1 rounded-full border border-white/10 mb-4">
                            <span class="font-bold text-xs text-primary">${badge}</span>
                        </div>
                        <h2 class="text-2xl font-bold text-on-surface m-0 leading-tight">${rec.name}</h2>
                        <div class="flex items-center gap-2 mt-2">
                            <span class="material-symbols-outlined text-tertiary text-sm">star</span>
                            <span class="font-bold text-on-surface">${rec.rating}</span>
                        </div>
                    </div>
                    
                    <div class="p-6 pt-2 flex-1 flex flex-col gap-4">
                        <div class="flex flex-wrap gap-2">
                            <span class="px-2 py-1 rounded-md bg-white/5 border border-white/10 text-[10px] font-bold text-on-surface-variant uppercase tracking-wider">${rec.cuisine}</span>
                            <span class="px-2 py-1 rounded-md bg-tertiary/10 border border-tertiary/20 text-[10px] font-bold text-tertiary uppercase tracking-wider">₹${rec.estimated_cost} FOR TWO</span>
                        </div>
                        <div class="bg-surface-container-low rounded-xl p-4 border border-white/5 flex-1 relative mt-2">
                            <span class="material-symbols-outlined absolute top-2 right-2 text-primary/30 text-4xl pointer-events-none">format_quote</span>
                            <p class="text-sm text-on-surface-variant relative z-10 leading-relaxed">
                                <strong class="text-primary block mb-1">AI Insight</strong>
                                ${rec.explanation}
                            </p>
                        </div>
                    </div>
                </article>
                `;
                resultsGrid.innerHTML += cardHtml;
            });

        } catch (err) {
            console.error(err);
            loadingState.classList.add("hidden");
            resultsGrid.innerHTML = `<div class="col-span-full text-center py-12"><p class="text-xl text-error">An error occurred while fetching recommendations.</p></div>`;
        }
    });
});
