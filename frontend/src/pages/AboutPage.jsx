import AboutHero from '../components/AboutHero';
import AboutVision from '../components/AboutVision';
import AboutMission from '../components/AboutMission';

const AboutPage = () => (
  <main>
    <AboutHero />

    <section className="section about-story">
      <div className="container about-story__inner">
        <p className="eyebrow">Giới thiệu thương hiệu</p>
        <h2>Câu chuyện TaloFood</h2>

        <p>
          TaloFood được xây dựng với mong muốn mang đến những bữa ăn nhanh ngon
          miệng, tiện lợi và gần gũi với khách hàng Việt Nam. Chúng tôi hướng đến
          một trải nghiệm đặt món đơn giản, phục vụ nhanh và phù hợp với nhịp sống
          năng động của học sinh, sinh viên, gia đình và nhân viên văn phòng.
        </p>

        <p>
          Từ những món gà rán giòn nóng, burger đậm vị, combo tiện lợi đến các món
          ăn nhẹ và thức uống quen thuộc, TaloFood luôn chú trọng sự cân bằng giữa
          hương vị, chất lượng và mức giá hợp lý. Mỗi món ăn được xây dựng để vừa
          dễ thưởng thức, vừa phù hợp với khẩu vị của nhiều nhóm khách hàng.
        </p>

        <p>
          Chúng tôi tập trung vào chất lượng món ăn, tốc độ phục vụ và trải nghiệm
          thân thiện trong từng đơn hàng. TaloFood mong muốn trở thành một địa chỉ
          quen thuộc, nơi khách hàng có thể dễ dàng lựa chọn một bữa ăn nhanh nóng
          hổi, ngon miệng và đáng tin cậy cho những khoảnh khắc hằng ngày.
        </p>
      </div>
    </section>

    <AboutVision />
    <AboutMission />
  </main>
);

export default AboutPage;
