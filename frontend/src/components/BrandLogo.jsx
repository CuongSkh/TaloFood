const BrandLogo = ({ compact = false }) => (
  <a className={`brand-logo${compact ? ' brand-logo--compact' : ''}`} href="#top" aria-label="TaloFood - Trang chủ">
    <span className="brand-logo__mark">TF</span>
    <span className="brand-logo__text">TALOFOOD</span>
  </a>
);

export default BrandLogo;
