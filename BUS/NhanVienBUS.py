from DAO.NhanVienDAO import NhanVienDAO # type: ignore
from DTO.NhanVienDTO import NhanVienDTO

class NhanVienBUS:
    def __init__(self):
        self.nhanvien_dao = NhanVienDAO()
    
    def get_all_nhanvien(self):
        """Lấy danh sách tất cả nhân viên"""
        return self.nhanvien_dao.get_all_nhanvien()
    
    def add_nhanvien(self, ma_nv, ho_ten, chuc_vu, so_dien_thoai, email, ngay_vao_lam):
        """Thêm nhân viên mới"""
        nhanvien = NhanVienDTO(ma_nv, ho_ten, chuc_vu, so_dien_thoai, email, ngay_vao_lam)
        return self.nhanvien_dao.insert(nhanvien)
    
    def update_nhanvien(self, ma_nv, ho_ten, chuc_vu, so_dien_thoai, email, ngay_vao_lam):
        """Cập nhật thông tin nhân viên"""
        nhanvien = NhanVienDTO(ma_nv, ho_ten, chuc_vu, so_dien_thoai, email, ngay_vao_lam)
        return self.nhanvien_dao.update(nhanvien)
    
    def delete_nhanvien(self, ma_nv):
        """Xóa nhân viên"""
        return self.nhanvien_dao.delete(ma_nv)
    
    def search_nhanvien(self, keyword):
        """Tìm kiếm nhân viên theo từ khóa"""
        return self.nhanvien_dao.search(keyword)
