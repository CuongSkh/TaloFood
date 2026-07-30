import { useEffect, useMemo, useRef, useState } from 'react';
import products from '../data/products.json';
import MenuHero from '../components/MenuHero';
import MenuCategoryNav from '../components/MenuCategoryNav';
import MenuSection from '../components/MenuSection';
import ProductList from '../components/ProductList';

const categories = [
  { id: 'mon-moi', label: 'Món mới' },
  { id: 'combo', label: 'Combo' },
  { id: 'ga-ran', label: 'Gà rán' },
  { id: 'burger', label: 'Burger' },
  { id: 'thuc-an-nhe', label: 'Thức ăn nhẹ' },
  { id: 'thuc-uong', label: 'Thức uống' },
];

const normalizeText = (value) =>
  value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

const getStickyOffset = () => {
  const isMobile = window.matchMedia('(max-width: 680px)').matches;
  const headerHeight = isMobile ? 68 : 76;
  const categoryHeight = isMobile ? 58 : 68;
  return headerHeight + categoryHeight;
};

const ProductPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState(categories[0].id);
  const sectionRefs = useRef({});
  const isSearching = searchTerm.trim().length > 0;

  const groupedProducts = useMemo(
    () =>
      Object.fromEntries(
        categories.map((category) => [
          category.id,
          products.filter((product) => product.category === category.label),
        ]),
      ),
    [],
  );

  const searchResults = useMemo(() => {
    const keyword = normalizeText(searchTerm.trim());
    if (!keyword) return [];

    return products.filter((product) =>
      normalizeText(product.name).includes(keyword),
    );
  }, [searchTerm]);

  useEffect(() => {
    if (isSearching) return undefined;

    let frameId = null;
    let observer = null;

    const updateActiveCategory = () => {
      frameId = null;
      const activationLine = getStickyOffset() + 24;
      let currentId = categories[0].id;

      // Mục active là section cuối cùng đã đi qua đường ngay dưới hai thanh sticky.
      categories.forEach(({ id }) => {
        const section = sectionRefs.current[id];
        if (section?.getBoundingClientRect().top <= activationLine) {
          currentId = id;
        }
      });

      setActiveCategory((previousId) =>
        previousId === currentId ? previousId : currentId,
      );
    };

    const scheduleUpdate = () => {
      if (frameId !== null) return;
      frameId = window.requestAnimationFrame(updateActiveCategory);
    };

    const createObserver = () => {
      observer?.disconnect();

      const activationLine = getStickyOffset() + 24;
      const bottomMargin = Math.max(
        0,
        window.innerHeight - activationLine - 2,
      );

      // Thu vùng quan sát thành một đường mỏng ngay dưới Header + category bar.
      // Observer chỉ kích hoạt khi ranh giới section đi qua đúng đường này.
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

    const handleResize = () => {
      createObserver();
      scheduleUpdate();
    };

    window.addEventListener('resize', handleResize);

    return () => {
      observer?.disconnect();
      window.removeEventListener('resize', handleResize);
      if (frameId !== null) window.cancelAnimationFrame(frameId);
    };
  }, [isSearching]);

  const handleCategorySelect = (id) => {
    const targetSection = sectionRefs.current[id];
    if (!targetSection) return;

    setSearchTerm('');
    setActiveCategory(id);

    const targetTop =
      targetSection.getBoundingClientRect().top +
      window.scrollY -
      getStickyOffset() -
      16;

    window.scrollTo({
      top: Math.max(0, targetTop),
      behavior: 'smooth',
    });
  };

  return (
    <main className="menu-page">
      <MenuHero />
      <MenuCategoryNav
        categories={categories}
        activeId={activeCategory}
        onSelect={handleCategorySelect}
      />

      <div className="container menu-page__content">
        <div className="menu-search">
          <label htmlFor="menu-search-input" className="sr-only">
            Tìm món ăn
          </label>
          <span aria-hidden="true">⌕</span>
          <input
            id="menu-search-input"
            type="search"
            placeholder="Tìm món ăn bạn yêu thích..."
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
          />
        </div>

        {isSearching ? (
          <section className="menu-search-results" aria-live="polite">
            <div className="menu-section__heading">
              <h2>Kết quả tìm kiếm</h2>
              <span>{searchResults.length} món phù hợp</span>
            </div>
            {searchResults.length > 0 ? (
              <ProductList products={searchResults} />
            ) : (
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
              sectionRef={(element) => {
                sectionRefs.current[category.id] = element;
              }}
            />
          ))
        )}
      </div>
    </main>
  );
};

export default ProductPage;
