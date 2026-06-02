from shiny import App, ui
from pathlib import Path

# ---------------------------------------------------------------------------
# Static JS - all JavaScript in one place, injected at render time
# ---------------------------------------------------------------------------
_STATIC_JS = """
(function() {
  // ---- NAV SCROLL --------------------------------------------------------
  var navLinks = document.querySelectorAll('.nav-pill');
  var shell = document.querySelector('.pitch-shell');

  navLinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      // In full mode, handle scroll here; in summary mode, goFull handles it
      if (shell.classList.contains('mode-full')) {
        var target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
      navLinks.forEach(function(l) { l.classList.remove('active'); });
      this.classList.add('active');
    });
  });

  // ---- ACTIVE NAV ON SCROLL ----------------------------------------------
  var sections = document.querySelectorAll('.pitch-section');
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        var id = entry.target.id;
        navLinks.forEach(function(l) {
          l.classList.toggle('active', l.getAttribute('href') === '#' + id);
        });
      }
    });
  }, { rootMargin: '-30% 0px -60% 0px' });
  sections.forEach(function(s) { observer.observe(s); });

  // ---- BACKLOG TOGGLE ----------------------------------------------------
  document.querySelectorAll('.backlog-team-header').forEach(function(hdr) {
    hdr.addEventListener('click', function() {
      var body = this.nextElementSibling;
      var icon = this.querySelector('.expand-icon');
      var isOpen = body.style.display !== 'none';
      body.style.display = isOpen ? 'none' : 'block';
      icon.textContent = isOpen ? '+' : '-';
    });
  });

  // ---- DISCOVERY Q REVEAL ------------------------------------------------
  document.querySelectorAll('.disc-question').forEach(function(q) {
    q.addEventListener('click', function() {
      var reveal = this.querySelector('.disc-reveal');
      var wasOpen = reveal.style.display === 'block';
      document.querySelectorAll('.disc-reveal').forEach(function(r) {
        r.style.display = 'none';
      });
      document.querySelectorAll('.disc-question').forEach(function(dq) {
        dq.classList.remove('open');
      });
      if (!wasOpen) {
        reveal.style.display = 'block';
        this.classList.add('open');
      }
    });
  });

  // ---- AUTO-RESIZE CALCULATOR IFRAMES ------------------------------------
  window.addEventListener('message', function(e) {
    if (e.data && e.data.type === 'iframeResize') {
      var iframes = document.querySelectorAll('iframe');
      iframes.forEach(function(f) {
        if (f.contentWindow === e.source) {
          f.style.height = e.data.height + 'px';
        }
      });
    }
  });

  // ---- MODE TOGGLE -------------------------------------------------------
  var expandBtn = document.getElementById('expand-btn');
  var collapseBtn = document.getElementById('collapse-btn');

  function goFull(scrollTargetId) {
    shell.classList.remove('mode-summary');
    shell.classList.add('mode-full');
    setTimeout(function() {
      var t = scrollTargetId ? document.querySelector(scrollTargetId) : document.getElementById('full-view');
      if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 50);
  }

  function goSummary() {
    shell.classList.remove('mode-full');
    shell.classList.add('mode-summary');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  if (expandBtn) expandBtn.addEventListener('click', function(e) {
    e.preventDefault();
    goFull('#opening');
  });

  if (collapseBtn) collapseBtn.addEventListener('click', function(e) {
    e.preventDefault();
    goSummary();
  });

  // Nav auto-expand: if a nav link fires while in summary mode, let goFull handle scroll
  navLinks.forEach(function(link) {
    link.addEventListener('click', function() {
      if (shell.classList.contains('mode-summary')) {
        goFull(this.getAttribute('href'));
      }
    });
  });

})();
"""

def _build_js():
    return _STATIC_JS

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600&family=Source+Code+Pro:wght@400;500;600&display=swap');

:root {
  --blue:       #447099;
  --blue-lt:    #d0dde9;
  --blue-bg:    #eef3f8;
  --blue-dk:    #2d5278;
  --orange:     #ee6331;
  --orange-lt:  #fde8df;
  --orange-dk:  #c94e1f;
  --teal:       #419599;
  --green:      #729943;
  --gray:       #404041;
  --gray-lt:    #c2c2c4;
  --gray-bg:    #f4f4f4;
  --black:      #151515;
  --border:     #d4d4d5;
  --bg:         #f6f7f8;
  --card:       #ffffff;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }

body {
  font-family: 'Open Sans', sans-serif;
  font-weight: 400;
  color: var(--black);
  background: var(--bg);
  font-size: 15px;
  line-height: 1.65;
}

/* ---- LAYOUT ---- */
.pitch-shell {
  display: flex;
  min-height: 100vh;
}

/* ---- SIDEBAR NAV ---- */
.pitch-nav {
  width: 220px;
  flex-shrink: 0;
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  background: var(--card);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  z-index: 100;
  overflow-y: auto;
}
.nav-brand {
  padding: 1.5rem 1.25rem 1.1rem;
  border-bottom: 2.5px solid var(--blue);
}
.nav-logo {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.5rem;
}
.nav-logo-mark {
  width: 28px;
  height: 28px;
  background: var(--blue);
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Source Code Pro', monospace;
  font-weight: 600;
  font-size: 13px;
  color: #fff;
  flex-shrink: 0;
}
.nav-brand-name {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--blue);
}
.nav-doc-label {
  font-size: 10px;
  color: var(--gray);
  font-family: 'Source Code Pro', monospace;
  line-height: 1.4;
}
.nav-pills {
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.nav-section-label {
  font-family: 'Source Code Pro', monospace;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gray-lt);
  padding: 0.6rem 0.5rem 0.3rem;
  margin-top: 0.25rem;
}
.nav-pill {
  display: block;
  padding: 0.45rem 0.75rem;
  border-radius: 5px;
  font-size: 13px;
  color: var(--gray);
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
  line-height: 1.3;
}
.nav-pill:hover { background: var(--blue-bg); color: var(--blue); }
.nav-pill.active { background: var(--blue-bg); color: var(--blue); font-weight: 600; }

/* ---- MAIN CONTENT ---- */
.pitch-main {
  margin-left: 220px;
  flex: 1;
  max-width: 860px;
}

.pitch-section {
  padding: 4rem 3rem 3.5rem;
  border-bottom: 1px solid var(--border);
}
.pitch-section:last-child { border-bottom: none; }

/* ---- SECTION HEADERS ---- */
.section-eyebrow {
  font-family: 'Source Code Pro', monospace;
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--blue);
  margin-bottom: 0.6rem;
}
.section-title {
  font-size: clamp(1.4rem, 2.5vw, 1.9rem);
  font-weight: 300;
  line-height: 1.2;
  letter-spacing: -0.01em;
  margin-bottom: 1.25rem;
  color: var(--black);
}
.section-title strong { font-weight: 600; color: var(--blue); }
.section-title em { font-style: normal; color: var(--orange); font-weight: 600; }

/* ---- OPENING / HERO ---- */
.opening-hero {
  background: var(--blue);
  border-radius: 12px;
  padding: 2.5rem 2.5rem 2.25rem;
  color: #fff;
  margin-bottom: 1.5rem;
}
.opening-hero-eyebrow {
  font-family: 'Source Code Pro', monospace;
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.5);
  margin-bottom: 1rem;
}
.opening-statement {
  font-size: clamp(1.2rem, 2.2vw, 1.6rem);
  font-weight: 300;
  line-height: 1.4;
  color: #fff;
  max-width: 62ch;
}
.opening-statement strong { font-weight: 600; }
.opening-kicker {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255,255,255,0.18);
  font-family: 'Source Code Pro', monospace;
  font-size: 13px;
  color: rgba(255,255,255,0.7);
  font-style: italic;
}

.stat-strip {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1.5rem;
}
.stat-cell {
  background: var(--card);
  padding: 1.25rem 1.5rem;
}
.stat-num {
  font-family: 'Source Code Pro', monospace;
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--blue);
  line-height: 1;
  margin-bottom: 0.3rem;
}
.stat-num.orange { color: var(--orange); }
.stat-label { font-size: 0.8rem; color: var(--gray); line-height: 1.4; }

.body-copy { font-size: 0.93rem; color: var(--gray); line-height: 1.8; margin-bottom: 1.1rem; max-width: 72ch; }
.body-copy strong { color: var(--black); font-weight: 600; }
.body-copy em { font-style: normal; color: var(--blue); font-weight: 600; }

/* ---- CALLOUT BOX ---- */
.callout {
  border-left: 3px solid var(--orange);
  background: var(--orange-lt);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.25rem;
  margin: 1.25rem 0;
}
.callout p { font-size: 0.9rem; color: var(--gray); line-height: 1.7; }
.callout p strong { color: var(--orange-dk); }

.callout.blue {
  border-left-color: var(--blue);
  background: var(--blue-bg);
}
.callout.blue p strong { color: var(--blue-dk); }

.callout.green {
  border-left-color: var(--green);
  background: #f0f5e8;
}
.callout.green p strong { color: #4a6b28; }

/* ---- PILLARS ---- */
.pillars-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin: 1.5rem 0;
}
.pillar-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.35rem 1.25rem;
}
.pillar-num {
  font-family: 'Source Code Pro', monospace;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--blue);
  margin-bottom: 0.5rem;
}
.pillar-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--black);
  margin-bottom: 0.5rem;
}
.pillar-body { font-size: 0.82rem; color: var(--gray); line-height: 1.6; }

/* ---- BACKLOG ---- */
.backlog-team {
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 0.75rem;
}
.backlog-team-header {
  background: var(--blue-bg);
  padding: 0.85rem 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
}
.backlog-team-header:hover { background: var(--blue-lt); }
.backlog-team-name {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--blue);
}
.backlog-team-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.backlog-badge {
  font-family: 'Source Code Pro', monospace;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 4px;
  background: var(--orange-lt);
  color: var(--orange-dk);
}
.backlog-badge.hyp {
  background: var(--gray-bg);
  color: var(--gray-lt);
}
.expand-icon {
  font-family: 'Source Code Pro', monospace;
  font-size: 16px;
  color: var(--blue);
  width: 20px;
  text-align: center;
}
.backlog-team-body {
  padding: 0;
}
.backlog-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 0.85rem 1.25rem;
  border-top: 1px solid var(--border);
}
.backlog-item-icon {
  font-family: 'Source Code Pro', monospace;
  font-size: 10px;
  font-weight: 600;
  color: var(--gray-lt);
  padding-top: 3px;
  min-width: 18px;
}
.backlog-item-body { flex: 1; }
.backlog-item-name { font-size: 0.88rem; font-weight: 600; color: var(--black); margin-bottom: 0.2rem; }
.backlog-item-desc { font-size: 0.78rem; color: var(--gray); line-height: 1.5; }
.backlog-item-tags { display: flex; gap: 0.4rem; margin-top: 0.4rem; flex-wrap: wrap; }
.tag {
  font-family: 'Source Code Pro', monospace;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 2px 7px;
  border-radius: 4px;
}
.tag-quick { background: #e8f3de; color: #4a6b28; }
.tag-shared { background: var(--blue-bg); color: var(--blue-dk); }
.tag-posit { background: #fff3e0; color: #8a5200; }
.tag-caution { background: var(--orange-lt); color: var(--orange-dk); }
.tag-hyp { background: var(--gray-bg); color: var(--gray); }

/* ---- WHY ME ---- */
.credential-pair {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin: 1.5rem 0;
}
.credential-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.35rem 1.25rem;
}
.credential-num {
  font-family: 'Source Code Pro', monospace;
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--orange);
  margin-bottom: 0.5rem;
}
.credential-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--black);
  margin-bottom: 0.5rem;
}
.credential-body { font-size: 0.82rem; color: var(--gray); line-height: 1.6; }
.credential-body strong { color: var(--black); }

/* ---- DISCOVERY QUESTIONS ---- */
.disc-question {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.85rem 1.1rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
  position: relative;
}
.disc-question:hover { border-color: var(--blue-lt); background: var(--blue-bg); }
.disc-question.open { border-color: var(--blue); background: var(--blue-bg); }
.disc-q-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 1rem;
}
.disc-q-num {
  font-family: 'Source Code Pro', monospace;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--gray-lt);
  flex-shrink: 0;
}
.disc-q-text { font-size: 0.88rem; font-weight: 500; color: var(--black); flex: 1; }
.disc-q-chevron { font-size: 10px; color: var(--gray-lt); flex-shrink: 0; }
.disc-reveal {
  display: none;
  margin-top: 0.65rem;
  padding-top: 0.65rem;
  border-top: 1px solid var(--blue-lt);
  font-size: 0.8rem;
  color: var(--gray);
  line-height: 1.65;
}
.disc-reveal strong { color: var(--blue); }

/* ---- ASK / CLOSE ---- */
.ask-band {
  background: var(--blue);
  border-radius: 12px;
  padding: 2.25rem 2.5rem;
  color: #fff;
  margin-bottom: 1.5rem;
}
.ask-band p {
  font-size: 0.97rem;
  font-weight: 300;
  line-height: 1.8;
  max-width: 68ch;
  margin-bottom: 0.75rem;
}
.ask-band p:last-child { margin-bottom: 0; }
.ask-band strong { font-weight: 600; }
.ask-items {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin: 1.25rem 0;
}
.ask-item {
  background: rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 1rem 1.1rem;
}
.ask-item-label {
  font-family: 'Source Code Pro', monospace;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.55);
  margin-bottom: 0.3rem;
}
.ask-item-val { font-size: 0.9rem; font-weight: 500; color: #fff; }

.footnote-strip {
  font-size: 0.72rem;
  color: var(--gray);
  line-height: 1.75;
  padding: 1.25rem 0 0.5rem;
  border-top: 1px solid var(--border);
  margin-top: 1.5rem;
}

/* ---- MODE TOGGLE ---- */
.mode-summary .pitch-nav { display: none; }
.mode-summary #full-view { display: none; }
.mode-summary .pitch-main { margin-left: 0; max-width: 760px; margin-left: auto; margin-right: auto; }

.mode-full #tldr { display: none; }

/* ---- TL;DR VIEW ---- */
.tldr-view {
  padding: 3.5rem 3rem 3rem;
  max-width: 760px;
  margin: 0 auto;
}
.tldr-headline {
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  font-weight: 300;
  line-height: 1.25;
  letter-spacing: -0.01em;
  margin-bottom: 1.75rem;
  color: var(--black);
}
.tldr-headline strong { font-weight: 600; color: var(--blue); }
.tldr-body {
  font-size: 0.95rem;
  color: var(--gray);
  line-height: 1.8;
  margin-bottom: 1.1rem;
  max-width: 68ch;
}
.tldr-body strong { color: var(--black); font-weight: 600; }
.tldr-ask {
  font-size: 1rem;
  font-weight: 600;
  color: var(--black);
  margin: 1.5rem 0 1.75rem;
  font-style: italic;
}
.tldr-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}

/* ---- SCALING LADDER ---- */
.ladder-wrap {
  margin: 2rem 0 2.25rem;
}
.ladder-label {
  font-family: 'Source Code Pro', monospace;
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--gray-lt);
  margin-bottom: 1rem;
}
.ladder {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
}
.ladder-rung {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.ladder-bar {
  width: 100%;
  border-radius: 5px 5px 0 0;
  margin-bottom: 0.6rem;
}
.ladder-rung:nth-child(1) .ladder-bar { height: 48px; background: var(--blue); opacity: 0.5; }
.ladder-rung:nth-child(2) .ladder-bar { height: 96px; background: var(--blue); opacity: 0.75; }
.ladder-rung:nth-child(3) .ladder-bar { height: 160px; background: var(--orange); }
.ladder-num {
  font-family: 'Source Code Pro', monospace;
  font-size: 1.4rem;
  font-weight: 600;
  line-height: 1;
  margin-bottom: 0.25rem;
}
.ladder-rung:nth-child(1) .ladder-num,
.ladder-rung:nth-child(2) .ladder-num { color: var(--blue); }
.ladder-rung:nth-child(3) .ladder-num { color: var(--orange-dk); }
.ladder-desc {
  font-size: 0.75rem;
  color: var(--gray);
  line-height: 1.4;
}
.ladder-caption {
  font-family: 'Source Code Pro', monospace;
  font-size: 10px;
  color: var(--gray-lt);
  margin-top: 0.85rem;
  font-style: italic;
}

/* ---- EXPAND / COLLAPSE BUTTONS ---- */
.expand-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--blue);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.85rem 1.5rem;
  font-family: 'Open Sans', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
  text-decoration: none;
}
.expand-btn:hover { background: var(--blue-dk); }

.collapse-bar {
  padding: 1rem 3rem 0;
}
.collapse-link {
  font-family: 'Source Code Pro', monospace;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--gray-lt);
  text-decoration: none;
}
.collapse-link:hover { color: var(--blue); }

/* ---- RESPONSIVE ---- */
@media (max-width: 900px) {
  .pitch-nav { width: 180px; }
  .pitch-main { margin-left: 180px; }
}
@media (max-width: 700px) {
  .pitch-nav { display: none; }
  .pitch-main { margin-left: 0; }
  .pitch-section { padding: 2.5rem 1.25rem 2rem; }
  .stat-strip { grid-template-columns: 1fr; }
  .pillars-grid { grid-template-columns: 1fr; }
  .credential-pair { grid-template-columns: 1fr; }
  .ask-items { grid-template-columns: 1fr; }
  .tldr-view { padding: 2.5rem 1.25rem 2rem; }
}
"""

# ---------------------------------------------------------------------------
# HTML content builders
# ---------------------------------------------------------------------------

def _section_tldr():
    return ui.div(
        {"class": "tldr-view", "id": "tldr"},
        ui.h1(
            {"class": "tldr-headline"},
            ui.HTML(
                "You will own an internal AI function eventually. "
                "<strong>The only question is when.</strong>"
            ),
        ),
        ui.p(
            {"class": "tldr-body"},
            ui.HTML(
                "AI tooling across your operational teams is already being built. The risk isn't that it fails - "
                "it's that it works at first, then quietly drifts. Every agent has to stay in sync with a world "
                "that keeps moving: processes change, products update, new information lands, the tools it relies "
                "on shift. Skip those updates and the agent keeps answering on six-month-old information until "
                "someone acts on a wrong answer - a customer misled, or one of your own teams making a call on "
                "facts that changed months ago. Nothing alerts you when it happens."
            ),
        ),
        ui.p(
            {"class": "tldr-body"},
            ui.HTML(
                "You're scaling the company, and the AI tooling scales with it. Scaling it is also what turns "
                "a manageable task into a liability no one is holding. For a company your size - around 200 people, "
                "with operational teams across PS, Sales, CS, and Support - a realistic internal portfolio runs "
                "15-20 agents. At 2-3 updates each, that's 30-60 maintenance events a month. Today that work "
                "is no one's actual job."
            ),
        ),
        ui.div(
            {"class": "ladder-wrap"},
            ui.div({"class": "ladder-label"}, "As the company scales \u2192"),
            ui.div(
                {"class": "ladder"},
                ui.div(
                    {"class": "ladder-rung"},
                    ui.div({"class": "ladder-bar"}),
                    ui.div({"class": "ladder-num"}, "2-3"),
                    ui.div({"class": "ladder-desc"}, "updates / month - one agent (what I run today)"),
                ),
                ui.div(
                    {"class": "ladder-rung"},
                    ui.div({"class": "ladder-bar"}),
                    ui.div({"class": "ladder-num"}, "10-15"),
                    ui.div({"class": "ladder-desc"}, "updates / month - one business unit's set of agents"),
                ),
                ui.div(
                    {"class": "ladder-rung"},
                    ui.div({"class": "ladder-bar"}),
                    ui.div({"class": "ladder-num"}, "30-60"),
                    ui.div({"class": "ladder-desc"}, "updates / month - company-wide, ~200 people"),
                ),
            ),
            ui.div({"class": "ladder-caption"}, "The burden grows with every team you add. Today, none of it is owned."),
        ),
        ui.p(
            {"class": "tldr-body"},
            ui.HTML(
                "This is a question of ownership, not skill. Building and maintaining these tools isn't the "
                "product team's job - they're rightly focused on the roadmap - and it isn't the operational "
                "teams' job either, with their hands full of the customers, deals, and implementations they own. "
                "It belongs to neither. What's missing is a dedicated function whose job is exactly this: "
                "requirements in, working systems out."
            ),
        ),
        ui.p(
            {"class": "tldr-body"},
            ui.HTML(
                "I've spent a decade making software land, and I build AI agents that ship and stay in "
                "production. I already run a smaller version of this exact function for my own team - "
                "maintenance included."
            ),
        ),
        ui.hr({"class": "tldr-divider"}),
        ui.p(
            {"class": "tldr-ask"},
            "The ask is one conversation to find out whether this is true for you.",
        ),
        ui.a(
            {"class": "expand-btn", "id": "expand-btn", "href": "#"},
            "Ok, you have my attention \u2192",
        ),
    )


def _nav():
    return ui.div(
        {"class": "pitch-nav"},
        ui.div(
            {"class": "nav-brand"},
            ui.div(
                {"class": "nav-logo"},
                ui.div({"class": "nav-logo-mark"}, "P"),
                ui.div({"class": "nav-brand-name"}, "Posit, PBC"),
            ),
            ui.div({"class": "nav-doc-label"}, "AI Solutions\nRole Proposal"),
        ),
        ui.div(
            {"class": "nav-pills"},
            ui.div({"class": "nav-section-label"}, "The Case"),
            ui.a({"class": "nav-pill active", "href": "#opening"}, "The Risk"),
            ui.a({"class": "nav-pill", "href": "#why-now"}, "Why Now"),
            ui.a({"class": "nav-pill", "href": "#discovery"}, "The Questions"),
            ui.div({"class": "nav-section-label"}, "The Answer"),
            ui.a({"class": "nav-pill", "href": "#function"}, "The Function"),
            ui.a({"class": "nav-pill", "href": "#backlog"}, "Build Backlog"),
            ui.div({"class": "nav-section-label"}, "The Fit"),
            ui.a({"class": "nav-pill", "href": "#why-me"}, "Why Me"),
            ui.div({"class": "nav-section-label"}, "The Numbers"),
            ui.a({"class": "nav-pill", "href": "#calc-capacity"}, "Capacity Cost"),
            ui.div({"class": "nav-section-label"}, "Close"),
            ui.a({"class": "nav-pill", "href": "#ask"}, "The Ask"),
        ),
    )


def _section_opening():
    return ui.div(
        {"class": "pitch-section", "id": "opening"},
        ui.div({"class": "section-eyebrow"}, "The Risk"),
        ui.div(
            {"class": "opening-hero"},
            ui.div({"class": "opening-hero-eyebrow"}, "The maintenance problem"),
            ui.div(
                {"class": "opening-statement"},
                ui.HTML(
                    "Most leaders think the risk of AI tooling is building something that <strong>doesn't work.</strong><br><br>"
                    "The real risk is building something that <strong>works</strong> - and then nobody maintains it."
                ),
            ),
            ui.div(
                {"class": "opening-kicker"},
                ui.HTML(
                    "An unmaintained agent doesn't fail loudly. It keeps running. "
                    "It keeps answering. It keeps producing outputs based on how things worked six months ago. "
                    "By the time anyone notices, the damage is done."
                ),
            ),
        ),
        ui.div(
            {"class": "stat-strip"},
            ui.div(
                {"class": "stat-cell"},
                ui.div({"class": "stat-num"}, "2-3x"),
                ui.div({"class": "stat-label"}, "updates per month to maintain one internal process agent"),
            ),
            ui.div(
                {"class": "stat-cell"},
                ui.div({"class": "stat-num orange"}, "20-30x"),
                ui.div({"class": "stat-label"}, "updates per month across a portfolio of 10 agents"),
            ),
            ui.div(
                {"class": "stat-cell"},
                ui.div({"class": "stat-num"}, "0"),
                ui.div({"class": "stat-label"}, "people currently assigned to own that work at most companies"),
            ),
        ),
        ui.div(
            {"class": "callout"},
            ui.p(
                ui.HTML(
                    "The plan for maintaining these tools a year from now matters more than the plan to build them. "
                    "If the answer is 'whoever built it' or 'we will figure it out,' "
                    "that is not a plan. It is a liability that compounds quietly until it becomes a crisis."
                )
            ),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "Process changes. Tools get updated. Models release new versions that silently degrade "
                "output in ways no alert catches. Every one of those events is a maintenance event - "
                "a prompt that needs updating, a data connection that needs checking, an output that "
                "needs validation. "
                "<strong>Someone has to own that.</strong> Right now, nobody does."
            ),
        ),
        ui.div(
            {"class": "callout blue"},
            ui.p(
                ui.HTML(
                    "The builds are coming. AI tooling across operational teams is not a question of if - "
                    "the only question is whether maintenance is planned from the start or discovered "
                    "after the first tool fails silently."
                )
            ),
        ),
    )


def _section_why_now():
    return ui.div(
        {"class": "pitch-section", "id": "why-now"},
        ui.div({"class": "section-eyebrow"}, "Why Now"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("The window is <strong>open now.</strong> It will not stay that way."),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "AI is no longer a question of whether - it is a question of how. "
                "That shift from curiosity to commitment is happening across every team right now. "
                "The organizations that win are not the ones that move first. "
                "They are the ones that move with structure while everyone else is still moving fast."
            ),
        ),
        ui.div(
            {"class": "stat-strip"},
            ui.div(
                {"class": "stat-cell"},
                ui.div({"class": "stat-num"}, "12-18"),
                ui.div({"class": "stat-label"}, "months to build real operational AI muscle - not tools, but systems"),
            ),
            ui.div(
                {"class": "stat-cell"},
                ui.div({"class": "stat-num orange"}, "2027"),
                ui.div({"class": "stat-label"}, "is not one year behind - it is competing against a team with a year of production data"),
            ),
            ui.div(
                {"class": "stat-cell"},
                ui.div({"class": "stat-num"}, "2x"),
                ui.div({"class": "stat-label"}, "potential return on every internal build that runs on Posit's own stack"),
            ),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "Anyone can use AI. The organizations that pull ahead are the ones that build the "
                "<em>operational muscle</em> - the framework, the <strong>systems</strong>, the evaluation data - "
                "to deploy it with discipline. That muscle is not built in a sprint, and it cannot be built "
                "by people working on it around their day jobs. It takes deliberate investment: "
                "dedicated ownership, production experience, real failures absorbed and learned from. "
                "A company that starts in 2027 is not one year behind. It is competing against "
                "an organization that already made the expensive mistakes and hardened its approach."
            ),
        ),
        ui.div(
            {"class": "callout green"},
            ui.p(
                ui.HTML(
                    "<strong>The Posit multiplier:</strong> Posit's customers are data science teams. "
                    "When internal AI tools are built on Posit's own packages and platforms, "
                    "there is potential for those builds to travel beyond the internal team. "
                    "Reference implementations, dogfooding feedback loops, devrel content. "
                    "The work could pay for itself two or three times over. "
                    "That compounding return is a possibility unique to Posit - but only if the builds "
                    "are done deliberately, on the right stack, with someone accountable for making that happen."
                )
            ),
        ),
    )


def _section_function():
    return ui.div(
        {"class": "pitch-section", "id": "function"},
        ui.div({"class": "section-eyebrow"}, "The Function"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("Requirements in. <strong>Working systems out.</strong>"),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "What Posit's operational teams need is a dedicated internal capability that takes "
                "'we wish we had an AI tool that does X' and turns it into something that actually works - "
                "without PS, Sales, CS, or Support stopping what they are already doing to build it. "
                "<strong>The gap is not competence. It is bandwidth.</strong> "
                "Posit's senior engineers are excellent at AI. Their expertise is committed to the "
                "product roadmap - as it should be. A dedicated internal AI function protects that focus "
                "by owning the operational builds that will never make the product queue."
            ),
        ),
        ui.div(
            {"class": "pillars-grid"},
            ui.div(
                {"class": "pillar-card"},
                ui.div({"class": "pillar-num"}, "Pillar 01"),
                ui.div({"class": "pillar-title"}, "Triage and Advisory"),
                ui.div(
                    {"class": "pillar-body"},
                    "Help any team assess whether AI fits a given problem and what the ROI would be. "
                    "The prioritization question needs an owner whose actual job is to ask it. "
                    "'Should we build this at all' is not an engineer's job to ask, and should not be.",
                ),
            ),
            ui.div(
                {"class": "pillar-card"},
                ui.div({"class": "pillar-num"}, "Pillar 02"),
                ui.div({"class": "pillar-title"}, "Build and Maintain"),
                ui.div(
                    {"class": "pillar-body"},
                    "Posit does not send customers a few emails and hope they are successful. "
                    "Internal tools deserve the same standard. That means proper implementation: "
                    "requirements gathered, systems built to spec, deployed correctly, and maintained "
                    "as the processes around them change. On Posit's stack wherever the use case fits.",
                ),
            ),
            ui.div(
                {"class": "pillar-card"},
                ui.div({"class": "pillar-num"}, "Pillar 03"),
                ui.div({"class": "pillar-title"}, "Governance"),
                ui.div(
                    {"class": "pillar-body"},
                    "Shared standards for how AI is used internally: which models for which tasks, "
                    "how data is handled, how outputs are validated, and how the portfolio is evaluated "
                    "as models evolve. The same rigor Posit applies to reproducibility in its products, "
                    "applied to the AI systems running inside its own walls.",
                ),
            ),
        ),
        ui.div(
            {"class": "callout blue"},
            ui.p(
                ui.HTML(
                    "<strong>Operating model - small and scaling:</strong> Two people to start. "
                    "A founding director and one strong builder. Land-and-expand: low burn, fast proof, "
                    "grow against a proven pipeline rather than a slide. Player-coach from day one - "
                    "hands-on in the build, not pure management. "
                    "Where it makes sense to build on Posit's own stack, we will - that is where the "
                    "additional leverage lives. But the right tool for the job comes first."
                )
            ),
        ),
    )


def _section_backlog():
    teams = [
        {
            "name": "Professional Services",
            "badge": "validated",
            "items": [
                {
                    "name": "PM Agent",
                    "desc": "Automates status updates, flags at-risk milestones, surfaces blockers for PM review. Keeps the PM's head up and reduces reporting overhead.",
                    "tags": [],
                },
                {
                    "name": "Customer Self-Service Agent",
                    "desc": "Answers common how-to questions during implementation using project documentation and Posit product docs. Reduces interruptions to the PS team.",
                    "tags": [("QUICK WIN", "tag-quick")],
                },
                {
                    "name": "PS-to-CS Handoff Agent",
                    "desc": "Drafts the structured handoff document from implementation data at project close. Owned by PS, consumed by CS.",
                    "tags": [("SHARED", "tag-shared")],
                },
                {
                    "name": "SOW Agent",
                    "desc": "Drafts statement of work sections from scoping call notes and historical SOW patterns. One build, scoped narrowly.",
                    "tags": [],
                },
            ],
        },
        {
            "name": "Customer Success",
            "badge": "validated",
            "items": [
                {
                    "name": "PS-to-CS Handoff Agent",
                    "desc": "The CS side of the shared handoff build. CS owns consumption and follow-up workflow; PS owns creation.",
                    "tags": [("SHARED", "tag-shared")],
                },
                {
                    "name": "QBR Prep Agent",
                    "desc": "Pulls usage data, support history, and account notes into a structured QBR brief. Quick win: low complexity, high visibility, strong first proof point for the function.",
                    "tags": [("QUICK WIN", "tag-quick")],
                },
                {
                    "name": "Onboarding Gap Detector",
                    "desc": "Flags customers who are behind on adoption benchmarks at defined intervals. Surfaces them for CSM review before they become churn risk.",
                    "tags": [],
                },
                {
                    "name": "Renewal Risk Signal Agent",
                    "desc": "Aggregates engagement, support, and usage signals to score renewal risk. High-value, high-complexity. Starts read-only; earns action through Crawl/Walk/Run phases.",
                    "tags": [("CRAWL-WALK-RUN", "tag-caution")],
                },
            ],
        },
        {
            "name": "Sales",
            "badge": "hypothesis",
            "items": [
                {
                    "name": "Pre-Call Research Agent",
                    "desc": "Assembles account context, recent news, and product usage history into a pre-call brief. Reduces prep time; increases rep confidence.",
                    "tags": [],
                },
                {
                    "name": "RFP / Technical Questionnaire Agent",
                    "desc": "Drafts responses to security, compliance, and technical RFP questions from a maintained knowledge base. High-volume, repetitive work with clear ROI.",
                    "tags": [],
                },
                {
                    "name": "Competitive Intel Agent",
                    "desc": "Monitors competitive signals and surfaces relevant positioning notes for reps. Sensitive territory - starts read-only, earns its way carefully.",
                    "tags": [("CRAWL-WALK-RUN", "tag-caution")],
                },
            ],
        },
        {
            "name": "Support",
            "badge": "hypothesis",
            "items": [
                {
                    "name": "Ticket Pattern Analyzer",
                    "desc": "Surfaces recurring issue clusters across the ticket queue. Identifies documentation gaps and systemic bugs that no single ticket reveals.",
                    "tags": [],
                },
                {
                    "name": "Known-Issue Triage Agent",
                    "desc": "Matches incoming tickets against a maintained known-issue database. Routes to the right resource faster; reduces duplicate investigation.",
                    "tags": [],
                },
                {
                    "name": "Documentation Gap Detector",
                    "desc": "Identifies questions the docs do not answer well by analyzing ticket patterns and failed self-service attempts.",
                    "tags": [],
                },
                {
                    "name": "Escalation Signal Agent",
                    "desc": "Flags tickets with escalation indicators before they escalate - sentiment, account tier, recurrence, wait time. Gives support leads time to intervene.",
                    "tags": [("CRAWL-WALK-RUN", "tag-caution")],
                },
            ],
        },
    ]

    team_els = []
    for team in teams:
        badge_cls = "backlog-badge" if team["badge"] == "validated" else "backlog-badge hyp"
        badge_text = "VALIDATED" if team["badge"] == "validated" else "HYPOTHESIS"

        item_els = []
        for idx, item in enumerate(team["items"]):
            tag_els = [ui.span({"class": f"tag {tc}"}, tl) for tl, tc in item["tags"]]
            item_els.append(
                ui.div(
                    {"class": "backlog-item"},
                    ui.div({"class": "backlog-item-icon"}, f"{idx+1:02d}"),
                    ui.div(
                        {"class": "backlog-item-body"},
                        ui.div({"class": "backlog-item-name"}, item["name"]),
                        ui.div({"class": "backlog-item-desc"}, item["desc"]),
                        ui.div({"class": "backlog-item-tags"}, *tag_els) if tag_els else ui.span(),
                    ),
                )
            )

        team_els.append(
            ui.div(
                {"class": "backlog-team"},
                ui.div(
                    {"class": "backlog-team-header"},
                    ui.div({"class": "backlog-team-name"}, team["name"]),
                    ui.div(
                        {"class": "backlog-team-meta"},
                        ui.div({"class": badge_cls}, badge_text),
                        ui.div({"class": "expand-icon"}, "-"),
                    ),
                ),
                ui.div({"class": "backlog-team-body"}, *item_els),
            )
        )

    return ui.div(
        {"class": "pitch-section", "id": "backlog"},
        ui.div({"class": "section-eyebrow"}, "Possibilities"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("A pipeline, <strong>not a wishlist.</strong>"),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "These are starting points, not a definitive list. The value AI could unlock across "
                "PS, Sales, CS, and Support is real and significant - the tools below give a sense "
                "of what becomes possible. But as you read them, hold both thoughts at once: "
                "<strong>how much could these accelerate the work,</strong> and "
                "<strong>who is going to build and maintain them?</strong> "
                "That second question is the one this role exists to answer."
            ),
        ),
        *team_els,
        ui.div(
            {"class": "callout blue"},
            ui.p(
                ui.HTML(
                    "<strong>Every build starts read-only. We never arrive at a state where AI decides and acts without a human in the loop.</strong> "
                    "Phase 1 (Crawl): agent reads and reports, human decides and acts. "
                    "Phase 2 (Walk): agent flags and scores, human owns all actions. "
                    "Phase 3 (Run): agent drafts and routes within a narrow scope, human approves before anything executes. "
                    "The gate between phases is performance, not a calendar. "
                    "For the highest-risk builds - Renewal Risk Signal, Competitive Intel, Escalation Signal - "
                    "the phases are mapped explicitly before any work starts."
                )
            ),
        ),
        ui.div(
            {"class": "footnote-strip"},
            ui.HTML(
                "<b>Tag key:</b> "
                "<span style='color:#4a6b28;font-weight:600;'>QUICK WIN</span> - ships first as proof; "
                "<span style='color:#447099;font-weight:600;'>SHARED</span> - cross-team build with two owners; "
                "<span style='color:#c94e1f;font-weight:600;'>CRAWL-WALK-RUN</span> - higher-complexity build, phased approach required."
            ),
        ),
    )


def _section_why_me():
    return ui.div(
        {"class": "pitch-section", "id": "why-me"},
        ui.div({"class": "section-eyebrow"}, "Why Me"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("Two credentials. <strong>Both load-bearing.</strong>"),
        ),
        ui.p(
            {"class": "body-copy"},
            "This case rests on two separate things.",
        ),
        ui.div(
            {"class": "credential-pair"},
            ui.div(
                {"class": "credential-card"},
                ui.div({"class": "credential-num"}, "Credential 01 - The Delivery Track Record"),
                ui.div({"class": "credential-title"}, "A decade of making software land"),
                ui.div(
                    {"class": "credential-body"},
                    ui.HTML(
                        "Implementation leadership, enterprise delivery, cross-functional alignment, PMP. "
                        "I know the project management motions. I know how to work with stakeholders to get "
                        "the actual solution they need - not just what they first ask for. I know how to "
                        "stay on target and on time, and how to enable the teams that will use what gets built.<br><br>"
                        "<strong>This is 80% of this job.</strong> Building the agents is the other 20%. "
                        "An engineer can write the code. The delivery skill is what makes the function work."
                    ),
                ),
            ),
            ui.div(
                {"class": "credential-card"},
                ui.div({"class": "credential-num"}, "Credential 02 - The Hands-On AI Record"),
                ui.div({"class": "credential-title"}, "Working agents in production, not slides"),
                ui.div(
                    {"class": "credential-body"},
                    ui.HTML(
                        "A suite of working agents built for a PS team: PM Agent, PS-to-Support Handoff, "
                        "PS-to-CS Handoff, How-To Agent. A Shiny for R prototype of a SaaS implementation "
                        "assistant, deployed on Posit Cloud, built with the Anthropic API via httr2.<br><br>"
                        "A few years of hands-on building with a structured, scalable framework."
                    ),
                ),
            ),
        ),
        ui.div(
            {"class": "callout blue"},
            ui.p(
                ui.HTML(
                    "<strong>The rare combination:</strong> Technical depth plus business judgment. "
                    "The reason not to staff this from the engineering bench is not that engineers lack "
                    "judgment - it is that they are correctly pointed at the product roadmap and measured "
                    "on it. 'Should we build this internal tool at all' is not their job to ask. "
                    "An internal hire also comes from the exact bench this role exists to protect, "
                    "and would drift back to product work. An outside hire who has already built "
                    "on Posit's own stack does not have that drift problem."
                )
            ),
        ),
        ui.div(
            {"class": "callout green"},
            ui.p(
                ui.HTML(
                    "<strong>Maintenance ownership as proof:</strong> I already run the function I am proposing. "
                    "My internal process agent documents our team's processes and answers questions. "
                    "Every time a process changes, I update it - 2-3 times a month, every month. "
                    "That is not a hypothetical maintenance burden. That is the lifecycle work "
                    "Posit's operational teams currently have no plan for, running live."
                )
            ),
        ),
    )


def _section_discovery():
    questions = [
        {
            "q": "Who is responsible for building AI agents and systems for internal operational teams?",
            "reveal": "Without a clear owner, builds happen whenever someone has a spare hour - which means they happen inconsistently, to varying standards, with no shared framework. The institutional knowledge lives with whoever did the work, and leaves when they do.",
        },
        {
            "q": "How much time away from their actual job do they have to build these tools properly?",
            "reveal": "Bandwidth is the real constraint, not capability. When the people doing the building are also responsible for their primary job, AI tooling gets the hours nobody else claimed. That is not a recipe for production-quality systems.",
        },
        {
            "q": "Are the people building these tools following a shared company standard?",
            "reveal": "Without shared standards, every build is a one-off. That makes each tool harder to maintain, harder to hand off, and impossible to govern at scale. What works for one team does not transfer to the next.",
        },
        {
            "q": "Before anything gets built, who decides whether the tool is even needed?",
            "reveal": "Without an owner for the prioritization question, the answer defaults to whoever asked loudest or most recently. Tools get built that duplicate effort, solve the wrong problem, or create maintenance burden without corresponding value.",
        },
        {
            "q": "Who makes sure these tools are optimized - not just reaching for the most expensive model when a cheaper one would do?",
            "reveal": "Model selection, prompt design, context trimming, and output right-sizing can dramatically affect cost. Without someone accountable for those decisions, teams default to the most capable model they know - which is rarely the most appropriate one.",
        },
        {
            "q": "When a new model is released, who checks that it does not break the tools already in production?",
            "reveal": "Model updates are not automatically safe. An agent that performs well today can degrade quietly on a new version - different output formatting, changed reasoning patterns, subtle shifts in how instructions are interpreted. Nobody catches this unless someone is looking.",
        },
        {
            "q": "When an agent needs to be rebuilt, what happens when the person who built it has left or is buried in another project?",
            "reveal": "This is where most ad hoc AI programs eventually stall. The tool exists, the person who understood it is gone, and nobody else has the context to maintain it. The options are an expensive rebuild or quietly abandoning something the team came to depend on.",
        },
        {
            "q": "Who is evaluating new tools, platforms, and systems - keeping an eye on what is coming?",
            "reveal": "The AI tooling landscape changes fast enough that last year's best approach may already have a better alternative. Staying current is a dedicated task - it does not happen as a byproduct of other work.",
        },
        {
            "q": "Who is helping teams self-serve on AI - not building everything for them, but enabling them to move?",
            "reveal": "A build-only function creates dependency. Teams wait for the queue instead of moving. Enablement - teaching teams to use AI well within guardrails - is what makes the investment compound over time.",
        },
    ]

    q_els = []
    for idx, item in enumerate(questions):
        q_els.append(
            ui.div(
                {"class": "disc-question"},
                ui.div(
                    {"class": "disc-q-header"},
                    ui.div({"class": "disc-q-num"}, f"Q{idx+1:02d}"),
                    ui.div({"class": "disc-q-text"}, item["q"]),
                    ui.div({"class": "disc-q-chevron"}, "v"),
                ),
                ui.div(
                    {"class": "disc-reveal"},
                    ui.HTML(item["reveal"]),
                ),
            )
        )

    return ui.div(
        {"class": "pitch-section", "id": "discovery"},
        ui.div({"class": "section-eyebrow"}, "The Questions"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("Worth answering <strong>before the first build ships.</strong>"),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "Any organization scaling AI tooling should be able to answer these cleanly. "
                "They are not trick questions - they are the operational basics. "
                "Click any question to see what happens when the answer is unclear."
            ),
        ),
        *q_els,
    )


def _calc_capacity_embed():
    return ui.div(
        {"class": "pitch-section", "id": "calc-capacity"},
        ui.div({"class": "section-eyebrow"}, "The Numbers"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("The <strong>hidden capacity cost</strong> of building AI tooling ad hoc."),
        ),
        ui.p(
            {"class": "body-copy"},
            "Adjust the inputs to match your team. Defaults are conservative and sourced. Your actual numbers are likely larger, not smaller.",
        ),
        ui.HTML(
            '<iframe src="ai-value-calculator.html" '
            'style="width:100%;border:none;height:2600px;display:block;" '
            'scrolling="no"></iframe>'
        ),
    )


def _calc_roi_embed():
    return ui.div(
        {"class": "pitch-section", "id": "calc-roi"},
        ui.div({"class": "section-eyebrow"}, "Calculator 02"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("The <strong>compounding savings</strong> from AI governance across three phases."),
        ),
        ui.p(
            {"class": "body-copy"},
            "Each phase unlocks new optimization levers. The numbers below show what becomes possible, and when.",
        ),
        ui.HTML(
            '<iframe src="AI_Governance_ROI.html" '
            'style="width:100%;border:none;height:800px;display:block;" '
            'scrolling="no"></iframe>'
        ),
    )


def _section_ask():
    return ui.div(
        {"class": "pitch-section", "id": "ask"},
        ui.div({"class": "section-eyebrow"}, "The Ask"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("A conversation. <strong>Not a job application.</strong>"),
        ),
        ui.div(
            {"class": "ask-band"},
            ui.p(
                ui.HTML(
                    "This role does not exist yet. That is the point. "
                    "The function described here is the answer to a set of questions any organization "
                    "scaling AI tooling will eventually have to answer. "
                    "The ask is a conversation to test whether those questions resonate, "
                    "and whether this is the right moment to get ahead of them."
                )
            ),
            ui.div(
                {"class": "callout green"},
                ui.p(
                    ui.HTML(
                        "<strong>The compounding argument:</strong> A team that starts building "
                        "this function in 2026 does not have a one-year head start over a team "
                        "that starts in 2027. It has a year of production systems, real evaluation data, "
                        "and a team that has already made the expensive mistakes. That gap widens every month. "
                        "The cost of waiting is not just internal inefficiency - "
                        "it is also ceding the credibility story to someone else."
                    )
                ),
            ),
            ui.p(
                {"style": "font-size:0.82rem;color:rgba(255,255,255,0.7);margin-bottom:0.5rem;margin-top:1rem;"},
                "One scenario for how this could look:",
            ),
            ui.div(
                {"class": "ask-items"},
                ui.div(
                    {"class": "ask-item"},
                    ui.div({"class": "ask-item-label"}, "Title anchor"),
                    ui.div({"class": "ask-item-val"}, "Founding Head of AI Solutions"),
                ),
                ui.div(
                    {"class": "ask-item"},
                    ui.div({"class": "ask-item-label"}, "Level floor"),
                    ui.div({"class": "ask-item-val"}, "Director (or Sr. Manager, comp-dependent)"),
                ),
                ui.div(
                    {"class": "ask-item"},
                    ui.div({"class": "ask-item-label"}, "Reporting line"),
                    ui.div({"class": "ask-item-val"}, "COO or cross-functional ops owner"),
                ),
                ui.div(
                    {"class": "ask-item"},
                    ui.div({"class": "ask-item-label"}, "Starting team"),
                    ui.div({"class": "ask-item-val"}, "Two - founding director + builder"),
                ),
                ui.div(
                    {"class": "ask-item"},
                    ui.div({"class": "ask-item-label"}, "First proof points"),
                    ui.div({"class": "ask-item-val"}, "QBR Prep Agent + SOW Agent"),
                ),
                ui.div(
                    {"class": "ask-item"},
                    ui.div({"class": "ask-item-label"}, "Visibility anchor"),
                    ui.div({"class": "ask-item-val"}, "posit::conf 2026 - Houston, Sept 14-16"),
                ),
            ),
            ui.p(
                ui.HTML(
                    "Several of these are starting points, not conclusions - "
                    "the reporting line in particular depends on org structure that a conversation would clarify. "
                    "The next step is that conversation."
                )
            ),
        ),
        ui.div(
            {"class": "footnote-strip"},
            ui.HTML(
                "Some items here are hypotheses awaiting validation - the Sales and Support build ideas, "
                "the right reporting line, whether any informal version of this function already exists. "
                "That is what the conversation is for."
            ),
        ),
    )


# ---------------------------------------------------------------------------
# App UI
# ---------------------------------------------------------------------------

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.style(_CSS),
        ui.tags.link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.47.0/tabler-icons.min.css",
        ),
    ),
    ui.div(
        {"class": "pitch-shell mode-summary"},
        _nav(),
        ui.div(
            {"class": "pitch-main"},
            _section_tldr(),
            ui.div(
                {"class": "full-view", "id": "full-view"},
                ui.div(
                    {"class": "collapse-bar"},
                    ui.a(
                        {"class": "collapse-link", "id": "collapse-btn", "href": "#"},
                        "\u2191 Back to summary",
                    ),
                ),
                _section_opening(),
                _section_why_now(),
                _section_discovery(),
                _section_function(),
                _section_backlog(),
                _section_why_me(),
                _calc_capacity_embed(),
                _section_ask(),
            ),
        ),
    ),
    ui.tags.script(ui.HTML(_build_js())),
)


def server(input, output, session):
    pass


app = App(app_ui, server, static_assets=Path(__file__).parent / "www")
