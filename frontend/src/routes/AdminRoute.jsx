import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AdminRoute = () => {
  const { isAuthenticated, isAdmin, isAuthLoading } = useAuth();
  const location = useLocation();
  if (isAuthLoading) return <main className="auth-route-status">Đang kiểm tra quyền truy cập...</main>;
  if (!isAuthenticated) return <Navigate to="/login" replace state={{ from: location }} />;
  if (!isAdmin) return <Navigate to="/unauthorized" replace />;
  return <Outlet />;
};

export default AdminRoute;
