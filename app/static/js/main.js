/**
 * Krishi Kendra - Global Client Scripts
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Auto-dismiss alerts after 5 seconds
  setTimeout(function () {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    });
  }, 6000);

  // 2. Profile Pop-up Modal Handler (Strict Privacy Enforcement)
  const profileLinks = document.querySelectorAll('.trigger-profile-popup');
  profileLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      const userId = this.getAttribute('data-user-id');
      fetchUserProfilePopup(userId);
    });
  });

  // 3. Dynamic Mandi Rate & Deal Indicator on Offer Inputs
  const commodityInput = document.getElementById('offer-commodity-select');
  const priceInput = document.getElementById('offer-price-input');
  const unitSelect = document.getElementById('offer-unit-select');

  if (commodityInput && priceInput) {
    function updateMandiAnalysis() {
      const commodity = commodityInput.value;
      const price = parseFloat(priceInput.value) || 0;
      const unit = unitSelect ? unitSelect.value : 'kg';

      if (!commodity) return;

      // Fetch benchmark rate
      fetch(`/api/mandi-rate-lookup?commodity=${encodeURIComponent(commodity)}`)
        .then(res => res.json())
        .then(data => {
          const benchmarkEl = document.getElementById('mandi-benchmark-display');
          if (benchmarkEl) {
            benchmarkEl.innerHTML = `<strong>${data.market_name}:</strong> ₹${data.rate_per_kg}/kg (₹${data.raw_modal_price}/${data.unit})`;
          }

          // Fetch deal fairness analysis
          if (price > 0) {
            fetch('/api/analyze-deal', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ commodity: commodity, offered_price: price, unit: unit })
            })
              .then(res => res.json())
              .then(analysis => {
                const analysisEl = document.getElementById('deal-analysis-badge');
                if (analysisEl) {
                  analysisEl.className = `alert alert-${analysis.status === 'good' ? 'success' : (analysis.status === 'negotiate' ? 'warning' : 'danger')} py-2 px-3 mt-2 text-sm`;
                  analysisEl.innerHTML = `<strong>${analysis.tag}</strong>: ${analysis.recommendation}`;
                  analysisEl.style.display = 'block';
                }
              });
          }
        });
    }

    commodityInput.addEventListener('change', updateMandiAnalysis);
    priceInput.addEventListener('input', updateMandiAnalysis);
    if (unitSelect) unitSelect.addEventListener('change', updateMandiAnalysis);
  }
});

function fetchUserProfilePopup(userId) {
  fetch(`/api/user-popup/${userId}`)
    .then(res => res.json())
    .then(data => {
      document.getElementById('popup-user-name').textContent = data.name;
      document.getElementById('popup-user-id').textContent = data.custom_id;
      document.getElementById('popup-user-role').textContent = data.role;
      document.getElementById('popup-user-location').textContent = `${data.district}, ${data.state}`;
      document.getElementById('popup-user-bio').textContent = data.bio || 'Verified agricultural trade participant.';
      
      const badge = document.getElementById('popup-user-badge');
      if (data.is_verified) {
        badge.innerHTML = `<span class="badge badge-verified"><i class="fas fa-check-circle"></i> Verified ${data.role}</span>`;
      } else {
        badge.innerHTML = `<span class="badge bg-secondary">Registered User</span>`;
      }

      const phoneContainer = document.getElementById('popup-phone-container');
      if (data.phone_shared && data.phone) {
        phoneContainer.innerHTML = `<a href="tel:${data.phone}" class="btn btn-sm btn-outline-success"><i class="fas fa-phone"></i> Call ${data.phone}</a>`;
      } else {
        phoneContainer.innerHTML = `<small class="text-muted"><i class="fas fa-lock"></i> Phone hidden (Private by Default)</small>`;
      }

      const modalEl = document.getElementById('userProfileModal');
      if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
      }
    });
}
