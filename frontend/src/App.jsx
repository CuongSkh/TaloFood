import { Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import ProductPage from './pages/ProductPage';
import ProductDetailPage from './pages/ProductDetailPage';
import NotFoundPage from './pages/NotFoundPage';
import './App.css';

const App = () => (
  <>
    <Header />
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/products" element={<ProductPage />} />
      <Route path="/products/:id" element={<ProductDetailPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
    <Footer />
  </>
);

export default App;
