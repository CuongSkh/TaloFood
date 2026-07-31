import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = () => {
  const { isAuthenticated, isAuthLoading } = useAuth();
  const location = useLocation();
  if (isAuthLoading) return <main className="auth-route-status">Đang kiểm tra phiên đăng nhập...</main>;
  if (!isAuthenticated) return <Navigate to="/login" replace state={{ from: location }} />;
  return <Outlet />;
};

export default ProtectedRoute;
