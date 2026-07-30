import axios from 'axios';

export const getApiErrorMessage = (error, fallbackMessage = 'Đã xảy ra lỗi.') => {
  if (!axios.isAxiosError(error)) return fallbackMessage;

  if (error.code === 'ECONNABORTED') {
    return 'Yêu cầu mất quá nhiều thời gian. Vui lòng thử lại.';
  }

  if (!error.response) {
    return 'Không thể kết nối đến máy chủ TaloFood.';
  }

  const status = error.response.status;
  if (status === 404) return 'Không tìm thấy món ăn.';
  if (status === 422) return 'Dữ liệu món ăn không hợp lệ.';
  if (status >= 500) return 'Máy chủ đang gặp sự cố.';

  return error.response.data?.detail || fallbackMessage;
};
