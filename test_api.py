import requests
from datetime import date, timedelta
import json

BASE_URL = "http://127.0.0.1:8000"


def test_get_all_cars(available_only: bool = False):
    """Получение всех автомобилей"""
    params = {"available_only": available_only}
    response = requests.get(f"{BASE_URL}/cars/", params=params)
    print("GET Cars Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    return response

def test_create_car(car_data):
    """Создание автомобиля"""
    response = requests.post(f"{BASE_URL}/cars/", json=car_data)
    print("POST Car Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    if response.status_code == 200:
        return response.json().get('car_id')
    return None

def test_update_car(car_id, update_data):
    """Обновление автомобиля"""
    response = requests.put(f"{BASE_URL}/cars/{car_id}", json=update_data)
    print("PUT Car Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_delete_car(car_id):
    """Удаление автомобиля"""
    response = requests.delete(f"{BASE_URL}/cars/{car_id}")
    print("DELETE Car Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())


def test_get_all_customers():
    """Получение всех клиентов"""
    response = requests.get(f"{BASE_URL}/customers/")
    print("GET Customers Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_create_customer(customer_data):
    """Создание клиента"""
    response = requests.post(f"{BASE_URL}/customers/", json=customer_data)
    print("POST Customer Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    if response.status_code == 200:
        return response.json().get('customer_id')
    return None

def test_update_customer(customer_id, update_data):
    """Обновление клиента"""
    response = requests.put(f"{BASE_URL}/customers/{customer_id}", json=update_data)
    print("PUT Customer Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_delete_customer(customer_id):
    """Удаление клиента"""
    response = requests.delete(f"{BASE_URL}/customers/{customer_id}")
    print("DELETE Customer Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())


def test_create_rental(rental_data):
    """Создание аренды"""
    response = requests.post(f"{BASE_URL}/rentals/", json=rental_data)
    print("POST Rental Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    if response.status_code == 200:
        return response.json().get('rental_id')
    return None

def test_get_all_rentals(status: str = None):
    """Получение всех аренд"""
    params = {"status": status} if status else {}
    response = requests.get(f"{BASE_URL}/rentals/", params=params)
    print("GET Rentals Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_return_rental(rental_id, return_data):
    """Возврат автомобиля"""
    response = requests.post(f"{BASE_URL}/rentals/{rental_id}/return", json=return_data)
    print("POST Return Rental Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_delete_rental(rental_id):
    """Удаление аренды"""
    response = requests.delete(f"{BASE_URL}/rentals/{rental_id}")
    print("DELETE Rental Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())


def test_create_maintenance(maintenance_data):
    """Создание записи ТО"""
    response = requests.post(f"{BASE_URL}/maintenance/", json=maintenance_data)
    print("POST Maintenance Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    if response.status_code == 200:
        return response.json().get('maintenance_id')
    return None

def test_get_car_maintenance(car_id):
    """Получение ТО для автомобиля"""
    response = requests.get(f"{BASE_URL}/maintenance/{car_id}")
    print("GET Car Maintenance Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_delete_maintenance(maintenance_id):
    """Удаление записи ТО"""
    response = requests.delete(f"{BASE_URL}/maintenance/{maintenance_id}")
    print("DELETE Maintenance Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())


def test_get_rental_stats():
    """Получение статистики аренд"""
    response = requests.get(f"{BASE_URL}/stats/rentals")
    print("GET Rental Stats Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_get_car_stats():
    """Получение статистики автомобилей"""
    response = requests.get(f"{BASE_URL}/stats/cars")
    print("GET Car Stats Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())


def main():
    
    print("1. ТЕСТЫ АВТОМОБИЛЕЙ")
    print("-" * 50)
    
    # Получение всех автомобилей
    test_get_all_cars()
    
    # Создание тестовых автомобилей
    test_car1 = {
        "brand": "Toyota",
        "model": "Camry",
        "year": 2022,
        "color": "Black",
        "license_plate": "A123BC",
        "daily_rate": 2500.0,
        "mileage": 15000,
        "fuel_type": "petrol"
    }
    car1_id = test_create_car(test_car1)
    
    test_car2 = {
        "brand": "Honda",
        "model": "Civic",
        "year": 2023,
        "color": "White",
        "license_plate": "B456DE",
        "daily_rate": 2000.0,
        "mileage": 8000,
        "fuel_type": "petrol"
    }
    car2_id = test_create_car(test_car2)
    
    # Получение всех автомобилей после создания
    test_get_all_cars()
    
    # Получение только доступных автомобилей
    test_get_all_cars(available_only=True)
    
    if car1_id:
        # Обновление автомобиля
        car_update = {
            "daily_rate": 2700.0,
            "mileage": 15500,
            "color": "Dark Gray"
        }
        test_update_car(car1_id, car_update)
    
    print("\n2. ТЕСТЫ КЛИЕНТОВ")
    print("-" * 50)
    
    # Получение всех клиентов
    test_get_all_customers()
    
    # Создание тестовых клиентов
    test_customer1 = {
        "first_name": "Иван",
        "last_name": "Петров",
        "email": "ivan.petrov@mail.com",
        "phone": "+79161234567",
        "driver_license": "1234567890",
        "address": "Москва, ул. Ленина, д. 1"
    }
    customer1_id = test_create_customer(test_customer1)
    
    test_customer2 = {
        "first_name": "Мария",
        "last_name": "Сидорова",
        "email": "maria.sidorova@mail.com",
        "phone": "+79167654321",
        "driver_license": "0987654321",
        "address": "Санкт-Петербург, Невский пр., д. 10"
    }
    customer2_id = test_create_customer(test_customer2)
    
    # Получение всех клиентов после создания
    test_get_all_customers()
    
    if customer1_id:
        # Обновление клиента
        customer_update = {
            "phone": "+79169998877",
            "address": "Москва, ул. Пушкина, д. 15"
        }
        test_update_customer(customer1_id, customer_update)
    
    print("\n3. ТЕСТЫ АРЕНДЫ")
    print("-" * 50)
    
    # Получение всех аренд
    test_get_all_rentals()
    
    rental_id = None
    if car1_id and customer1_id:
        # Создание аренды
        test_rental = {
            "car_id": car1_id,
            "customer_id": customer1_id,
            "rental_date": str(date.today()),
            "planned_return_date": str(date.today() + timedelta(days=3)),
            "mileage_start": 15500
        }
        rental_id = test_create_rental(test_rental)
        
        # Проверка, что автомобиль стал недоступен
        test_get_all_cars(available_only=True)
        
        # Получение всех активных аренд
        test_get_all_rentals(status="active")
    
    print("\n4. ТЕСТЫ ВОЗВРАТА АВТОМОБИЛЯ")
    print("-" * 50)
    
    if rental_id:
        # Возврат автомобиля
        return_data = {
            "return_date": str(date.today() + timedelta(days=2)),
            "mileage_end": 15800
        }
        test_return_rental(rental_id, return_data)
        
        # Проверка, что автомобиль снова доступен
        test_get_all_cars(available_only=True)
        
        # Получение всех завершенных аренд
        test_get_all_rentals(status="completed")
    
    print("\n5. ТЕСТЫ ТЕХНИЧЕСКОГО ОБСЛУЖИВАНИЯ")
    print("-" * 50)
    
    maintenance_id = None
    if car2_id:
        # Создание записи ТО
        test_maintenance = {
            "car_id": car2_id,
            "maintenance_date": str(date.today()),
            "maintenance_type": "Замена масла",
            "cost": 5000.0,
            "mileage": 10000,
            "description": "Плановое ТО, замена масла и фильтров"
        }
        maintenance_id = test_create_maintenance(test_maintenance)
        
        # Получение истории ТО для автомобиля
        test_get_car_maintenance(car2_id)
    
    print("\n6. ТЕСТЫ СТАТИСТИКИ")
    print("-" * 50)
    
    # Статистика аренд
    test_get_rental_stats()
    
    # Статистика автомобилей
    test_get_car_stats()
    
    print("\n7. ТЕСТЫ УДАЛЕНИЯ")
    print("-" * 50)
    
    # Удаление в правильном порядке (сначала зависимые сущности)
    if maintenance_id:
        test_delete_maintenance(maintenance_id)
    
    if rental_id:
        test_delete_rental(rental_id)
    
    if customer1_id:
        test_delete_customer(customer1_id)
    
    if customer2_id:
        test_delete_customer(customer2_id)
    
    if car1_id:
        test_delete_car(car1_id)
    
    if car2_id:
        test_delete_car(car2_id)
    
    # Финальная проверка всех данных
    print("\n8. ФИНАЛЬНАЯ ПРОВЕРКА ДАННЫХ")
    print("-" * 50)
    
    test_get_all_cars()
    test_get_all_customers()
    test_get_all_rentals()
    test_get_rental_stats()
    test_get_car_stats()

if __name__ == "__main__":
    main()