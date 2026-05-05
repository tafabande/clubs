// socials.js — client-side feed renderer with persistent likes, comments, shares, and reports
(function(){
  const SOURCE = '../static/socials.json';
  const STORE_KEY = 'msu_socials_interactions_v1';

  function loadStore(){ try{ return JSON.parse(localStorage.getItem(STORE_KEY)||'{}') }catch(e){ return {} } }
  function saveStore(s){ localStorage.setItem(STORE_KEY, JSON.stringify(s)); }

  function timeAgo(iso){ const d=new Date(iso); const s=Math.floor((Date.now()-d)/1000); if(s<60) return s+'s'; if(s<3600) return Math.floor(s/60)+'m'; if(s<86400) return Math.floor(s/3600)+'h'; return Math.floor(s/86400)+'d'; }

  function el(tag, cls, html){ const e=document.createElement(tag); if(cls) e.className=cls; if(html!==undefined) e.innerHTML = html; return e }

  function renderPost(post, store){
    const id = post.id;
    const interaction = store[id] || {likes: post.likes||0, liked:false, comments: post.comments||[], shared:0, reported:false};

    const article = el('article','post');

    // header
    const ph = el('header','post-header');
    const avatar = el('div','avatar', post.avatar || '🟣');
    const meta = el('div','meta');
    meta.innerHTML = `<div class="club">${post.club}</div><div class="sub muted">${post.location} • ${timeAgo(post.time)}</div>`;
    const type = el('div','post-type', post.type);
    ph.appendChild(avatar); ph.appendChild(meta); ph.appendChild(type);

    // body
    const body = el('div','post-body', post.content);
    if(post.image){ const pm = el('div','post-media'); const img = el('img'); img.src = post.image; img.alt = post.club + ' media'; pm.appendChild(img); article.appendChild(pm); }

    // actions
    const actions = el('div','post-actions');
    const likeBtn = el('button','like-btn', `❤ <span class="likes">${interaction.likes}</span>`);
    if(interaction.liked) likeBtn.classList.add('liked');
    const commentBtn = el('button','comment-btn', `💬 <span class="comments">${interaction.comments.length||0}</span>`);
    const shareBtn = el('button','share-btn', `↗ Share <span class="shares">${interaction.shared||0}</span>`);
    const reportBtn = el('button','report-btn', interaction.reported ? '⚑ Reported' : '⚑ Report');
    actions.appendChild(likeBtn); actions.appendChild(commentBtn); actions.appendChild(shareBtn); actions.appendChild(reportBtn);

    // comments area
    const commentsWrap = el('div','comments-wrap');
    const commentsList = el('div','comments-list');
    function redrawComments(){ commentsList.innerHTML=''; (interaction.comments||[]).forEach(c=>{ const co = el('div','comment'); co.innerHTML = `<strong>${escapeHtml(c.author||'Anon')}</strong> <span class="muted">• ${escapeHtml(c.time||'')}</span><div class="comment-text">${escapeHtml(c.text)}</div>`; commentsList.appendChild(co); }); }
    redrawComments();
    const commentForm = el('form','comment-form');
    commentForm.innerHTML = `<input class="comment-input" placeholder="Write a comment..." /><button class="btn btn-primary" type="submit">Comment</button>`;
    commentsWrap.appendChild(commentsList); commentsWrap.appendChild(commentForm);

    // assemble
    article.appendChild(ph); article.appendChild(body); article.appendChild(actions); article.appendChild(commentsWrap);

    // interactions
    likeBtn.addEventListener('click', ()=>{
      interaction.liked = !interaction.liked;
      interaction.likes = Math.max(0,(interaction.likes || 0) + (interaction.liked ? 1 : -1));
      likeBtn.querySelector('.likes').textContent = interaction.likes;
      likeBtn.classList.toggle('liked', interaction.liked);
      store[id] = interaction; saveStore(store);
    });

    commentForm.addEventListener('submit', e=>{
      e.preventDefault(); const input = commentForm.querySelector('.comment-input'); const txt = input.value && input.value.trim(); if(!txt) return; const cobj = {author: (JSON.parse(localStorage.getItem('msu_user')||'{}').email) || 'Student', text: txt, time: new Date().toLocaleString('en-ZW')};
      interaction.comments = interaction.comments || [];
      interaction.comments.push(cobj);
      commentForm.querySelector('.comment-input').value = '';
      commentsList.innerHTML=''; redrawComments(); commentBtn.querySelector('.comments').textContent = interaction.comments.length;
      store[id] = interaction; saveStore(store);
    });

    shareBtn.addEventListener('click', ()=>{
      const url = location.origin + location.pathname + '#post-' + id;
      navigator.clipboard && navigator.clipboard.writeText(url).then(()=>{
        interaction.shared = (interaction.shared||0) + 1; shareBtn.querySelector('.shares').textContent = interaction.shared; store[id] = interaction; saveStore(store); alert('Post link copied to clipboard');
      }).catch(()=>{ prompt('Copy this link', url); });
    });

    reportBtn.addEventListener('click', ()=>{
      if(confirm('Report this post as inappropriate?')){ interaction.reported = true; reportBtn.textContent = '⚑ Reported'; reportBtn.disabled = true; store[id] = interaction; saveStore(store); alert('Post reported (local only).'); }
    });

    return article;
  }

  function escapeHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\"/g,'&quot;').replace(/\'/g,'&#39;'); }

  // boot
  document.addEventListener('DOMContentLoaded', ()=>{
    const feed = document.getElementById('feed'); if(!feed) return; feed.innerHTML = 'Loading feed…';
    const store = loadStore();
    fetch(SOURCE).then(r=>r.json()).then(posts=>{
      feed.innerHTML=''; posts.sort((a,b)=> new Date(b.time) - new Date(a.time));
      posts.forEach(p=>{
        const node = renderPost(p, store);
        node.id = 'post-' + p.id;
        feed.appendChild(node);
      });
    }).catch(err=>{ console.error(err); feed.textContent = 'Failed to load feed.' });
  });
})();
