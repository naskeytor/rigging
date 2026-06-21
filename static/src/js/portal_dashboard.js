'use strict';

(function () {
    function init() {
        var card = document.querySelector('.rg_portal_card');
        if (!card) return;

        // stack entries: { html, activeHref }
        var stack = [];

        function bindAll() {
            // Clickable rows (dashboard tables + rigging history in detail views)
            card.querySelectorAll('tr[data-rg-href]').forEach(function (tr) {
                tr.addEventListener('click', function () {
                    navigate(tr.getAttribute('data-rg-href'));
                });
            });
            // Intercept <a href="/my/rigging/..."> links inside the card
            // (component links in rig detail, job component link, etc.)
            card.querySelectorAll('a[href^="/my/rigging/"]').forEach(function (a) {
                a.addEventListener('click', function (e) {
                    e.preventDefault();
                    navigate(a.getAttribute('href'));
                });
            });
        }

        function navigate(url) {
            var activeLink = card.querySelector('.nav-link.active');
            stack.push({
                html: card.innerHTML,
                activeHref: activeLink ? activeLink.getAttribute('href') : ''
            });

            // Show spinner in body while loading
            card.querySelector('.card-body').innerHTML =
                '<div class="text-center py-5">' +
                '<div class="spinner-border text-secondary" role="status">' +
                '<span class="visually-hidden">Loading…</span>' +
                '</div></div>';

            fetch(url)
                .then(function (r) { return r.text(); })
                .then(function (html) {
                    var doc = new DOMParser().parseFromString(html, 'text/html');
                    var content = doc.querySelector('.o_portal_rigging_dashboard');
                    if (!content) { location.href = url; return; }

                    // Remove the standalone "Back to Dashboard" button blocks
                    content.querySelectorAll('a.btn[href^="/my/rigging"]').forEach(function (a) {
                        var wrap = a.closest('.mb-3');
                        if (wrap) wrap.remove(); else a.remove();
                    });

                    // Replace card header with a Back bar
                    var header = card.querySelector('.card-header');
                    header.className = 'card-header rg-detail-header';
                    header.innerHTML =
                        '<button class="btn btn-sm btn-outline-secondary rg-back-btn" id="rg-back-btn">' +
                        '<i class="fa fa-arrow-left me-1"></i>Back</button>';

                    card.querySelector('.card-body').innerHTML = content.innerHTML;

                    document.getElementById('rg-back-btn').addEventListener('click', goBack);

                    // Bind rows and links inside the freshly-loaded content
                    bindAll();
                })
                .catch(function () { location.href = url; });
        }

        function goBack() {
            var entry = stack.pop();
            if (!entry) return;

            card.innerHTML = entry.html;

            // Re-bind everything in the restored content
            bindAll();

            if (stack.length === 0) {
                // Returning to dashboard: restore the active tab
                if (entry.activeHref) {
                    var link = card.querySelector('.nav-link[href="' + entry.activeHref + '"]');
                    if (link && window.bootstrap && bootstrap.Tab) {
                        new bootstrap.Tab(link).show();
                    }
                }
            } else {
                // Returning to an intermediate detail: re-wire back button
                var btn = document.getElementById('rg-back-btn');
                if (btn) btn.addEventListener('click', goBack);
            }
        }

        bindAll();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
