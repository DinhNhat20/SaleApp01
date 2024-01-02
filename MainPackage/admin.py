from MainPackage import db, app, utils
from MainPackage.models import Category, Product, Tag, User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class ProductView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    column_exclude_list = ['image']
    column_filters = ['name', 'price']
    column_searchable_list = ['name', 'description']
    column_labels = {
        'id': 'Mã sản phẩm',
        'name': 'Tên',
        'description': 'Mô tả',
        'price': 'Giá',
        'category_id': 'Danh mục',
        'active': 'Còn kinh doanh',
        'created_date': 'Ngày tạo',
        'image': 'Ảnh sản phẩm'
    }
    form_excluded_columns = ['tags']


# class authenticatedBaseView(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated


class logoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class statsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = utils.product_count_by_cate()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app,
              name='QUẢN TRỊ BÁN HÀNG ONLINE',
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())

admin.add_view(AuthenticatedModelView(Category, db.session, name='Danh mục'))
admin.add_view(ProductView(Product, db.session, name='Sản phẩm'))
admin.add_view(AuthenticatedModelView(Tag, db.session, name='Nhãn'))
admin.add_view(AuthenticatedModelView(User, db.session, name='Người dùng'))
admin.add_view(logoutView(name='Đăng xuất'))
admin.add_view(statsView(name='Thống kê báo cáo'))
