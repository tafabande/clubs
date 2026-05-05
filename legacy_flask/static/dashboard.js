// Vanilla JS dashboard for clubs: search, filter, join/exit, details modal.
(function(){
  const el = (id)=>document.getElementById(id);
  const listEl = el('clubsList');
  const searchEl = el('searchInput');
  const catEl = el('categoryFilter');
  const statClubs = el('statClubs');
  const statCats = el('statCats');
  const statJoined = el('statJoined');
  const modal = el('clubModal');
  const modalContent = el('modalContent');
  const modalClose = el('modalClose');

  let clubs = [];
  let filtered = [];

  function getJoined(){
    try { return new Set(JSON.parse(localStorage.getItem('joinedClubs')||'[]')); }
    catch { return new Set(); }
  }
  function setJoined(set){ localStorage.setItem('joinedClubs', JSON.stringify([...set])); updateStats(); }

  function norm(s){ return (s||'').toLowerCase(); }

  function synthesizeIds(arr){
    // Ensure each club has an id
    return arr.map((c, i)=>({ id: c.id ?? (i+1000), ...c }));
  }

  function loadClubs(){
    fetch('/api/clubs').then(r=>r.json()).then(data=>{
      clubs = synthesizeIds(data);
      initUI();
    }).catch(()=>{
      // fallback to static data if API not available
      if (window.CLUBS) {
        clubs = synthesizeIds(window.CLUBS);
        initUI();
      } else {
        listEl.innerHTML = '<p>Failed to load clubs.</p>';
      }
    });
  }

  function initUI(){
    // categories
    const cats = Array.from(new Set(clubs.map(c=>c.category||'Uncategorized'))).sort();
    catEl.innerHTML = '<option value="">All categories</option>' + cats.map(c=>`<option value="${c}">${c}</option>`).join('');
    // render
    applyFilters();
    // listeners
    searchEl.addEventListener('input', applyFilters);
    catEl.addEventListener('change', applyFilters);
    modalClose.addEventListener('click', closeModal);
    modal.addEventListener('click', (e)=>{ if(e.target===modal) closeModal(); });
    updateStats();
  }

  function updateStats(){
    const cats = new Set(clubs.map(c=>c.category||'Uncategorized'));
    statClubs.textContent = clubs.length;
    statCats.textContent = cats.size;
    statJoined.textContent = getJoined().size;
  }

  function applyFilters(){
    const q = norm(searchEl.value);
    const cat = catEl.value;
    filtered = clubs.filter(c=>{
      const matchesCat = !cat || (c.category||'Uncategorized')===cat;
      const blob = `${c.name} ${c.category||''} ${c.description||''}`.toLowerCase();
      const matchesQ = !q || blob.includes(q);
      return matchesCat && matchesQ;
    });
    renderList();
  }

  function renderList(){
    const joined = getJoined();
    if(!filtered.length){ listEl.innerHTML = '<p class="muted">No clubs match your filters.</p>'; return; }
    listEl.innerHTML = filtered.map(c=>{
      const isJoined = joined.has(c.id);
      const canDeregister = (window.SESSION_CLUB_ID && c.id===window.SESSION_CLUB_ID);
      return `
        <div class="club-card">
          <h3>${c.name}</h3>
          <p class="muted">${c.category||'Uncategorized'}</p>
          <p class="small">${(c.description||'').slice(0,120)}${(c.description||'').length>120?'…':''}</p>
          <div class="card-actions">
            <a class="btn btn-view" href="/clubs/${c.id}">View</a>
            <button class="btn btn-details" data-action="details" data-id="${c.id}">Details</button>
            <button class="btn ${isJoined?'btn-view':'btn-details'}" data-action="toggle" data-id="${c.id}">${isJoined?'Exit':'Join'}</button>
            ${canDeregister?`<button class="btn btn-view" data-action="deregister" data-id="${c.id}">Deregister</button>`:''}
          </div>
        </div>`;
    }).join('');

    // wire actions
    listEl.querySelectorAll('button[data-action]').forEach(btn=>{
      btn.addEventListener('click', (e)=>{
        const id = Number(e.currentTarget.getAttribute('data-id'));
        const action = e.currentTarget.getAttribute('data-action');
        if(action==='details') openDetails(id);
        if(action==='toggle') toggleJoin(id);
        if(action==='deregister') deregisterClub(id);
      });
    });
  }

  function openDetails(id){
    const c = clubs.find(x=>x.id===id);
    if(!c) return;
    modalContent.innerHTML = `
      <h3>${c.name}</h3>
      <p class="muted">${c.category||'Uncategorized'} · ${c.email||''}</p>
      ${c.description?`<p>${c.description}</p>`:''}
      <div class="stats-row">
        <div class="stat"><div>Members (latest)</div><div id="mMembers" class="stat-val">—</div></div>
        <div class="stat"><div>Events (YTD)</div><div id="mEvents" class="stat-val">—</div></div>
      </div>
      <div class="charts">
        <div class="chart-card"><canvas id="historyChart" height="180"></canvas></div>
        <div class="chart-card" id="historyTable">Loading…</div>
      </div>
    `;
    openModal();
    // load history
    fetch(`/api/clubs/${id}/history`).then(r=>r.json()).then(rows=>{
      if(!Array.isArray(rows) || !rows.length){ el('historyTable').textContent = 'No history available.'; return; }
      // fill quick stats
      const latest = rows[rows.length-1];
      el('mMembers').textContent = latest.members;
      el('mEvents').textContent = rows.reduce((s,r)=>s+(r.events||0),0);
      // simple table
      const t = document.createElement('table');
      t.style.width='100%'; t.style.borderCollapse='collapse';
      t.innerHTML = `<thead><tr><th style='text-align:left'>Date</th><th>Members</th><th>Events</th></tr></thead>`;
      const tb = document.createElement('tbody');
      rows.forEach(r=>{
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${new Date(r.date).toLocaleDateString()}</td><td style='text-align:center'>${r.members}</td><td style='text-align:center'>${r.events}</td>`;
        tb.appendChild(tr);
      });
      t.appendChild(tb);
      const ht = el('historyTable');
      ht.innerHTML='';
      ht.appendChild(t);
    }).catch(()=>{
      el('historyTable').textContent = 'Failed to load history.';
    });
  }

  function openModal(){ modal.classList.add('open'); modal.setAttribute('aria-hidden','false'); }
  function closeModal(){ modal.classList.remove('open'); modal.setAttribute('aria-hidden','true'); }

  function toggleJoin(id){
    const joined = getJoined();
    if(joined.has(id)) joined.delete(id); else joined.add(id);
    setJoined(joined);
    renderList();
  }

  function deregisterClub(id){
    if(!window.SESSION_CLUB_ID || id!==window.SESSION_CLUB_ID) return;
    if(confirm('This will deregister your club (demo only, no backend call). Continue?')){
      alert('Deregistered (frontend demo) — contact admin to finalize.');
    }
  }

  // init
  loadClubs();
})();
