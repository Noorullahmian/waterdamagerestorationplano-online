import "./globals.css";
import Reveal from "./components";
export const metadata = { metadataBase: new URL("https://waterdamagerestorationplano.online"), title: { default: "Water Damage Restoration Plano, TX | 24/7 Water Removal" }, description: "Water damage in Plano, TX? 24/7 water extraction, thermal moisture mapping & structural drying across every Plano ZIP. Call (972) 472-7917 now.", icons: { icon: "/favicon.svg", apple: "/favicon.png" } };
export default function RootLayout({ children }) {
  return (<html lang="en"><body>
    <header className="site-header"><div className="wrap header-inner">
      <a className="brand" href="/">Water Damage Restoration <span>Plano</span></a>
      <nav className="main-nav" aria-label="Main">
        <a href="/">Home</a><a href="/services/">Services</a><a href="/areas/">Areas</a><a href="/guides/">Guides</a><a href="/about/">About</a><a href="/contact/">Contact</a>
      </nav>
      <a className="header-call" href="tel:+19724727917">Call 24/7: <span className="nowrap">(972) 472-7917</span></a>
    </div></header>
    <main>{children}</main>
    <footer className="site-footer"><div className="wrap footer-grid">
      <div><h3>Water Damage Restoration Plano</h3><p>Plano, TX &amp; Collin County<br /><a href="tel:+19724727917">(972) 472-7917</a><br />Open 24/7</p></div>
      <div><h3>Best Services</h3><ul>
        <li><a href="/emergency-water-damage/">24/7 Emergency Water Damage Cleanup</a></li>
        <li><a href="/water-extraction/">Standing Water Extraction</a></li>
        <li><a href="/structural-drying/">Structural Drying</a></li>
        <li><a href="/burst-pipe-cleanup/">Burst &amp; Frozen Pipe Cleanup</a></li>
        <li><a href="/slab-leak/">Slab Leak Water Damage</a></li>
        <li><a href="/sewage-cleanup/">Sewage Backup Cleanup</a></li>
      </ul></div>
      <div><h3>Quick Links</h3><ul>
        <li><a href="/services/">All Services</a></li><li><a href="/areas/">Service Areas</a></li>
        <li><a href="/guides/">Guides</a></li><li><a href="/about/">About Us</a></li><li><a href="/contact/">Contact Us</a></li>
      </ul></div>
      <div><h3>Emergency Help</h3><p>Water spreading right now? Call first, then shut off the water and power to wet rooms. Crews stage along US-75, the Dallas North Tollway, the George Bush Turnpike and SH-121.</p><p><a className="btn-call" href="tel:+19724727917">Call 24/7: <span className="nowrap">(972) 472-7917</span></a></p></div>
    </div>
    <div className="footer-bottom"><div className="wrap">Water Damage Restoration Plano · Plano, TX &amp; Collin County · (972) 472-7917 · Open 24/7</div></div>
    </footer>
    <a className="mobile-call-bar" href="tel:+19724727917">Call Now: (972) 472-7917</a>
    <Reveal />
  </body></html>);
}
