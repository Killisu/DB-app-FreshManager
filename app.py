from flask import Flask, render_template, request
import sys
from sqlalchemy import text, func
from models import *

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show/<table_choice>', methods=['GET', 'POST'])
def show_table(table_choice):
    user_table_choice = table_choice.capitalize()
    if user_table_choice:
        selected_table = getattr(sys.modules[__name__], user_table_choice)

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        item_count = selected_table.query.count()

        paginated_data = selected_table.query.paginate(page=page, per_page=per_page)
        data = paginated_data.items
        data_list = [item.as_dict() for item in data]

        return render_template('show_table.html', data=data_list, table_name=user_table_choice,
                               pagination=paginated_data, item_count=item_count)


@app.route('/insertForm/<table_choice>')
def add_data_form(table_choice):
    if table_choice == 'dish':
        return render_template('Insert_to_dish.html', table_name=table_choice)
    if table_choice == 'ingredient':
        return render_template('Insert_to_ingredient.html', table_name=table_choice)
    if table_choice == 'orders':
        return render_template('Insert_to_orders.html', table_name=table_choice)
    if table_choice == 'employees':
        return render_template('Insert_to_employees.html', table_name=table_choice)
    if table_choice == 'dish_order':
        return render_template('Insert_to_dish_order.html', table_name=table_choice)
    if table_choice == 'dish_ingredient':
        return render_template('Insert_to_dish_ingredient.html', table_name=table_choice)
    if table_choice == 'order_employee':
        return render_template('Insert_to_order_employee.html', table_name=table_choice)


@app.route('/database/insert', methods=['GET', 'POST'])
def add_data():
    table_name = request.form['table_name']
    if table_name == 'dish':
        try:
            name = request.form['name']
            price = request.form['price']
            production_cost = request.form['production_cost']
            quantity = request.form['quantity']

            existing_data = db.session.query(Dish).filter(Dish.name == name).first()
            if existing_data:
                return render_template('res.html', result='Такая запись уже существует в данной таблице')

            query = text(
                f"INSERT INTO dish (dish_id, name, price, production_cost, quantity) VALUES ({db.session.query(func.max(Dish.dish_id)).scalar() + 1},'{name}', {price}, {production_cost}, {quantity});")
            db.session.execute(query)
            db.session.commit()

            return render_template('res.html', result='Данные добавлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_name == 'ingredient':
        try:
            name = request.form['name']
            supplier = request.form['supplier']
            unit_of_measure = request.form['unit_of_measure']
            quantity = request.form['quantity']

            existing_data = db.session.query(Ingredient).filter(Ingredient.name == name).first()
            if existing_data:
                return render_template('res.html', result='Такая запись уже существует в данной таблице')

            query = text(
                f"INSERT INTO ingredient (ingredient_id, name, supplier, unit_of_measure, quantity) VALUES ({db.session.query(func.max(Ingredient.ingredient_id)).scalar() + 1}, '{name}', '{supplier}', '{unit_of_measure}', {quantity});")
            db.session.execute(query)
            db.session.commit()

            return render_template('res.html', result='Данные добавлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_name == 'orders':
        try:
            total_cost = request.form['total_cost']
            payment_method = request.form['payment_method']
            data = request.form['data']

            # existing_data = db.session.query(Orders).filter(Orders.name == data).first()
            # if existing_data:
            #     return render_template('res.html', result='Такая запись уже существует в данной таблице')
            query = text(
                f"INSERT INTO orders (order_id, total_cost, payment_method, data) VALUES ({db.session.query(func.max(Orders.order_id)).scalar() + 1}, {total_cost}, '{payment_method}', '{date}');")
            db.session.execute(query)
            db.session.commit()

            return render_template('res.html', result='Данные добавлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_name == 'employees':
        try:
            name = request.form['name']
            job_title = request.form['job_title']
            gender = request.form['gender']
            passport = request.form['passport']
            phone_number = request.form['phone_number']

            existing_data = db.session.query(Employees).filter(Employees.name == name).first()
            if existing_data:
                return render_template('res.html', result='Такая запись уже существует в данной таблице')
            query = text(
                f"INSERT INTO employees (employee_id, name, job_title, gender, passport, phone_number) VALUES ({db.session.query(func.max(Employees.employee_id)).scalar() + 1}, '{name}', '{job_title}', '{gender}', '{passport}', '{phone_number}');")
            db.session.execute(query)
            db.session.commit()

            return render_template('res.html', result='Данные добавлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_name == 'dish_order':
        try:
            dish_id = request.form['dish_id']
            order_id = request.form['order_id']

            existing_data = db.session.query(Dish_order).filter(Dish_order.dish_id == request.form['dish_id']).filter(
                Dish_order.order_id == request.form['order_id']).first()
            if existing_data:
                return render_template('res.html', result='Такая запись уже существует в данной таблице')

            query = text(
                f"INSERT INTO dish_order (dish_id, order_id) VALUES ({dish_id}, {order_id});")
            db.session.execute(query)
            db.session.commit()

            return render_template('res.html', result='Данные добавлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_name == 'dish_ingredient':
        try:
            dish_id = request.form['dish_id']
            ingredient_id = request.form['ingredient_id']

            existing_data = db.session.query(Dish_ingredient).filter(
                Dish_ingredient.dish_id == request.form['dish_id']).filter(
                Dish_ingredient.ingredient_id == request.form['ingredient_id']).first()
            if existing_data:
                return render_template('res.html', result='Такая запись уже существует в данной таблице')

            query = text(
                f"INSERT INTO dish_ingredient (dish_id, ingredient_id) VALUES ({dish_id}, {ingredient_id});")
            db.session.execute(query)
            db.session.commit()

            return render_template('res.html', result='Данные добавлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_name == 'order_employee':
        try:
            order_id = request.form['order_id']
            employee_id = request.form['employee_id']

            existing_data = db.session.query(Order_employee).filter(
                Order_employee.order_id == request.form['order_id']).filter(
                Order_employee.employee_id == request.form['employee_id']).first()
            if existing_data:
                return render_template('res.html', result='Такая запись уже существует в данной таблице')

            query = text(
                f"INSERT INTO order_employee (order_id, employee_id) VALUES ({order_id}, {employee_id});")
            db.session.execute(query)
            db.session.commit()

            return render_template('res.html', result='Данные добавлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')


# @app.route('/show/<table_choice>/edit/<value>', methods=['GET', 'POST'])
# def show_edit_value(table_choice, value):
#     if table_choice == 'dish':
#         old_dish = db.session.query(Dish).filter(Dish.dish_id == value).first()
#         old_name = old_dish.name
#         old_price = old_dish.price
#         old_production_cost = old_dish.production_cost
#         old_quantity = old_dish.quantity
#         return render_template('Edit_dish.html', table_name=table_choice, dish_id=value, old_name=old_name,
#                                old_price=old_price,
#                                old_production_cost=old_production_cost, old_quantity=old_quantity)

@app.route('/show/<table_choice>/edit/<value>', methods=['GET', 'POST'])
def show_edit_value(table_choice, value):
    if table_choice == 'dish':
        old_dish = db.session.query(Dish).filter(Dish.dish_id == value).first()
        old_name = old_dish.name
        old_price = old_dish.price
        old_production_cost = old_dish.production_cost
        old_quantity = old_dish.quantity
        return render_template('Edit_dish.html', table_name=table_choice, dish_id=value, old_name=old_name,
                               old_price=old_price,
                               old_production_cost=old_production_cost, old_quantity=old_quantity)
    if table_choice == 'ingredient':
        old_ingredient = db.session.query(Ingredient).filter(Ingredient.ingredient_id == value).first()
        old_name = old_ingredient.name
        old_supplier = old_ingredient.supplier
        old_unit_of_measure = old_ingredient.unit_of_measure
        old_quantity = old_ingredient.quantity
        return render_template('Edit_ingredient.html', table_name=table_choice, ingredient_id=value, old_name=old_name,
                               old_supplier=old_supplier,
                               old_unit_of_measure=old_unit_of_measure, old_quantity=old_quantity)
    if table_choice == 'orders':
        old_orders = db.session.query(Orders).filter(Orders.order_id == value).first()
        old_total_cost = old_orders.total_cost
        old_payment_method = old_orders.payment_method
        old_date = old_orders.date
        return render_template('Edit_orders.html', table_name=table_choice, order_id=value,
                               old_total_cost=old_total_cost,
                               old_payment_method=old_payment_method, old_date=old_date)
    if table_choice == 'employees':
        old_employees = db.session.query(Employees).filter(Employees.employee_id == value).first()
        old_name = old_employees.name
        old_job_title = old_employees.job_title
        old_gender = old_employees.gender
        old_passport = old_employees.passport
        old_phone_number = old_employees.phone_number
        return render_template('Edit_employees.html', table_name=table_choice, employee_id=value, old_name=old_name,
                               old_job_title=old_job_title,
                               old_gender=old_gender, old_passport=old_passport, old_phone_number=old_phone_number)

    if table_choice == 'dish_order':
        dish_order = db.session.query(Dish_order).filter_by(dish_order_id=value).first()
        old_dish_id = dish_order.dish_id
        old_order_id = dish_order.order_id
        return render_template('Edit_dish_order.html', table_name=table_choice, dish_order_id=value,
                               old_dish_id=old_dish_id, old_order_id=old_order_id)

    if table_choice == 'dish_ingredient':
        dish_ingredient = db.session.query(Dish_ingredient).filter_by(dish_ingredient_id=value).first()
        old_dish_id = dish_ingredient.dish_id
        old_ingredient_id = dish_ingredient.ingredient_id
        return render_template('Edit_dish_ingredient.html', table_name=table_choice, dish_ingredient_id=value,
                               old_dish_id=old_dish_id,
                               old_ingredient_id=old_ingredient_id)
    if table_choice == 'order_employee':
        order_employee = db.session.query(Order_employee).filter_by(order_employee_id=value).first()
        old_order_id = order_employee.order_id
        old_employee_id = order_employee.employee_id
        return render_template('Edit_order_employee.html', table_name=table_choice, order_employee_id=value,
                               old_order_id=old_order_id, old_employee_id=old_employee_id)


@app.route('/edit_value', methods=['GET', 'POST'])
def edit_value():
    table_choice = request.form['table_name']
    if table_choice == 'dish':
        dish_id = request.form['dish_id']
        new_name = request.form['new_name']
        new_price = request.form['new_price']
        new_production_cost = request.form['new_production_cost']
        new_quantity = request.form['new_quantity']
        try:
            dish = db.session.query(Dish).filter(Dish.dish_id == dish_id).first()
            if dish:
                dish.name = new_name
                dish.price = new_price
                dish.production_cost = new_production_cost
                dish.quantity = new_quantity
                db.session.commit()
                return render_template('res.html', result='Данные обновлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')

    if table_choice == 'ingredient':
        ingredient_id = request.form['ingredient_id']
        new_name = request.form['new_name']
        new_supplier = request.form['new_supplier']
        new_unit_of_measure = request.form['new_unit_of_measure']
        new_quantity = request.form['new_quantity']
        try:
            ingredient = db.session.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
            if ingredient:
                ingredient.name = new_name
                ingredient.supplier = new_supplier
                ingredient.unit_of_measure = new_unit_of_measure
                ingredient.quantity = new_quantity
                db.session.commit()
                return render_template('res.html', result='Данные обновлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_choice == 'orders':
        order_id = request.form['order_id']
        new_total_cost = request.form['new_total_cost']
        new_payment_method = request.form['new_payment_method']
        new_date = request.form['new_date']
        try:
            orders = db.session.query(Orders).filter(Orders.order_id == order_id).first()
            if orders:
                orders.total_cost = new_total_cost
                orders.payment_method = new_payment_method
                orders.date = new_date
                db.session.commit()
                return render_template('res.html', result='Данные обновлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_choice == 'employees':
        employee_id = request.form['employee_id']
        new_name = request.form['new_name']
        new_job_title = request.form['new_job_title']
        new_passport = request.form['new_passport']
        new_phone_number = request.form['new_phone_number']
        try:
            employees = db.session.query(Employees).filter(Employees.employee_id == employee_id).first()
            if employees:
                employees.name = new_name
                employees.job_title = new_job_title
                employees.passport = new_passport
                employees.phone_number = new_phone_number
                db.session.commit()
                return render_template('res.html', result='Данные обновлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_choice == 'dish_order':
        dish_order_id = request.form['dish_order_id']
        new_dish_id = request.form['new_dish_id']
        new_order_id = request.form['new_order_id']
        try:
            dish_order = db.session.query(Dish_order).filter(Dish_order.dish_order_id == dish_order_id).first()
            if dish_order:
                dish_order.dish_id = new_dish_id
                dish_order.order_id = new_order_id
                db.session.commit()
                return render_template('res.html', result='Данные обновлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_choice == 'dish_ingredient':
        dish_ingredient_id = request.form['dish_ingredient_id']
        new_dish_id = request.form['new_dish_id']
        new_ingredient_id = request.form['new_ingredient_id']
        try:
            dish_ingredient = db.session.query(Dish_ingredient).filter(
                Dish_ingredient.dish_ingredient_id == dish_ingredient_id).first()
            if dish_ingredient:
                dish_ingredient.dish_id = new_dish_id
                dish_ingredient.ingredient_id = new_ingredient_id
                db.session.commit()
                return render_template('res.html', result='Данные обновлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_choice == 'order_employee':
        order_employee_id = request.form['order_employee_id']
        new_order_id = request.form['new_order_id']
        new_employee_id = request.form['new_employee_id']
        try:
            order_employee = db.session.query(Order_employee).filter(
                Order_employee.order_employee_id == order_employee_id).first()
            if order_employee:
                order_employee.order_id = new_order_id
                order_employee.employee_id = new_employee_id
                db.session.commit()
                return render_template('res.html', result='Данные обновлены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')


@app.route('/delete_value/<table_choice>/<value>', methods=['GET', 'POST'])
def delete_value(table_choice, value):
    if table_choice == 'dish_order':
        try:
            dish_order = db.session.query(Dish_order).filter_by(dish_order_id=value).first()
            if dish_order:
                db.session.delete(dish_order)
                db.session.commit()
                return render_template('res.html', result='Данные удалены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_choice == 'dish_ingredient':
        try:
            dish_ingredient = db.session.query(Dish_ingredient).filter_by(dish_ingredient_id=value).first()
            if dish_ingredient:
                db.session.delete(dish_ingredient)
                db.session.commit()
                return render_template('res.html', result='Данные удалены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')
    if table_choice == 'order_employee':
        try:
            order_employee = db.session.query(Order_employee).filter_by(order_employee_id=value).first()
            if order_employee:
                db.session.delete(order_employee)
                db.session.commit()
                return render_template('res.html', result='Данные удалены')
        except Exception as e:
            return render_template('res.html', result=f'Error: {str(e)}')


@app.route('/show/dish', methods=['GET', 'POST'])
def show_filter():
    value = request.form.get('filter')
    selected_table = Dish
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if value:
        old_filter = value
        paginated_data = selected_table.query.filter(selected_table.name.like(f'%{value}%')).paginate(page=page,
                                                                                                      per_page=per_page)
    else:
        old_filter = ''
        paginated_data = selected_table.query.paginate(page=page, per_page=per_page)
    data = paginated_data.items
    data_list = [item.as_dict() for item in data]

    item_count = selected_table.query.count()

    return render_template('selectFilterDish.html', data=data_list, table_name='dish',
                           pagination=paginated_data, old_filter=old_filter, item_count=item_count)


@app.route('/statistics', methods=['GET', 'POST'])
def show_statistics():
    dish_amount = db.session.query(Dish).count()
    ingredient_amount = db.session.query(Ingredient).count()
    employees_amount = db.session.query(Employees).count()
    orders_amount = db.session.query(Orders).count()
    dish_ingredient_amount = db.session.query(Dish_ingredient).count()
    dish_order_amount = db.session.query(Dish_order).count()
    order_employee_amount = db.session.query(Order_employee).count()
    database_items_amount = dish_amount + ingredient_amount + employees_amount + orders_amount + dish_ingredient_amount + dish_order_amount + order_employee_amount
    return render_template('Stats.html', dish_amount=dish_amount, ingredient_amount=ingredient_amount,
                           employees_amount=employees_amount, orders_amount=orders_amount,
                           dish_ingredient_amount=dish_ingredient_amount, dish_order_amount=dish_order_amount, order_employee_amount=order_employee_amount,
                           database_items_amount=database_items_amount)



if __name__ == "__main__":
    app.run(debug=True)
