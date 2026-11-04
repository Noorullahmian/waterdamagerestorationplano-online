"use client";
import { useEffect } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";
// Tier 1 animation, actually running (Final added scope, 2026-11-04).
// Correction to the brief: a GSAP reveal WAS already wired (0.5s, 18px,
// hover-only card 3D, no Lenis) — that is why motion looked absent. This
// upgrade keeps the same progressive-enhancement rule (no CSS hiding:
// content is visible without JS; GSAP only animates FROM a translated /
// faded state when JS runs) and adds: Lenis smooth scroll, stronger
// scroll reveals (transform + opacity only, never layout properties,
// so no CLS), a scroll-into-view 3D tilt for cards that works on touch
// (hover 3D stays for pointer devices via CSS), and a homepage-only
// hero scrub (image scale/parallax + text fade/slide driven by scroll).
// No WebGL / R3F: held by the speed kill-switch, not added silently.
// Reduced motion: no Lenis, no reveals, no scrub — native scroll, static hero.
// Phone CTA / sticky call bar are never targeted by any animation.
export default function Reveal() {
  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) {
      window.__plano3Anim = { lenis: false, reduced: true, reveals: 0, heroScrub: false };
      document.documentElement.dataset.anim = "reduced-motion";
      return;
    }
    gsap.registerPlugin(ScrollTrigger);
    const lenis = new Lenis({ duration: 1.15, smoothWheel: true });
    lenis.on("scroll", ScrollTrigger.update);
    const raf = (time) => { lenis.raf(time * 1000); };
    gsap.ticker.add(raf);
    gsap.ticker.lagSmoothing(0);
    const els = gsap.utils.toArray(".reveal");
    els.forEach((el) => {
      const isCard = el.classList && el.classList.contains("card");
      const from = isCard
        ? { opacity: 0, y: 28, rotationX: 5, transformPerspective: 900 }
        : { opacity: 0, y: 28 };
      gsap.from(el, { ...from, duration: 0.9, ease: "power3.out", clearProps: "transform,opacity",
        scrollTrigger: { trigger: el, start: "top 88%", once: true } });
    });
    // Homepage hero scrub only (.hero-home exists on the home page alone).
    // Poster = the existing hero image; no video file is invented or needed.
    const hero = document.querySelector(".hero-home");
    let heroScrub = false;
    if (hero) {
      const img = hero.querySelector(".hero-img");
      const text = hero.querySelector(".hero-grid > div");
      if (img) {
        gsap.fromTo(img, { scale: 1, yPercent: 0 },
          { scale: 1.12, yPercent: -8, ease: "none",
            scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
        heroScrub = true;
      }
      if (text) {
        gsap.fromTo(text, { y: 0, opacity: 1 },
          { y: -50, opacity: 0.15, ease: "none",
            scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
        heroScrub = true;
      }
    }
    window.__plano3Anim = { lenis: true, reduced: false, reveals: els.length, heroScrub: heroScrub };
    document.documentElement.dataset.anim = "on";
    return () => {
      ScrollTrigger.getAll().forEach((t) => t.kill());
      gsap.ticker.remove(raf);
      lenis.destroy();
    };
  }, []);
  return null;
}
