import axios from 'axios';

export const getApiErrorMessage = (error, fallbackMessage = 'Đã xảy ra lỗi.') => {
  if (!axios.isAxiosError(error)) return fallbackMessage;
  if (error.code === 'ECONNABORTED') return 'Yêu cầu mất quá nhiều thời gian. Vui lòng thử lại.';
  if (!error.response) return 'Không thể kết nối đến máy chủ TaloFood.';

  const detail = error.response.data?.detail;
  const status = error.response.status;
  if (status === 401) return detail || 'Email hoặc mật khẩu không chính xác.';
  if (status === 403) return detail || 'Bạn không có quyền thực hiện thao tác này.';
  if (status === 404) return detail || 'Không tìm thấy dữ liệu.';
  if (status === 409) return detail || 'Dữ liệu đã tồn tại.';
  if (status === 422) {
    const validationMessage = Array.isArray(detail) ? detail[0]?.msg : detail;
    return validationMessage || 'Thông tin nhập vào chưa hợp lệ. Vui lòng kiểm tra lại.';
  }
  if (status >= 500) return 'Máy chủ đang gặp sự cố.';
  return detail || fallbackMessage;
};
