import os
from shiny import App, ui

# ---------------------------------------------------------------------------
# Static JS - all JavaScript in one place, injected at render time
# ---------------------------------------------------------------------------
_STATIC_JS = """
(function() {
  // ---- NAV SCROLL --------------------------------------------------------
  var navLinks = document.querySelectorAll('.nav-pill');
  navLinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
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

/* ---- CRAWL/WALK/RUN ---- */
.cwr-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin: 1.5rem 0;
}
.cwr-card {
  border-radius: 10px;
  padding: 1.35rem 1.25rem;
}
.cwr-card.crawl { background: #FAEEDA; border: 1px solid #BA7517; }
.cwr-card.walk  { background: #E6F1FB; border: 1px solid #378ADD; }
.cwr-card.run   { background: #EAF3DE; border: 1px solid #639922; }
.cwr-label {
  font-family: 'Source Code Pro', monospace;
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-bottom: 0.35rem;
}
.cwr-card.crawl .cwr-label { color: #854F0B; }
.cwr-card.walk  .cwr-label { color: #185FA5; }
.cwr-card.run   .cwr-label { color: #3B6D11; }
.cwr-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.cwr-card.crawl .cwr-title { color: #633806; }
.cwr-card.walk  .cwr-title { color: #0C447C; }
.cwr-card.run   .cwr-title { color: #27500A; }
.cwr-body { font-size: 0.8rem; line-height: 1.6; }
.cwr-card.crawl .cwr-body { color: #854F0B; }
.cwr-card.walk  .cwr-body { color: #185FA5; }
.cwr-card.run   .cwr-body { color: #3B6D11; }
.cwr-human {
  margin-top: 0.75rem;
  padding-top: 0.6rem;
  border-top: 1px solid rgba(0,0,0,0.1);
  font-family: 'Source Code Pro', monospace;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.cwr-card.crawl .cwr-human { color: #854F0B; }
.cwr-card.walk  .cwr-human { color: #185FA5; }
.cwr-card.run   .cwr-human { color: #3B6D11; }

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

/* ---- CALCULATOR WRAPPER ---- */
.calc-embed {
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  background: var(--card);
}
.calc-header {
  background: var(--blue-bg);
  border-bottom: 1px solid var(--blue-lt);
  padding: 0.85rem 1.25rem;
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
}
.calc-header-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--blue);
}
.calc-header-sub {
  font-size: 0.75rem;
  color: var(--gray);
}
.calc-body { padding: 1.5rem; }

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
  .cwr-grid { grid-template-columns: 1fr; }
  .credential-pair { grid-template-columns: 1fr; }
  .ask-items { grid-template-columns: 1fr; }
}
"""

# ---------------------------------------------------------------------------
# HTML content builders
# ---------------------------------------------------------------------------

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
            ui.a({"class": "nav-pill", "href": "#function"}, "The Function"),
            ui.div({"class": "nav-section-label"}, "The Work"),
            ui.a({"class": "nav-pill", "href": "#backlog"}, "Build Backlog"),
            ui.a({"class": "nav-pill", "href": "#framework"}, "The Framework"),
            ui.div({"class": "nav-section-label"}, "The Fit"),
            ui.a({"class": "nav-pill", "href": "#why-me"}, "Why Me"),
            ui.a({"class": "nav-pill", "href": "#discovery"}, "Discovery Qs"),
            ui.div({"class": "nav-section-label"}, "The Numbers"),
            ui.a({"class": "nav-pill", "href": "#calc-capacity"}, "Capacity Cost"),
            ui.a({"class": "nav-pill", "href": "#calc-roi"}, "Governance ROI"),
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
            ui.div({"class": "opening-hero-eyebrow"}, "The cold open"),
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
                    "<strong>The question to put in the room:</strong> \"What is your plan for maintaining "
                    "these tools a year from now?\" If the answer is 'whoever built it' or 'we'll figure it out,' "
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
                    "<strong>Close the escape hatch:</strong> A skeptical leader might answer 'or we just don't "
                    "build all those agents.' That option is off the table. The CEO and leadership have made AI "
                    "a now priority - not-building is not the choice. The only real question is whether "
                    "maintenance is designed in from day one, or discovered after the first tool fails silently."
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
            ui.HTML("Attaching to <strong>existing urgency,</strong> not creating it."),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "The CEO and leadership have explicitly communicated that AI is a now priority. "
                "This is explicit direction, not ambient enthusiasm. That makes this an easier pitch: "
                "the question is not whether AI matters. The question is whether doing it with structure "
                "beats doing it ad hoc."
            ),
        ),
        ui.div(
            {"class": "stat-strip"},
            ui.div(
                {"class": "stat-cell"},
                ui.div({"class": "stat-num"}, "12-18"),
                ui.div({"class": "stat-label"}, "months to build real operational AI muscle - not tools, systems"),
            ),
            ui.div(
                {"class": "stat-cell"},
                ui.div({"class": "stat-num orange"}, "2027"),
                ui.div({"class": "stat-label"}, "is not one year behind - it is competing against a team with a year of production data"),
            ),
            ui.div(
                {"class": "stat-cell"},
                ui.div({"class": "stat-num"}, "2x"),
                ui.div({"class": "stat-label"}, "every internal build on Posit's stack is also a reference implementation for customers"),
            ),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "Anyone can use AI. The companies that win are the ones that build the "
                "<em>operational muscle</em> - the framework, the systems, the evaluation data - "
                "to deploy it with discipline. That muscle is not built in a sprint. "
                "It takes 12-18 months of production experience, real failures, and institutional "
                "learning. A company that starts in 2027 is not one year behind. It is competing "
                "against an organization that already made the expensive mistakes and learned from them."
            ),
        ),
        ui.div(
            {"class": "callout green"},
            ui.p(
                ui.HTML(
                    "<strong>The Posit multiplier:</strong> Posit's customers are data science teams. "
                    "When Posit builds internal AI tools on its own stack - ellmer, ragnar, shinychat - "
                    "those builds do not stay internal. They become reference implementations, "
                    "dogfooding feedback loops, and devrel content. The work pays for itself two or "
                    "three times over. That compounding return is unique to Posit. It does not exist "
                    "the same way anywhere else."
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
                "The function takes 'we wish we had an AI tool that does X' from any operational "
                "team - PS, Sales, CS, Support - and ships it, without that team stopping what "
                "they are already doing. <strong>The gap is not competence. It is bandwidth.</strong> "
                "Posit's senior engineers are excellent at AI. Their expertise is committed to the "
                "product roadmap. This function protects that focus by owning the internal builds "
                "that will never make it to the product queue."
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
                    "Ship and maintain agents and shared AI infrastructure on Posit's stack wherever "
                    "the use case allows. Deployment is its own project, not a button press. "
                    "Maintenance is designed in from day one, not discovered after the first failure.",
                ),
            ),
            ui.div(
                {"class": "pillar-card"},
                ui.div({"class": "pillar-num"}, "Pillar 03"),
                ui.div({"class": "pillar-title"}, "Governance"),
                ui.div(
                    {"class": "pillar-body"},
                    "Responsible-use, data-handling, and security standards across every build. "
                    "Zero-data-retention routing, PII sanitization, and model evaluation standards "
                    "that map onto Posit's reproducibility and verification pitch to regulated industries.",
                ),
            ),
        ),
        ui.div(
            {"class": "callout blue"},
            ui.p(
                ui.HTML(
                    "<strong>Operating model - small and scaling:</strong> Two people to start. "
                    "A delivery lead (me) and one ecosystem-fluent builder with real depth in "
                    "ellmer, chatlas, ragnar, and shinychat. Land-and-expand: low burn, fast proof, "
                    "grow against a proven pipeline rather than a slide. Player-coach from day one - "
                    "hands-on in the build, not pure management."
                )
            ),
        ),
        ui.div(
            {"class": "callout"},
            ui.p(
                ui.HTML(
                    "<strong>The partner model:</strong> I do not know Posit's processes better than "
                    "Posit does, and I will not pretend to. What I do: listen, translate what a team "
                    "needs into something that works, and deliver it. The same thing I have done for "
                    "customers for over a decade, now pointed inward. That reframes the function from "
                    "'AI expert who tells you what to build' to 'delivery partner who builds what you "
                    "actually need.' It is harder to replicate than an engineer's instinct to design "
                    "the solution before understanding the problem."
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
                    "tags": [("POSIT STACK", "tag-posit")],
                },
                {
                    "name": "Customer Self-Service Agent",
                    "desc": "Answers common how-to questions during implementation using project documentation and Posit product docs. Reduces interruptions to the PS team.",
                    "tags": [("POSIT STACK", "tag-posit"), ("QUICK WIN", "tag-quick")],
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
                    "tags": [("QUICK WIN", "tag-quick"), ("POSIT STACK", "tag-posit")],
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
                    "tags": [("HYPOTHESIS", "tag-hyp")],
                },
                {
                    "name": "RFP / Technical Questionnaire Agent",
                    "desc": "Drafts responses to security, compliance, and technical RFP questions from a maintained knowledge base. High-volume, repetitive work with clear ROI.",
                    "tags": [("HYPOTHESIS", "tag-hyp")],
                },
                {
                    "name": "Competitive Intel Agent",
                    "desc": "Monitors competitive signals and surfaces relevant positioning notes for reps. Sensitive territory - starts read-only, earns its way carefully.",
                    "tags": [("HYPOTHESIS", "tag-hyp"), ("CRAWL-WALK-RUN", "tag-caution")],
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
                    "tags": [("HYPOTHESIS", "tag-hyp"), ("POSIT STACK", "tag-posit")],
                },
                {
                    "name": "Known-Issue Triage Agent",
                    "desc": "Matches incoming tickets against a maintained known-issue database. Routes to the right resource faster; reduces duplicate investigation.",
                    "tags": [("HYPOTHESIS", "tag-hyp")],
                },
                {
                    "name": "Documentation Gap Detector",
                    "desc": "Identifies questions the docs do not answer well by analyzing ticket patterns and failed self-service attempts.",
                    "tags": [("HYPOTHESIS", "tag-hyp")],
                },
                {
                    "name": "Escalation Signal Agent",
                    "desc": "Flags tickets with escalation indicators before they escalate - sentiment, account tier, recurrence, wait time. Gives support leads time to intervene.",
                    "tags": [("HYPOTHESIS", "tag-hyp"), ("CRAWL-WALK-RUN", "tag-caution")],
                },
            ],
        },
    ]

    team_els = []
    for team in teams:
        badge_cls = "backlog-badge" if team["badge"] == "validated" else "backlog-badge hyp"
        badge_text = "Validated" if team["badge"] == "validated" else "Hypothesis - validate with Aaron"

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
        ui.div({"class": "section-eyebrow"}, "Build Backlog"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("14 candidate builds. <strong>12-18 months</strong> of pipeline before anyone invents new ideas."),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "The backlog is thickest for PS - where I have lived the work - and thinner for "
                "teams I do not know as well. That asymmetry is honest, and it is the operating model. "
                "I am not the process expert. I am the delivery partner who extracts what is needed "
                "and builds it. Sales and Support items are marked as hypotheses until validated "
                "through a proper discovery conversation."
            ),
        ),
        *team_els,
        ui.div(
            {"class": "footnote-strip"},
            ui.HTML(
                "<b>Tag key:</b> "
                "<span style='color:#4a6b28;font-weight:600;'>QUICK WIN</span> - ships first as proof; "
                "<span style='color:#447099;font-weight:600;'>SHARED</span> - cross-team build with two owners; "
                "<span style='color:#8a5200;font-weight:600;'>POSIT STACK</span> - built on ellmer/ragnar/shinychat, doubles as reference implementation; "
                "<span style='color:#c94e1f;font-weight:600;'>CRAWL-WALK-RUN</span> - high-risk build, phases required; "
                "<span style='color:#888;font-weight:600;'>HYPOTHESIS</span> - validate with internal connection before committing."
            ),
        ),
    )


def _section_framework():
    return ui.div(
        {"class": "pitch-section", "id": "framework"},
        ui.div({"class": "section-eyebrow"}, "The Framework"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("Every build starts <strong>read-only.</strong> Autonomy is earned, not assumed."),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "Crawl / Walk / Run is not a phasing patch on the risky builds. It is the default "
                "operating posture for every build. We never arrive at a state where AI decides and "
                "acts without a human in the loop. The gate between phases is performance, not a calendar."
            ),
        ),
        ui.div(
            {"class": "cwr-grid"},
            ui.div(
                {"class": "cwr-card crawl"},
                ui.div({"class": "cwr-label"}, "Crawl - Phase 1"),
                ui.div({"class": "cwr-title"}, "Read-only reporting"),
                ui.div(
                    {"class": "cwr-body"},
                    "Agent reads data and produces a digest or report. "
                    "Human reads the output, decides what to do, and acts. "
                    "No action surface exposed to the agent.",
                ),
                ui.div({"class": "cwr-human"}, "Human owns: everything"),
            ),
            ui.div(
                {"class": "cwr-card walk"},
                ui.div({"class": "cwr-label"}, "Walk - Phase 2"),
                ui.div({"class": "cwr-title"}, "Structured surfacing"),
                ui.div(
                    {"class": "cwr-body"},
                    "Agent flags, scores, or categorizes. Output is structured for human judgment. "
                    "Human still owns every action - the agent surfaces; it does not decide.",
                ),
                ui.div({"class": "cwr-human"}, "Human owns: all actions"),
            ),
            ui.div(
                {"class": "cwr-card run"},
                ui.div({"class": "cwr-label"}, "Run - Phase 3"),
                ui.div({"class": "cwr-title"}, "Narrow workflow initiation"),
                ui.div(
                    {"class": "cwr-body"},
                    "Agent drafts and routes within a narrow, reversible scope. "
                    "Human approves before anything executes. "
                    "Delegation stays explicit and bounded.",
                ),
                ui.div({"class": "cwr-human"}, "Human owns: every approval gate"),
            ),
        ),
        ui.div(
            {"class": "callout"},
            ui.p(
                ui.HTML(
                    "<strong>For the highest-risk builds</strong> - Renewal Risk Signal, Competitive Intel, "
                    "Escalation Signal - the Crawl/Walk/Run phases are itemized explicitly in the build plan "
                    "before any work starts. The framework is not a workaround. It is the plan."
                )
            ),
        ),
    )


def _section_why_me():
    return ui.div(
        {"class": "pitch-section", "id": "why-me"},
        ui.div({"class": "section-eyebrow"}, "Why Me"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("Two credentials. <strong>Do not conflate them.</strong>"),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "The honest version of this case is built on two separate things. "
                "Conflating them makes both weaker. Keeping them distinct makes the case more credible."
            ),
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
                        "<strong>Not a decade of AI.</strong> A few years of hands-on building with a "
                        "structured, scalable framework. The real story is strong enough on its own. "
                        "One exaggeration makes them doubt everything else."
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
            "reveal": "At most companies, the honest answer is 'no one,' or 'whoever happens to have a free hour this week.' Each question that lands without a clean answer is another piece of the case for the function.",
        },
        {
            "q": "How much time away from their actual job do they have to build these tools properly?",
            "reveal": "The gap is not competence - it is bandwidth. Posit's engineers are committed to the product roadmap. Internal operational builds will never make the product queue, which means they fall to whoever is available.",
        },
        {
            "q": "Are the people building these tools following a shared company standard?",
            "reveal": "Without a shared owner, standards fragment. Teams build to their own approach, which makes maintenance harder, governance impossible, and institutional knowledge tied to whoever built the thing.",
        },
        {
            "q": "Before anything gets built, who decides whether the tool is even needed?",
            "reveal": "The prioritization question needs an owner whose actual job is to ask it. Without one, everything that gets requested gets built, and the maintenance burden compounds without a corresponding return.",
        },
        {
            "q": "Who makes sure these tools are optimized - not just reaching for the most expensive model when a cheaper one would do?",
            "reveal": "Model selection, context trimming, caching, and batch routing can cut API costs dramatically. Without governance, teams default to the biggest model for everything. The ROI calculator on this site models the compounding savings from structured optimization.",
        },
        {
            "q": "When a new model is released, who checks that it does not break the tools already in production?",
            "reveal": "Model updates are silent maintenance events. An agent that passes all tests today may degrade quietly on a new model version. Without ownership, nobody checks until something goes wrong.",
        },
        {
            "q": "When an agent needs to be rebuilt, what happens when the person who built it has left or is buried in another project?",
            "reveal": "This is the core liability. Institutional knowledge tied to one person is a single point of failure. The function solves this by owning the portfolio, not individual people owning individual tools.",
        },
        {
            "q": "Who is evaluating new tools, platforms, and systems - keeping an eye on what is coming?",
            "reveal": "Horizon scanning is a dedicated task, not something that happens naturally alongside a full-time job. The function owns this, which protects the rest of the organization from being blindsided by a platform shift.",
        },
        {
            "q": "Who is helping teams self-serve on AI - not building everything for them, but enabling them to move?",
            "reveal": "Enablement is the long-term multiplier. A function that only builds creates a dependency. A function that also enables creates capability. Both are part of the operating model.",
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
        ui.div({"class": "section-eyebrow"}, "Discovery Questions"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("The questions that <strong>surface the gap</strong> without naming it."),
        ),
        ui.p(
            {"class": "body-copy"},
            ui.HTML(
                "These are the diagnostic questions to raise in a leadership conversation. "
                "Their power is structural: at most companies, the honest answer to nearly every one "
                "is 'no one,' or 'whoever has a free hour.' "
                "Each question that lands without a clean answer is another piece of the case for the function. "
                "Click any question to see the framing behind it."
            ),
        ),
        *q_els,
    )


def _calc_capacity_embed():
    # Read the full HTML from project files and embed as iframe-equivalent
    # We'll embed the calculator JS/HTML inline
    calc_html = open(os.path.join(os.path.dirname(__file__), "ai-value-calculator.html")).read()
    # Strip the DOCTYPE/html/head/body wrappers, keep the page div and script
    # Extract just the inner content we need
    import re
    # Get the style block
    style_match = re.search(r'<style>(.*?)</style>', calc_html, re.DOTALL)
    style = style_match.group(1) if style_match else ""
    # Get everything inside body
    body_match = re.search(r'<body>(.*?)</body>', calc_html, re.DOTALL)
    body = body_match.group(1) if body_match else calc_html

    # Scope the style to avoid conflicts
    scoped = f'<style>.calc-capacity-scope {{ font-family: inherit; }} .calc-capacity-scope .page {{ max-width: 100%; padding: 0; }}</style><div class="calc-capacity-scope">{body}</div>'

    return ui.div(
        {"class": "pitch-section", "id": "calc-capacity"},
        ui.div({"class": "section-eyebrow"}, "Calculator 01"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("The <strong>hidden capacity cost</strong> of building AI tooling ad hoc."),
        ),
        ui.p(
            {"class": "body-copy"},
            "Adjust the inputs to match your team. Defaults are conservative and sourced. Your actual numbers are likely larger, not smaller.",
        ),
        ui.div(
            {"class": "calc-embed"},
            ui.div(
                {"class": "calc-header"},
                ui.div({"class": "calc-header-title"}, "Capacity Cost Model"),
                ui.div({"class": "calc-header-sub"}, "Hours diverted from real work - build + maintenance over 3 years"),
            ),
            ui.div({"class": "calc-body"}, ui.HTML(scoped)),
        ),
    )


def _calc_roi_embed():
    calc_html = open(os.path.join(os.path.dirname(__file__), "AI_Governance_ROI.html")).read()
    import re
    style_match = re.search(r'<style>(.*?)</style>', calc_html, re.DOTALL)
    style = style_match.group(1) if style_match else ""
    # This one is just a div.w - grab everything
    body = calc_html  # it's already a fragment

    scoped = f'<div class="calc-roi-scope">{body}</div>'

    return ui.div(
        {"class": "pitch-section", "id": "calc-roi"},
        ui.div({"class": "section-eyebrow"}, "Calculator 02"),
        ui.h2(
            {"class": "section-title"},
            ui.HTML("The <strong>compounding savings</strong> from AI governance across three phases."),
        ),
        ui.p(
            {"class": "body-copy"},
            "Crawl / Walk / Run is not just a risk framework - it is a savings framework. Each phase unlocks new optimization levers. The numbers below show what becomes possible, and when.",
        ),
        ui.div(
            {"class": "calc-embed"},
            ui.div(
                {"class": "calc-header"},
                ui.div({"class": "calc-header-title"}, "AI Governance ROI"),
                ui.div({"class": "calc-header-sub"}, "Cumulative savings across Crawl / Walk / Run phases"),
            ),
            ui.div({"class": "calc-body"}, ui.HTML(scoped)),
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
                    "The function I am describing is the answer to a set of questions Posit's "
                    "leadership has not yet had to answer formally - but will, as the AI build "
                    "mandate accelerates. The ask is a conversation to test whether those questions "
                    "land the way I think they will, and whether the function makes sense as I have described it."
                )
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
                    ui.div({"class": "ask-item-label"}, "Reporting line (hypothesis)"),
                    ui.div({"class": "ask-item-val"}, "COO or cross-functional ops owner"),
                ),
                ui.div(
                    {"class": "ask-item"},
                    ui.div({"class": "ask-item-label"}, "Starting team"),
                    ui.div({"class": "ask-item-val"}, "Two - delivery lead + ecosystem builder"),
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
                    "The reporting line recommendation assumes Posit has a COO or a clear "
                    "cross-functional operations owner. This is a hypothesis, not a confirmed fact. "
                    "The right answer comes from the discovery conversation, not this document."
                )
            ),
        ),
        ui.div(
            {"class": "callout green"},
            ui.p(
                ui.HTML(
                    "<strong>The compounding argument:</strong> A company that starts building "
                    "this function in 2026 does not have a one-year head start over a company "
                    "that starts in 2027. It has a year of production systems, real evaluation data, "
                    "and a team that has already made the expensive mistakes. That gap widens every month. "
                    "The cost of waiting is not just internal inefficiency. "
                    "For Posit specifically, it is also ceding the credibility story to someone else."
                )
            ),
        ),
        ui.div(
            {"class": "footnote-strip"},
            ui.HTML(
                "<b>A note on what this document is and is not:</b> "
                "This is a role proposal, not a one-sided sales pitch. "
                "The discovery questions exist because I do not know Posit's internal structure better than Posit does. "
                "Several items here are flagged as hypotheses to be validated - the Sales and Support backlog, "
                "the reporting line, whether an informal version of this function already exists. "
                "The honest version of this pitch includes the things I do not yet know."
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
        {"class": "pitch-shell"},
        _nav(),
        ui.div(
            {"class": "pitch-main"},
            _section_opening(),
            _section_why_now(),
            _section_function(),
            _section_backlog(),
            _section_framework(),
            _section_why_me(),
            _section_discovery(),
            _calc_capacity_embed(),
            _calc_roi_embed(),
            _section_ask(),
        ),
    ),
    ui.tags.script(ui.HTML(_build_js())),
)


def server(input, output, session):
    pass


app = App(app_ui, server)
