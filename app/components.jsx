"use client";
import { useState } from "react";

// ANIMATIONS OFF (user order 2026-11-05): the Lenis smooth scroll +
// GSAP ScrollTrigger reveals + hero scrub made the whole page lag and
// fly away during scrolling. ALL motion is removed: no Lenis, no GSAP,
// no ScrollTrigger, no ticker, no hero scrub. Content renders in its
// final state with native scroll. The `reveal` classes gen4.py adds to
// cards / trust-bands are inert (no CSS rule, no JS) and are left as-is.
// Hover-only card transitions in globals.css are kept (hover, not scroll).

export default function Reveal() {
  return null;
}

// Mobile header controls (<=820px): hamburger + small call button.
// Desktop header is unchanged (inline nav + Call 24/7 button in layout.jsx).
// The menu opens INSTANTLY (no slide/fly — animations are off).
export function MobileNav() {
  const [open, setOpen] = useState(false);
  const links = [
    ["Home", "/"],
    ["Services", "/services/"],
    ["Areas", "/areas/"],
    ["Guides", "/guides/"],
    ["About", "/about/"],
    ["Contact", "/contact/"],
  ];
  return (
    <div className="mobile-nav">
      <a className="header-call-small" href="tel:+19724727917" aria-label="Call (972) 472-7917">
        <svg className="call-ico" viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z" /></svg>
        <span>Call</span>
      </a>
      <button type="button" className="hamburger" aria-expanded={open} aria-controls="mobile-menu" aria-label={open ? "Close menu" : "Open menu"} onClick={() => setOpen(!open)}>
        <span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>
      </button>
      {open && (
        <nav className="mobile-menu-panel" id="mobile-menu" aria-label="Mobile">
          {links.map(([label, href]) => (
            <a key={href} href={href} onClick={() => setOpen(false)}>{label}</a>
          ))}
          <a className="btn-call mobile-menu-call" href="tel:+19724727917" onClick={() => setOpen(false)}>Call 24/7: <span className="nowrap">(972) 472-7917</span></a>
        </nav>
      )}
    </div>
  );
}
