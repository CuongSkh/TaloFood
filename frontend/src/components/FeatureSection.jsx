const features = [
  {
    icon: '◴',
    title: 'Giao nhanh 30 phút',
    description: 'Hệ thống cửa hàng phủ khắp giúp đơn hàng đến tay bạn trong nháy mắt.',
  },
  {
    icon: '♨',
    title: 'Nóng hổi giòn tan',
    description: 'Quy trình đóng gói chuyên nghiệp giữ trọn hương vị và độ giòn của món ăn.',
  },
  {
    icon: '✺',
    title: 'Nguồn nguyên liệu sạch',
    description: '100% nguyên liệu tươi sống, đạt chuẩn vệ sinh an toàn thực phẩm VietGAP.',
  },
];

const FeatureSection = () => (
  <section className="section feature-section" id="features">
    <div className="container">
      <div className="section-heading section-heading--center">
        <h2>VÌ SAO NÊN CHỌN TALOFOOD?</h2>
        <span className="heading-underline" />
      </div>
      <div className="feature-grid">
        {features.map((feature) => (
          <article className="feature-card" key={feature.title}>
            <span className="feature-card__icon" aria-hidden="true">{feature.icon}</span>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </article>
        ))}
      </div>
    </div>
  </section>
);

export default FeatureSection;
