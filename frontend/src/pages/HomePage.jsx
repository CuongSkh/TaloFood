import products from '../data/products.json';
import Banner from '../components/Banner';
import CategoryQuickLinks from '../components/CategoryQuickLinks';
import FeaturedProducts from '../components/FeaturedProducts';
import FeatureSection from '../components/FeatureSection';
import Newsletter from '../components/Newsletter';

const HomePage = () => {
  const featuredProducts = products.filter((product) => product.featured).slice(0, 4);

  return (
    <main>
      <Banner />
      <CategoryQuickLinks />
      <FeaturedProducts products={featuredProducts} />
      <FeatureSection />
      <Newsletter />
    </main>
  );
};

export default HomePage;
