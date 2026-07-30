import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import MenuHero from '../components/MenuHero';
import MenuCategoryNav from '../components/MenuCategoryNav';
import MenuSection from '../components/MenuSection';
import ProductList from '../components/ProductList';
import { productsApi } from '../api/productsApi';

const categories = [
  { id: 'mon-moi', label: 'Món mới' },
  { id: 'combo', label: 'Combo' },
  { id: 'ga-ran', label: 'Gà rán' },
  { id: 'burger', label: 'Burger' },
  { id: 'thuc-an-nhe', label: 'Thức ăn nhẹ' },
  { id: 'thuc-uong', label: 'Thức uống' },
];

const getStickyOffset = () => {
  const isMobile = window.matchMedia('(max-width: 680px)').matches;
  return (isMobile ? 68 : 76) + (isMobile ? 58 : 68);
};

const ProductPage = () => {
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState(categories[0].id);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const sectionRefs = useRef({});
  const isSearching = debouncedSearch.trim().length > 0;

  useEffect(() => {
    const timer = window.setTimeout(() => setDebouncedSearch(searchTerm.trim()), 400);
    return () => window.clearTimeout(timer);
  }, [searchTerm]);

  const loadProducts = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const response = await productsApi.getAll({
        size: 100,
        ...(debouncedSearch ? { search: debouncedSearch } : {}),
      });
      setProducts(response.items);
    } catch (requestError) {
      setProducts([]);
      setError(requestError.userMessage || 'Không thể tải thực đơn. Vui lòng kiểm tra kết nối và thử lại.');
    } finally {
      setLoading(false);
    }
  }, [debouncedSearch]);

  useEffect(() => {
    loadProducts();
  }, [loadProducts]);

  const groupedProducts = useMemo(
    () => Object.fromEntries(
      categories.map((category) => [
        category.id,
        products.filter((product) => product.category === category.label),
      ]),
    ),
    [products],
  );

  useEffect(() => {
    if (isSearching || loading || error) return undefined;

    let frameId = null;
    let observer = null;
    const updateActiveCategory = () => {
      frameId = null;
      const activationLine = getStickyOffset() + 24;
      let currentId = categories[0].id;
      categories.forEach(({ id }) => {
        const section = sectionRefs.current[id];
        if (section?.getBoundingClientRect().top <= activationLine) currentId = id;
      });
      setActiveCategory((previousId) => previousId === currentId ? previousId : currentId);
    };
    const scheduleUpdate = () => {
      if (frameId === null) frameId = window.requestAnimationFrame(updateActiveCategory);
    };
    const createObserver = () => {
      observer?.disconnect();
      const activationLine = getStickyOffset() + 24;
      const bottomMargin = Math.max(0, window.innerHeight - activationLine - 2);
      observer = new IntersectionObserver(scheduleUpdate, {
        root: null,
        rootMargin: `-${activationLine}px 0px -${bottomMargin}px 0px`,
        threshold: 0,
      });
      categories.forEach(({ id }) => {
        const section = sectionRefs.current[id];
        if (section) observer.observe(section);
      });
    };
    createObserver();
    updateActiveCategory();
    const handleResize = () => { createObserver(); scheduleUpdate(); };
    window.addEventListener('resize', handleResize);
    return () => {
      observer?.disconnect();
      window.removeEventListener('resize', handleResize);
      if (frameId !== null) window.cancelAnimationFrame(frameId);
    };
  }, [isSearching, loading, error, products]);

  const handleCategorySelect = (id) => {
    const targetSection = sectionRefs.current[id];
    if (!targetSection) return;
    setSearchTerm('');
    setDebouncedSearch('');
    setActiveCategory(id);
    const targetTop = targetSection.getBoundingClientRect().top + window.scrollY - getStickyOffset() - 16;
    window.scrollTo({ top: Math.max(0, targetTop), behavior: 'smooth' });
  };

  return (
    <main className="menu-page">
      <MenuHero />
      <MenuCategoryNav categories={categories} activeId={activeCategory} onSelect={handleCategorySelect} />

      <div className="container menu-page__content">
        <div className="menu-search">
          <label htmlFor="menu-search-input" className="sr-only">Tìm món ăn</label>
          <span aria-hidden="true">⌕</span>
          <input
            id="menu-search-input"
            type="search"
            placeholder="Tìm món ăn bạn yêu thích..."
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
          />
        </div>

        {loading ? (
          <div className="menu-status" aria-live="polite">Đang tải thực đơn...</div>
        ) : error ? (
          <div className="menu-status menu-status--error" role="alert">
            <strong>Không thể tải thực đơn.</strong>
            <p>{error}</p>
            <button type="button" className="button button--primary" onClick={loadProducts}>Thử lại</button>
          </div>
        ) : isSearching ? (
          <section className="menu-search-results" aria-live="polite">
            <div className="menu-section__heading">
              <h2>Kết quả tìm kiếm</h2>
              <span>{products.length} món phù hợp</span>
            </div>
            {products.length > 0 ? <ProductList products={products} /> : (
              <div className="menu-empty-state">
                <strong>Không tìm thấy món ăn phù hợp.</strong>
                <p>Hãy thử tìm bằng tên món khác.</p>
              </div>
            )}
          </section>
        ) : (
          categories.map((category) => (
            <MenuSection
              key={category.id}
              category={category}
              products={groupedProducts[category.id]}
              sectionRef={(element) => { sectionRefs.current[category.id] = element; }}
            />
          ))
        )}
      </div>
    </main>
  );
};

export default ProductPage;
