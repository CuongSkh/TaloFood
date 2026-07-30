const values = [
  {
    icon: '♡',
    title: 'Ngon miệng',
    text: 'Chú trọng hương vị và chất lượng trong từng món ăn.',
  },
  {
    icon: '✓',
    title: 'An toàn',
    text: 'Ưu tiên nguyên liệu phù hợp và quy trình chế biến rõ ràng.',
  },
  {
    icon: '↗',
    title: 'Phục vụ nhanh',
    text: 'Tối ưu trải nghiệm đặt món, nhận món và chăm sóc khách hàng.',
  },
];

const commitments = [
  {
    title: 'Món ăn chất lượng',
    text: 'Chú trọng nguyên liệu, hương vị và sự ổn định trong từng phần ăn.',
  },
  {
    title: 'Phục vụ chuyên nghiệp',
    text: 'Đề cao sự nhanh chóng, tận tâm và thân thiện trong mỗi đơn hàng.',
  },
  {
    title: 'Không gian sạch sẽ, gần gũi',
    text: 'Hướng đến trải nghiệm thoải mái, gọn gàng và phù hợp với khách hàng Việt.',
  },
  {
    title: 'Giá trị hợp lý',
    text: 'Mang đến nhiều lựa chọn ngon miệng với mức giá phù hợp cho nhu cầu hằng ngày.',
  },
];

const AboutMission = () => (
  <section className="section about-mission">
    <div className="container">
      <div className="section-heading section-heading--center">
        <p className="eyebrow">Giá trị phục vụ</p>
        <h2>Sứ mệnh của TaloFood</h2>
        <span className="heading-underline" />

        <div className="about-mission__copy">
          <p>
            TaloFood hướng đến trở thành điểm đến ẩm thực nhanh được khách hàng yêu
            thích, nơi mỗi bữa ăn không chỉ ngon miệng mà còn mang lại cảm giác tiện
            lợi, thân thiện và đáng nhớ. Chúng tôi không ngừng hoàn thiện chất lượng
            món ăn và dịch vụ để khách hàng luôn có những lựa chọn quen thuộc như gà
            rán, burger, khoai tây chiên, combo và nhiều món ăn nhẹ hấp dẫn.
          </p>

          <p>
            TaloFood cam kết xây dựng trải nghiệm phục vụ dựa trên bốn giá trị cốt
            lõi: chất lượng món ăn, dịch vụ chuyên nghiệp, môi trường sạch sẽ và mức
            giá hợp lý. Đây là nền tảng giúp thương hiệu tạo dựng niềm tin và đồng
            hành cùng nhu cầu ăn uống hằng ngày của người Việt.
          </p>
        </div>
      </div>

      <div className="about-commitments" aria-label="Cam kết phục vụ của TaloFood">
        {commitments.map((item) => (
          <div className="about-commitment" key={item.title}>
            <span className="about-commitment__dot" aria-hidden="true" />
            <p>
              <strong>{item.title}:</strong> {item.text}
            </p>
          </div>
        ))}
      </div>

      <div className="about-values">
        {values.map((value) => (
          <article className="about-value-card" key={value.title}>
            <span className="about-value-card__icon">{value.icon}</span>
            <h3>{value.title}</h3>
            <p>{value.text}</p>
          </article>
        ))}
      </div>
    </div>
  </section>
);

export default AboutMission;
