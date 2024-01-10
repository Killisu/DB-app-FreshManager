from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

available_tables = ['dish', 'dish_order', 'dish_ingredient', 'ingredient', 'orders', 'employees', 'order_employee']


class Dish(db.Model):
    __tablename__ = 'dish'
    dish_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    production_cost = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {'dish_id': self.dish_id, 'name': self.name, 'price': self.price, 'production_cost': self.production_cost, 'quantity': self.quantity}


class Dish_order(db.Model):
    __tablename__ = 'dish_order'
    dish_order_id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {'dish_order_id': self.dish_order_id, 'dish_id': self.dish_id, 'order_id': self.order_id}


class Dish_ingredient(db.Model):
    __tablename__ = 'dish_ingredient'
    dish_ingredient_id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, nullable=False)
    ingredient_id = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {'dish_ingredient_id': self.dish_ingredient_id, 'dish_id': self.dish_id, 'ingredient_id': self.ingredient_id}


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    supplier = db.Column(db.String(255), nullable=False)
    unit_of_measure = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {'ingredient_id': self.ingredient_id, 'name': self.name, 'supplier': self.supplier, 'unit_of_measure': self.unit_of_measure, 'quantity': self.quantity}


class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    total_cost = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def as_dict(self):
        return {'order_id': self.order_id, 'total_cost': self.total_cost, 'payment_method': self.payment_method, 'date': self.date}


class Employees(db.Model):
    __tablename__ = 'employees'
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    passport = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)


    def as_dict(self):
        return {'employee_id': self.employee_id, 'name': self.name, 'job_title': self.job_title, 'gender': self.gender, 'passport': self.passport, 'phone_number': self.phone_number}

class Order_employee(db.Model):
    __tablename__ = 'order_employee'
    order_employee_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {'order_employee_id': self.order_employee_id, 'order_id': self.order_id, 'employee_id': self.employee_id}
