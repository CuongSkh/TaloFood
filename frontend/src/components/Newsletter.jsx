const Newsletter = () => (
  <section className="newsletter-section" id="newsletter">
    <div className="container">
      <div className="newsletter-card">
        <div>
          <h2>ĐĂNG KÝ NHẬN ƯU ĐÃI</h2>
          <p>Nhận ngay voucher giảm giá 50% cho đơn hàng đầu tiên khi đăng ký thành viên.</p>
        </div>
        <form className="newsletter-form" onSubmit={(event) => event.preventDefault()}>
          <label className="sr-only" htmlFor="newsletter-email">Email của bạn</label>
          <input id="newsletter-email" type="email" placeholder="Nhập email của bạn..." />
          <button type="submit">ĐĂNG KÝ NGAY</button>
        </form>
      </div>
    </div>
  </section>
);

export default Newsletter;
