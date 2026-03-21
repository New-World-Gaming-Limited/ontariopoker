/* ============================================
   ONTARIO POKER - Shared JavaScript
   ============================================ */

// --- THEME TOGGLE ---
(function(){
  var toggle = document.querySelector('[data-theme-toggle]');
  var htmlEl = document.documentElement;
  var theme = window.matchMedia('(prefers-color-scheme:dark)').matches ? 'dark' : 'light';
  htmlEl.setAttribute('data-theme', theme);
  updateToggleIcon();

  if (toggle) {
    toggle.addEventListener('click', function() {
      theme = theme === 'dark' ? 'light' : 'dark';
      htmlEl.setAttribute('data-theme', theme);
      toggle.setAttribute('aria-label', 'Switch to ' + (theme === 'dark' ? 'light' : 'dark') + ' mode');
      updateToggleIcon();
    });
  }

  function updateToggleIcon() {
    if (!toggle) return;
    toggle.innerHTML = theme === 'dark'
      ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
      : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  }
})();

// --- MOBILE MENU ---
(function(){
  var btn = document.querySelector('.mobile-menu-btn');
  var nav = document.querySelector('.mobile-nav');
  if (!btn || !nav) return;

  btn.addEventListener('click', function() {
    var isOpen = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', isOpen);
    btn.innerHTML = isOpen
      ? '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>'
      : '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>';
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  nav.querySelectorAll('a').forEach(function(a) {
    a.addEventListener('click', function() {
      nav.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
      btn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>';
      document.body.style.overflow = '';
    });
  });
})();

// --- FAQ ACCORDION ---
document.querySelectorAll('.faq-question').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var item = btn.closest('.faq-item');
    var wasOpen = item.classList.contains('open');
    var list = item.closest('.faq-list');
    if (list) list.querySelectorAll('.faq-item').forEach(function(i) { i.classList.remove('open'); });
    if (!wasOpen) item.classList.add('open');
  });
});

// --- SCROLL REVEALS ---
(function(){
  var reveals = document.querySelectorAll('.reveal');
  if (!reveals.length) return;
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  reveals.forEach(function(el) {
    el.classList.add('reveal-init');
    observer.observe(el);
  });
})();

// --- SCORE BAR ANIMATION ---
(function(){
  var bars = document.querySelectorAll('.score-bar-fill');
  if (!bars.length) return;
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        var width = entry.target.getAttribute('data-width');
        entry.target.style.width = width + '%';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });
  bars.forEach(function(bar) {
    bar.style.width = '0';
    observer.observe(bar);
  });
})();

// --- COPY PROMO CODE + REDIRECT ---
var AFFILIATE_URLS = {
  'ggpoker': '#',
  '888poker': '#',
  'betmgm-poker': '#',
  'pokerstars': '#',
  'partypoker': '#',
  'bwin': '#'
};

function getAffiliateUrl() {
  var path = window.location.pathname.toLowerCase();
  if (path.indexOf('/888poker') !== -1) return AFFILIATE_URLS['888poker'];
  if (path.indexOf('/betmgm') !== -1) return AFFILIATE_URLS['betmgm-poker'];
  if (path.indexOf('/pokerstars') !== -1) return AFFILIATE_URLS['pokerstars'];
  if (path.indexOf('/partypoker') !== -1) return AFFILIATE_URLS['partypoker'];
  if (path.indexOf('/bwin') !== -1) return AFFILIATE_URLS['bwin'];
  return AFFILIATE_URLS['ggpoker'];
}

function copyAndRedirect(btn) {
  var code = btn.getAttribute('data-code') || '';
  var url = btn.getAttribute('data-url') || getAffiliateUrl();
  if (code) {
    navigator.clipboard.writeText(code).catch(function() {
      var ta = document.createElement('textarea');
      ta.value = code;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    });
  }
  btn.classList.add('copied');
  var orig = btn.innerHTML;
  btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Copied! Redirecting...';
  setTimeout(function() {
    btn.classList.remove('copied');
    btn.innerHTML = orig;
  }, 2000);
  setTimeout(function() {
    window.open(url, '_blank', 'noopener,noreferrer');
  }, 400);
}

document.querySelectorAll('.copy-btn').forEach(function(btn) {
  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    copyAndRedirect(btn);
  });
});

document.querySelectorAll('.promo-code-cutout').forEach(function(box) {
  box.style.cursor = 'pointer';
  box.setAttribute('role', 'button');
  box.setAttribute('tabindex', '0');
  box.addEventListener('click', function(e) {
    if (e.target.closest('.copy-btn')) return;
    var btn = box.querySelector('.copy-btn');
    if (btn) copyAndRedirect(btn);
  });
  box.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      var btn = box.querySelector('.copy-btn');
      if (btn) copyAndRedirect(btn);
    }
  });
});

// --- ACTIVE NAV HIGHLIGHT ---
(function(){
  var currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-desktop a, .mobile-nav a').forEach(function(a) {
    var href = a.getAttribute('href');
    if (href === currentPage || (currentPage === 'index.html' && href === './')) {
      a.classList.add('active');
    }
  });
})();

// --- DYNAMIC DATES ---
(function(){
  var now = new Date();
  var months = ['January','February','March','April','May','June',
                'July','August','September','October','November','December'];
  var month = months[now.getMonth()];
  var year = now.getFullYear();
  var day = now.getDate();
  var fullDate = month + ' ' + day + ', ' + year;
  var monthYear = month + ' ' + year;

  document.querySelectorAll('.dynamic-date-full').forEach(function(el){
    el.textContent = fullDate;
  });
  document.querySelectorAll('.dynamic-month-year').forEach(function(el){
    el.textContent = monthYear;
  });

  var isoDate = now.getFullYear() + '-' +
    String(now.getMonth()+1).padStart(2,'0') + '-' +
    String(now.getDate()).padStart(2,'0');
  document.querySelectorAll('script[type="application/ld+json"]').forEach(function(s){
    try {
      var data = JSON.parse(s.textContent);
      if (data.dateModified) {
        data.dateModified = isoDate;
        s.textContent = JSON.stringify(data);
      }
    } catch(e) {}
  });
})();

// --- FOOTER ACCORDION (MOBILE) ---
(function(){
  document.querySelectorAll('.footer-col-toggle').forEach(function(toggle){
    toggle.addEventListener('click', function(){
      if(window.innerWidth >= 768) return;
      var col = this.closest('.footer-col');
      if(col) col.classList.toggle('open');
    });
  });
})();

// --- SITE SEARCH ---
(function(){
  var overlay = document.getElementById('searchOverlay');
  if(!overlay) return;
  var input = overlay.querySelector('.search-input');
  var resultsDiv = overlay.querySelector('.search-results');
  var index = null;
  var activeIdx = -1;

  var base = '';
  var path = window.location.pathname;
  if(path.match(/\/[^\/]+\/[^\/]+\.html/)){
    base = '../';
  } else {
    base = './';
  }

  function loadIndex(){
    if(index) return Promise.resolve(index);
    return fetch(base + 'search-index.json')
      .then(function(r){
        if(!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function(data){index = data; return data;})
      .catch(function(){
        var paths = ['./search-index.json','../search-index.json','/search-index.json'];
        return paths.reduce(function(p, tryPath){
          return p.catch(function(){
            return fetch(tryPath).then(function(r){
              if(!r.ok) throw new Error('HTTP ' + r.status);
              return r.json();
            }).then(function(data){index = data; return data;});
          });
        }, Promise.reject());
      });
  }

  function openSearch(){
    overlay.classList.add('open');
    input.value = '';
    resultsDiv.innerHTML = '<div class="search-hint">Search reviews, guides, and promotions</div>';
    activeIdx = -1;
    setTimeout(function(){input.focus();},100);
    loadIndex();
  }

  function closeSearch(){
    overlay.classList.remove('open');
    input.value = '';
    activeIdx = -1;
  }

  document.querySelectorAll('.search-btn').forEach(function(btn){
    btn.addEventListener('click', function(e){e.preventDefault();openSearch();});
  });

  document.addEventListener('keydown', function(e){
    if((e.metaKey||e.ctrlKey) && e.key === 'k'){e.preventDefault();openSearch();}
    if(e.key === 'Escape' && overlay.classList.contains('open')){closeSearch();}
  });

  overlay.addEventListener('click', function(e){
    if(e.target === overlay) closeSearch();
  });

  overlay.querySelector('.search-close').addEventListener('click', closeSearch);

  input.addEventListener('input', function(){
    if(!index) return;
    var q = input.value.trim().toLowerCase();
    if(!q){
      resultsDiv.innerHTML = '<div class="search-hint">Search reviews, guides, and promotions</div>';
      activeIdx = -1;
      return;
    }
    var words = q.split(/\s+/);
    var scored = index.map(function(p){
      var hay = (p.title + ' ' + p.h1 + ' ' + p.desc + ' ' + p.h2s).toLowerCase();
      var score = 0;
      words.forEach(function(w){
        if(p.title.toLowerCase().indexOf(w) !== -1) score += 10;
        if(p.h1.toLowerCase().indexOf(w) !== -1) score += 8;
        if(p.desc.toLowerCase().indexOf(w) !== -1) score += 3;
        if(p.h2s.toLowerCase().indexOf(w) !== -1) score += 2;
      });
      return {page:p, score:score};
    }).filter(function(s){return s.score > 0;})
      .sort(function(a,b){return b.score - a.score;})
      .slice(0,10);

    if(!scored.length){
      resultsDiv.innerHTML = '<div class="search-empty">No results for "'+q+'"</div>';
      activeIdx = -1;
      return;
    }

    resultsDiv.innerHTML = scored.map(function(s,i){
      return '<a class="search-result" href="' + base + s.page.url + '" data-idx="'+i+'">' +
        '<div class="search-result-cat">' + s.page.cat + '</div>' +
        '<div class="search-result-title">' + s.page.title + '</div>' +
        '<div class="search-result-desc">' + s.page.desc + '</div>' +
        '</a>';
    }).join('');
    activeIdx = -1;
  });

  input.addEventListener('keydown', function(e){
    var items = resultsDiv.querySelectorAll('.search-result');
    if(!items.length) return;
    if(e.key === 'ArrowDown'){
      e.preventDefault();
      activeIdx = Math.min(activeIdx + 1, items.length - 1);
      items.forEach(function(el,i){el.classList.toggle('active', i === activeIdx);});
      items[activeIdx].scrollIntoView({block:'nearest'});
    } else if(e.key === 'ArrowUp'){
      e.preventDefault();
      activeIdx = Math.max(activeIdx - 1, 0);
      items.forEach(function(el,i){el.classList.toggle('active', i === activeIdx);});
      items[activeIdx].scrollIntoView({block:'nearest'});
    } else if(e.key === 'Enter' && activeIdx >= 0){
      e.preventDefault();
      items[activeIdx].click();
    }
  });
})();

// --- STICKY CTA BAR ---
(function(){
  var cta = document.getElementById('stickyCta');
  if (!cta) return;
  var shown = false;
  function checkScroll() {
    if (window.scrollY > 400 && !shown) {
      cta.classList.add('visible');
      shown = true;
    }
  }
  window.addEventListener('scroll', checkScroll, {passive: true});
  checkScroll();
})();

// --- COMPARISON TABLE SCROLL HINT ---
document.querySelectorAll('.compare-table-wrap').forEach(function(wrap) {
  wrap.addEventListener('scroll', function() {
    if (this.scrollLeft > 20) {
      this.classList.add('scrolled');
    }
  }, { passive: true });
});
