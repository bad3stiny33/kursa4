from fastapi import FastAPI
import sqlite3
from datetime import date

app = FastAPI()

# Создаем базу данных и таблицы
conn = sqlite3.connect("car_rental.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cars (
        car_id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        color TEXT NOT NULL,
        license_plate TEXT UNIQUE NOT NULL,
        daily_rate REAL NOT NULL,
        is_available BOOLEAN DEFAULT 1,
        mileage INTEGER DEFAULT 0,
        fuel_type TEXT DEFAULT 'petrol'
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        driver_license TEXT UNIQUE NOT NULL,
        address TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rentals (
        rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        rental_date DATE NOT NULL,
        return_date DATE,
        planned_return_date DATE NOT NULL,
        total_cost REAL,
        mileage_start INTEGER NOT NULL,
        mileage_end INTEGER,
        status TEXT DEFAULT 'active',
        FOREIGN KEY (car_id) REFERENCES Cars (car_id),
        FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Maintenance (
        maintenance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER NOT NULL,
        maintenance_date DATE NOT NULL,
        maintenance_type TEXT NOT NULL,
        description TEXT,
        cost REAL NOT NULL,
        mileage INTEGER NOT NULL,
        FOREIGN KEY (car_id) REFERENCES Cars (car_id)
    )
''')

conn.commit()
conn.close()

# Автомобили
@app.post("/cars/")
def create_car(brand: str, model: str, year: int, color: str, license_plate: str, daily_rate: float, mileage: int = 0, fuel_type: str = "petrol"):
    """Добавление автомобиля"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Cars (brand, model, year, color, license_plate, daily_rate, mileage, fuel_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (brand, model, year, color, license_plate, daily_rate, mileage, fuel_type)
        )
        conn.commit()
        car_id = cursor.lastrowid
        return {"car_id": car_id, "message": "Автомобиль добавлен"}
    except sqlite3.IntegrityError:
        return {"error": "Автомобиль с таким номерным знаком уже существует"}
    except Exception as e:
        return {"error": f"Ошибка добавления автомобиля: {str(e)}"}
    finally:
        conn.close()

@app.get("/cars/")
def get_cars(available_only: bool = False):
    """Получить все автомобили"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    
    if available_only:
        cursor.execute("SELECT car_id, brand, model, year, color, license_plate, daily_rate, is_available, mileage, fuel_type FROM Cars WHERE is_available = 1")
    else:
        cursor.execute("SELECT car_id, brand, model, year, color, license_plate, daily_rate, is_available, mileage, fuel_type FROM Cars")
    
    cars = cursor.fetchall()
    conn.close()
    
    if not cars:
        return {"error": "Список автомобилей пуст"}
    
    return [{
        "car_id": c[0], 
        "brand": c[1], 
        "model": c[2], 
        "year": c[3], 
        "color": c[4], 
        "license_plate": c[5], 
        "daily_rate": c[6], 
        "is_available": bool(c[7]),
        "mileage": c[8],
        "fuel_type": c[9]
    } for c in cars]

@app.put("/cars/{car_id}")
def update_car(car_id: int, brand: str = None, model: str = None, year: int = None, color: str = None, 
               license_plate: str = None, daily_rate: float = None, is_available: bool = None, 
               mileage: int = None, fuel_type: str = None):
    """Обновление информации об автомобиле"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    try:
        # Проверяем существование автомобиля
        cursor.execute("SELECT * FROM Cars WHERE car_id = ?", (car_id,))
        car = cursor.fetchone()
        
        if not car:
            return {"error": "Автомобиль не найден"}
        
        # Собираем поля для обновления
        update_fields = []
        update_values = []
        
        if brand is not None:
            update_fields.append("brand = ?")
            update_values.append(brand)
        if model is not None:
            update_fields.append("model = ?")
            update_values.append(model)
        if year is not None:
            update_fields.append("year = ?")
            update_values.append(year)
        if color is not None:
            update_fields.append("color = ?")
            update_values.append(color)
        if license_plate is not None:
            update_fields.append("license_plate = ?")
            update_values.append(license_plate)
        if daily_rate is not None:
            update_fields.append("daily_rate = ?")
            update_values.append(daily_rate)
        if is_available is not None:
            update_fields.append("is_available = ?")
            update_values.append(1 if is_available else 0)
        if mileage is not None:
            update_fields.append("mileage = ?")
            update_values.append(mileage)
        if fuel_type is not None:
            update_fields.append("fuel_type = ?")
            update_values.append(fuel_type)
        
        if not update_fields:
            return {"error": "Нет данных для обновления"}
        
        update_values.append(car_id)
        query = f"UPDATE Cars SET {', '.join(update_fields)} WHERE car_id = ?"
        
        cursor.execute(query, update_values)
        conn.commit()
        
        return {"message": "Информация об автомобиле обновлена"}
    except Exception as e:
        return {"error": f"Ошибка обновления автомобиля: {str(e)}"}
    finally:
        conn.close()

# Клиенты
@app.post("/customers/")
def create_customer(first_name: str, last_name: str, email: str, phone: str, driver_license: str, address: str = ""):
    """Добавление клиента"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Customers (first_name, last_name, email, phone, driver_license, address) VALUES (?, ?, ?, ?, ?, ?)",
            (first_name, last_name, email, phone, driver_license, address)
        )
        conn.commit()
        customer_id = cursor.lastrowid
        return {"customer_id": customer_id, "message": "Клиент добавлен"}
    except sqlite3.IntegrityError:
        return {"error": "Клиент с таким email или водительским удостоверением уже существует"}
    except Exception as e:
        return {"error": f"Ошибка добавления клиента: {str(e)}"}
    finally:
        conn.close()

@app.get("/customers/")
def get_customers():
    """Получить всех клиентов"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, first_name, last_name, email, phone, driver_license, address FROM Customers")
    customers = cursor.fetchall()
    conn.close()
    
    if not customers:
        return {"error": "Список клиентов пуст"}
    
    return [{
        "customer_id": c[0], 
        "first_name": c[1], 
        "last_name": c[2], 
        "email": c[3], 
        "phone": c[4], 
        "driver_license": c[5], 
        "address": c[6]
    } for c in customers]

@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, first_name: str = None, last_name: str = None, email: str = None, 
                   phone: str = None, driver_license: str = None, address: str = None):
    """Обновление информации о клиенте"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    try:
        # Проверяем существование клиента
        cursor.execute("SELECT * FROM Customers WHERE customer_id = ?", (customer_id,))
        customer = cursor.fetchone()
        
        if not customer:
            return {"error": "Клиент не найден"}
        
        # Собираем поля для обновления
        update_fields = []
        update_values = []
        
        if first_name is not None:
            update_fields.append("first_name = ?")
            update_values.append(first_name)
        if last_name is not None:
            update_fields.append("last_name = ?")
            update_values.append(last_name)
        if email is not None:
            update_fields.append("email = ?")
            update_values.append(email)
        if phone is not None:
            update_fields.append("phone = ?")
            update_values.append(phone)
        if driver_license is not None:
            update_fields.append("driver_license = ?")
            update_values.append(driver_license)
        if address is not None:
            update_fields.append("address = ?")
            update_values.append(address)
        
        if not update_fields:
            return {"error": "Нет данных для обновления"}
        
        update_values.append(customer_id)
        query = f"UPDATE Customers SET {', '.join(update_fields)} WHERE customer_id = ?"
        
        cursor.execute(query, update_values)
        conn.commit()
        
        return {"message": "Информация о клиенте обновлена"}
    except Exception as e:
        return {"error": f"Ошибка обновления клиента: {str(e)}"}
    finally:
        conn.close()

# Аренда
@app.post("/rentals/")
def create_rental(car_id: int, customer_id: int, rental_date: str, planned_return_date: str, mileage_start: int):
    """Создание записи об аренде"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    try:
        # Проверяем существование автомобиля и клиента
        cursor.execute("SELECT is_available FROM Cars WHERE car_id = ?", (car_id,))
        car = cursor.fetchone()
        
        cursor.execute("SELECT 1 FROM Customers WHERE customer_id = ?", (customer_id,))
        customer = cursor.fetchone()
        
        if not car:
            return {"error": "Автомобиль не найден"}
        if not customer:
            return {"error": "Клиент не найден"}
        if not car[0]:  # is_available
            return {"error": "Автомобиль уже арендован"}
        
        cursor.execute(
            "INSERT INTO Rentals (car_id, customer_id, rental_date, planned_return_date, mileage_start) VALUES (?, ?, ?, ?, ?)",
            (car_id, customer_id, rental_date, planned_return_date, mileage_start)
        )
        
        # Обновляем статус автомобиля
        cursor.execute("UPDATE Cars SET is_available = 0 WHERE car_id = ?", (car_id,))
        
        conn.commit()
        rental_id = cursor.lastrowid
        return {"rental_id": rental_id, "message": "Аренда создана"}
    except Exception as e:
        return {"error": f"Ошибка создания аренды: {str(e)}"}
    finally:
        conn.close()

@app.post("/rentals/{rental_id}/return")
def return_rental(rental_id: int, return_date: str, mileage_end: int):
    """Возврат арендованного автомобиля"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    try:
        # Получаем информацию об аренде
        cursor.execute("SELECT car_id, rental_date, planned_return_date, mileage_start FROM Rentals WHERE rental_id = ? AND status = 'active'", (rental_id,))
        rental = cursor.fetchone()
        
        if not rental:
            return {"error": "Активная аренда не найдена"}
        
        car_id, rental_date, planned_return_date, mileage_start = rental
        
        # Рассчитываем стоимость аренды
        from datetime import datetime
        rental_dt = datetime.strptime(rental_date, "%Y-%m-%d")
        return_dt = datetime.strptime(return_date, "%Y-%m-%d")
        planned_dt = datetime.strptime(planned_return_date, "%Y-%m-%d")
        
        days_rented = (return_dt - rental_dt).days
        if days_rented < 1:
            days_rented = 1
        
        # Получаем дневную ставку автомобиля
        cursor.execute("SELECT daily_rate FROM Cars WHERE car_id = ?", (car_id,))
        daily_rate = cursor.fetchone()[0]
        
        total_cost = days_rented * daily_rate
        
        # Добавляем штраф за просрочку, если есть
        if return_dt > planned_dt:
            overdue_days = (return_dt - planned_dt).days
            penalty = overdue_days * daily_rate * 0.5  # 50% от дневной ставки за каждый день просрочки
            total_cost += penalty
        
        # Обновляем запись аренды
        cursor.execute(
            "UPDATE Rentals SET return_date = ?, mileage_end = ?, total_cost = ?, status = 'completed' WHERE rental_id = ?",
            (return_date, mileage_end, total_cost, rental_id)
        )
        
        # Обновляем пробег и статус автомобиля
        cursor.execute("UPDATE Cars SET mileage = ?, is_available = 1 WHERE car_id = ?", (mileage_end, car_id))
        
        conn.commit()
        
        return {
            "message": "Автомобиль возвращен", 
            "days_rented": days_rented,
            "total_cost": total_cost,
            "mileage_driven": mileage_end - mileage_start
        }
    except Exception as e:
        return {"error": f"Ошибка возврата автомобиля: {str(e)}"}
    finally:
        conn.close()

@app.get("/rentals/")
def get_rentals(status: str = None):
    """Получить все записи об аренде"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    
    if status:
        cursor.execute('''
            SELECT r.rental_id, c.brand, c.model, c.license_plate, 
                   cust.first_name, cust.last_name, r.rental_date, r.return_date, 
                   r.planned_return_date, r.total_cost, r.status
            FROM Rentals r
            JOIN Cars c ON r.car_id = c.car_id
            JOIN Customers cust ON r.customer_id = cust.customer_id
            WHERE r.status = ?
            ORDER BY r.rental_date DESC
        ''', (status,))
    else:
        cursor.execute('''
            SELECT r.rental_id, c.brand, c.model, c.license_plate, 
                   cust.first_name, cust.last_name, r.rental_date, r.return_date, 
                   r.planned_return_date, r.total_cost, r.status
            FROM Rentals r
            JOIN Cars c ON r.car_id = c.car_id
            JOIN Customers cust ON r.customer_id = cust.customer_id
            ORDER BY r.rental_date DESC
        ''')
    
    rentals = cursor.fetchall()
    conn.close()
    
    if not rentals:
        return {"error": "Список аренд пуст"}
    
    return [{
        "rental_id": r[0],
        "car_brand": r[1],
        "car_model": r[2],
        "license_plate": r[3],
        "customer_name": f"{r[4]} {r[5]}",
        "rental_date": r[6],
        "return_date": r[7],
        "planned_return_date": r[8],
        "total_cost": r[9],
        "status": r[10]
    } for r in rentals]

# Техническое обслуживание
@app.post("/maintenance/")
def create_maintenance(car_id: int, maintenance_date: str, maintenance_type: str, cost: float, mileage: int, description: str = ""):
    """Добавление записи о техническом обслуживании"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    try:
        # Проверяем существование автомобиля
        cursor.execute("SELECT 1 FROM Cars WHERE car_id = ?", (car_id,))
        car = cursor.fetchone()
        
        if not car:
            return {"error": "Автомобиль не найден"}
        
        cursor.execute(
            "INSERT INTO Maintenance (car_id, maintenance_date, maintenance_type, description, cost, mileage) VALUES (?, ?, ?, ?, ?, ?)",
            (car_id, maintenance_date, maintenance_type, description, cost, mileage)
        )
        conn.commit()
        maintenance_id = cursor.lastrowid
        return {"maintenance_id": maintenance_id, "message": "Запись о ТО добавлена"}
    except Exception as e:
        return {"error": f"Ошибка добавления записи о ТО: {str(e)}"}
    finally:
        conn.close()

@app.get("/maintenance/{car_id}")
def get_car_maintenance(car_id: int):
    """Получить историю ТО для автомобиля"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.maintenance_id, m.maintenance_date, m.maintenance_type, m.description, m.cost, m.mileage
        FROM Maintenance m
        JOIN Cars c ON m.car_id = c.car_id
        WHERE m.car_id = ?
        ORDER BY m.maintenance_date DESC
    ''', (car_id,))
    maintenance_records = cursor.fetchall()
    conn.close()
    
    if not maintenance_records:
        return {"error": "Записи о ТО не найдены"}
    
    return [{
        "maintenance_id": m[0],
        "maintenance_date": m[1],
        "maintenance_type": m[2],
        "description": m[3],
        "cost": m[4],
        "mileage": m[5]
    } for m in maintenance_records]

# Статистика
@app.get("/stats/rentals")
def get_rental_stats():
    """Получить статистику по арендам"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    
    # Общее количество аренд
    cursor.execute("SELECT COUNT(*) FROM Rentals")
    total_rentals = cursor.fetchone()[0]
    
    # Активные аренды
    cursor.execute("SELECT COUNT(*) FROM Rentals WHERE status = 'active'")
    active_rentals = cursor.fetchone()[0]
    
    # Общий доход
    cursor.execute("SELECT SUM(total_cost) FROM Rentals WHERE status = 'completed' AND total_cost IS NOT NULL")
    total_revenue = cursor.fetchone()[0] or 0
    
    # Средняя продолжительность аренды
    cursor.execute('''
        SELECT AVG(julianday(return_date) - julianday(rental_date)) 
        FROM Rentals 
        WHERE status = 'completed' AND return_date IS NOT NULL
    ''')
    avg_rental_days = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        "total_rentals": total_rentals,
        "active_rentals": active_rentals,
        "total_revenue": round(total_revenue, 2),
        "avg_rental_days": round(avg_rental_days, 1)
    }

@app.get("/stats/cars")
def get_car_stats():
    """Получить статистику по автомобилям"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    
    # Общее количество автомобилей
    cursor.execute("SELECT COUNT(*) FROM Cars")
    total_cars = cursor.fetchone()[0]
    
    # Доступные автомобили
    cursor.execute("SELECT COUNT(*) FROM Cars WHERE is_available = 1")
    available_cars = cursor.fetchone()[0]
    
    # Автомобили по маркам
    cursor.execute("SELECT brand, COUNT(*) FROM Cars GROUP BY brand")
    cars_by_brand = cursor.fetchall()
    
    # Самый популярный автомобиль
    cursor.execute('''
        SELECT c.brand, c.model, COUNT(r.rental_id) as rental_count
        FROM Cars c
        LEFT JOIN Rentals r ON c.car_id = r.car_id
        GROUP BY c.car_id
        ORDER BY rental_count DESC
        LIMIT 1
    ''')
    popular_car = cursor.fetchone()
    
    conn.close()
    
    result = {
        "total_cars": total_cars,
        "available_cars": available_cars,
        "cars_by_brand": [{"brand": c[0], "count": c[1]} for c in cars_by_brand]
    }
    
    if popular_car and popular_car[2] > 0:
        result["most_popular_car"] = {
            "brand": popular_car[0],
            "model": popular_car[1],
            "rental_count": popular_car[2]
        }
    
    return result

# Удаление автомобиля
@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    """Удаление автомобиля"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    try:
        # Проверяем, нет ли активных аренд
        cursor.execute("SELECT 1 FROM Rentals WHERE car_id = ? AND status = 'active'", (car_id,))
        active_rental = cursor.fetchone()
        
        if active_rental:
            return {"error": "Нельзя удалить автомобиль с активной арендой"}
        
        # Удаляем связанные записи
        cursor.execute("DELETE FROM Maintenance WHERE car_id = ?", (car_id,))
        cursor.execute("DELETE FROM Rentals WHERE car_id = ?", (car_id,))
        cursor.execute("DELETE FROM Cars WHERE car_id = ?", (car_id,))
        
        conn.commit()
        return {"message": "Автомобиль удален"}
    except Exception as e:
        return {"error": f"Ошибка удаления автомобиля: {str(e)}"}
    finally:
        conn.close()

# Удаление клиента
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    """Удаление клиента"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    try:
        # Проверяем, нет ли активных аренд
        cursor.execute("SELECT 1 FROM Rentals WHERE customer_id = ? AND status = 'active'", (customer_id,))
        active_rental = cursor.fetchone()
        
        if active_rental:
            return {"error": "Нельзя удалить клиента с активной арендой"}
        
        # Удаляем связанные записи об арендах
        cursor.execute("DELETE FROM Rentals WHERE customer_id = ?", (customer_id,))
        cursor.execute("DELETE FROM Customers WHERE customer_id = ?", (customer_id,))
        
        conn.commit()
        return {"message": "Клиент удален"}
    except Exception as e:
        return {"error": f"Ошибка удаления клиента: {str(e)}"}
    finally:
        conn.close()

# Удаление записи об аренде
@app.delete("/rentals/{rental_id}")
def delete_rental(rental_id: int):
    """Удаление записи об аренде"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Rentals WHERE rental_id = ?", (rental_id,))
        conn.commit()
        return {"message": "Запись об аренде удалена"}
    except Exception as e:
        return {"error": f"Ошибка удаления записи об аренде: {str(e)}"}
    finally:
        conn.close()

# Удаление записи о ТО
@app.delete("/maintenance/{maintenance_id}")
def delete_maintenance(maintenance_id: int):
    """Удаление записи о техническом обслуживании"""
    conn = sqlite3.connect("car_rental.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Maintenance WHERE maintenance_id = ?", (maintenance_id,))
        conn.commit()
        return {"message": "Запись о ТО удалена"}
    except Exception as e:
        return {"error": f"Ошибка удаления записи о ТО: {str(e)}"}
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)