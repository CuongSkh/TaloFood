import { useEffect, useState } from 'react';
import Banner from '../components/Banner';
import CategoryQuickLinks from '../components/CategoryQuickLinks';
import FeaturedProducts from '../components/FeaturedProducts';
import FeatureSection from '../components/FeatureSection';
import Newsletter from '../components/Newsletter';
import { productsApi } from '../api/productsApi';

const HomePage = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);

  useEffect(() => {
    let active = true;
    productsApi.getAll({ featured: true, page: 1, size: 4 })
      .then((result) => {
        if (active) setFeaturedProducts(result.items);
      })
      .catch(() => {
        if (active) setFeaturedProducts([]);
      });
    return () => {
      active = false;
    };
  }, []);

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
