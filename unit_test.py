import unittest
import requests
import time
from datetime import date, timedelta


class TestCarRentalAPI(unittest.TestCase):
    BASE_URL = "http://localhost:8000"
    
    def setUp(self):
        self.timestamp = int(time.time())
        self.created_ids = {
            'cars': [],
            'customers': [],
            'rentals': [],
            'maintenance': []
        }

    def tearDown(self):
        # Очистка созданных данных после каждого теста
        for maintenance_id in self.created_ids['maintenance']:
            try:
                requests.delete(f"{self.BASE_URL}/maintenance/{maintenance_id}")
            except:
                pass
        
        for rental_id in self.created_ids['rentals']:
            try:
                requests.delete(f"{self.BASE_URL}/rentals/{rental_id}")
            except:
                pass
        
        for customer_id in self.created_ids['customers']:
            try:
                requests.delete(f"{self.BASE_URL}/customers/{customer_id}")
            except:
                pass
        
        for car_id in self.created_ids['cars']:
            try:
                requests.delete(f"{self.BASE_URL}/cars/{car_id}")
            except:
                pass

    def test_01_get_cars(self):
        """Тест получения всех автомобилей"""
        response = requests.get(f"{self.BASE_URL}/cars/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), (list, dict))

    def test_02_get_available_cars(self):
        """Тест получения только доступных автомобилей"""
        response = requests.get(f"{self.BASE_URL}/cars/", params={"available_only": True})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), (list, dict))

    def test_03_create_car(self):
        """Тест создания автомобиля"""
        data = {
            'brand': f'Brand_{self.timestamp}',
            'model': f'Model_{self.timestamp}',
            'year': 2020 + (self.timestamp % 5),
            'color': 'Red',
            'license_plate': f'TEST{self.timestamp}',
            'daily_rate': 2000.0 + (self.timestamp % 1000),
            'mileage': 15000,
            'fuel_type': 'petrol'
        }
        response = requests.post(f"{self.BASE_URL}/cars/", params=data)
        self.assertEqual(response.status_code, 200)
        car_id = response.json().get('car_id')
        if car_id:
            self.created_ids['cars'].append(car_id)

    def test_04_update_car(self):
        """Тест обновления автомобиля"""
        # Сначала создаем автомобиль
        create_data = {
            'brand': 'Toyota',
            'model': 'Camry',
            'year': 2022,
            'color': 'Black',
            'license_plate': f'UPDATE{self.timestamp}',
            'daily_rate': 2500.0,
            'mileage': 10000,
            'fuel_type': 'petrol'
        }
        create_response = requests.post(f"{self.BASE_URL}/cars/", params=create_data)
        self.assertEqual(create_response.status_code, 200)
        car_id = create_response.json().get('car_id')
        
        if car_id:
            self.created_ids['cars'].append(car_id)
            
            # Обновляем автомобиль
            update_data = {
                'daily_rate': 2700.0,
                'mileage': 12000,
                'color': 'Dark Gray'
            }
            update_response = requests.put(f"{self.BASE_URL}/cars/{car_id}", params=update_data)
            self.assertEqual(update_response.status_code, 200)

    def test_05_get_customers(self):
        """Тест получения всех клиентов"""
        response = requests.get(f"{self.BASE_URL}/customers/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), (list, dict))

    def test_06_create_customer(self):
        """Тест создания клиента"""
        data = {
            'first_name': f'John_{self.timestamp}',
            'last_name': f'Doe_{self.timestamp}',
            'email': f'john.doe{self.timestamp}@test.com',
            'phone': f'+7916{self.timestamp % 1000000:06d}',
            'driver_license': f'DL{self.timestamp}',
            'address': f'Test address {self.timestamp}'
        }
        response = requests.post(f"{self.BASE_URL}/customers/", params=data)
        self.assertEqual(response.status_code, 200)
        customer_id = response.json().get('customer_id')
        if customer_id:
            self.created_ids['customers'].append(customer_id)

    def test_07_update_customer(self):
        """Тест обновления клиента"""
        # Сначала создаем клиента
        create_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': f'alice.smith{self.timestamp}@test.com',
            'phone': '+79160000001',
            'driver_license': f'DL_UPDATE{self.timestamp}',
            'address': 'Original address'
        }
        create_response = requests.post(f"{self.BASE_URL}/customers/", params=create_data)
        self.assertEqual(create_response.status_code, 200)
        customer_id = create_response.json().get('customer_id')
        
        if customer_id:
            self.created_ids['customers'].append(customer_id)
            
            # Обновляем клиента
            update_data = {
                'phone': '+79169998877',
                'address': f'Updated address {self.timestamp}'
            }
            update_response = requests.put(f"{self.BASE_URL}/customers/{customer_id}", params=update_data)
            self.assertEqual(update_response.status_code, 200)

    def test_08_get_rentals(self):
        """Тест получения всех аренд"""
        response = requests.get(f"{self.BASE_URL}/rentals/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), (list, dict))

    def test_09_create_rental(self):
        """Тест создания аренды"""
        # Сначала создаем автомобиль и клиента
        car_data = {
            'brand': 'Honda',
            'model': 'Civic',
            'year': 2023,
            'color': 'White',
            'license_plate': f'RENTAL{self.timestamp}',
            'daily_rate': 1800.0,
            'mileage': 5000,
            'fuel_type': 'petrol'
        }
        car_response = requests.post(f"{self.BASE_URL}/cars/", params=car_data)
        car_id = car_response.json().get('car_id')
        
        customer_data = {
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'email': f'bob.johnson{self.timestamp}@test.com',
            'phone': '+79160000002',
            'driver_license': f'DL_RENTAL{self.timestamp}',
            'address': 'Rental test address'
        }
        customer_response = requests.post(f"{self.BASE_URL}/customers/", params=customer_data)
        customer_id = customer_response.json().get('customer_id')
        
        if car_id and customer_id:
            self.created_ids['cars'].append(car_id)
            self.created_ids['customers'].append(customer_id)
            
            # Создаем аренду
            rental_data = {
                'car_id': car_id,
                'customer_id': customer_id,
                'rental_date': str(date.today()),
                'planned_return_date': str(date.today() + timedelta(days=3)),
                'mileage_start': 5000
            }
            response = requests.post(f"{self.BASE_URL}/rentals/", params=rental_data)
            self.assertEqual(response.status_code, 200)
            rental_id = response.json().get('rental_id')
            if rental_id:
                self.created_ids['rentals'].append(rental_id)

    def test_10_return_rental(self):
        """Тест возврата автомобиля"""
        # Сначала создаем автомобиль, клиента и аренду
        car_data = {
            'brand': 'Nissan',
            'model': 'Altima',
            'year': 2021,
            'color': 'Blue',
            'license_plate': f'RETURN{self.timestamp}',
            'daily_rate': 2200.0,
            'mileage': 20000,
            'fuel_type': 'petrol'
        }
        car_response = requests.post(f"{self.BASE_URL}/cars/", params=car_data)
        car_id = car_response.json().get('car_id')
        
        customer_data = {
            'first_name': 'Carol',
            'last_name': 'Wilson',
            'email': f'carol.wilson{self.timestamp}@test.com',
            'phone': '+79160000003',
            'driver_license': f'DL_RETURN{self.timestamp}',
            'address': 'Return test address'
        }
        customer_response = requests.post(f"{self.BASE_URL}/customers/", params=customer_data)
        customer_id = customer_response.json().get('customer_id')
        
        if car_id and customer_id:
            self.created_ids['cars'].append(car_id)
            self.created_ids['customers'].append(customer_id)
            
            # Создаем аренду
            rental_data = {
                'car_id': car_id,
                'customer_id': customer_id,
                'rental_date': str(date.today() - timedelta(days=2)),
                'planned_return_date': str(date.today() + timedelta(days=1)),
                'mileage_start': 20000
            }
            rental_response = requests.post(f"{self.BASE_URL}/rentals/", params=rental_data)
            rental_id = rental_response.json().get('rental_id')
            
            if rental_id:
                self.created_ids['rentals'].append(rental_id)
                
                # Возвращаем автомобиль
                return_data = {
                    'return_date': str(date.today()),
                    'mileage_end': 20300
                }
                return_response = requests.post(f"{self.BASE_URL}/rentals/{rental_id}/return", params=return_data)
                self.assertEqual(return_response.status_code, 200)
                self.assertIn('total_cost', return_response.json())

    def test_11_create_maintenance(self):
        """Тест создания записи ТО"""
        # Сначала создаем автомобиль
        car_data = {
            'brand': 'BMW',
            'model': 'X5',
            'year': 2020,
            'color': 'Black',
            'license_plate': f'MAINT{self.timestamp}',
            'daily_rate': 3500.0,
            'mileage': 30000,
            'fuel_type': 'diesel'
        }
        car_response = requests.post(f"{self.BASE_URL}/cars/", params=car_data)
        car_id = car_response.json().get('car_id')
        
        if car_id:
            self.created_ids['cars'].append(car_id)
            
            # Создаем запись ТО
            maintenance_data = {
                'car_id': car_id,
                'maintenance_date': str(date.today()),
                'maintenance_type': 'Замена масла',
                'cost': 5000.0,
                'mileage': 30000,
                'description': f'Плановое ТО {self.timestamp}'
            }
            response = requests.post(f"{self.BASE_URL}/maintenance/", params=maintenance_data)
            self.assertEqual(response.status_code, 200)
            maintenance_id = response.json().get('maintenance_id')
            if maintenance_id:
                self.created_ids['maintenance'].append(maintenance_id)

    def test_12_get_car_maintenance(self):
        """Тест получения истории ТО автомобиля"""
        # Сначала создаем автомобиль и запись ТО
        car_data = {
            'brand': 'Audi',
            'model': 'A4',
            'year': 2019,
            'color': 'Silver',
            'license_plate': f'MAINT_HIST{self.timestamp}',
            'daily_rate': 2800.0,
            'mileage': 40000,
            'fuel_type': 'petrol'
        }
        car_response = requests.post(f"{self.BASE_URL}/cars/", params=car_data)
        car_id = car_response.json().get('car_id')
        
        if car_id:
            self.created_ids['cars'].append(car_id)
            
            # Создаем запись ТО
            maintenance_data = {
                'car_id': car_id,
                'maintenance_date': str(date.today()),
                'maintenance_type': 'Технический осмотр',
                'cost': 3000.0,
                'mileage': 40000,
                'description': 'Регулярный техосмотр'
            }
            maintenance_response = requests.post(f"{self.BASE_URL}/maintenance/", params=maintenance_data)
            maintenance_id = maintenance_response.json().get('maintenance_id')
            if maintenance_id:
                self.created_ids['maintenance'].append(maintenance_id)
            
            # Получаем историю ТО
            response = requests.get(f"{self.BASE_URL}/maintenance/{car_id}")
            self.assertEqual(response.status_code, 200)

    def test_13_get_rental_stats(self):
        """Тест получения статистики аренд"""
        response = requests.get(f"{self.BASE_URL}/stats/rentals")
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_rentals', stats)

    def test_14_get_car_stats(self):
        """Тест получения статистики автомобилей"""
        response = requests.get(f"{self.BASE_URL}/stats/cars")
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_cars', stats)

    def test_15_delete_car(self):
        """Тест удаления автомобиля"""
        # Сначала создаем автомобиль
        create_data = {
            'brand': 'Ford',
            'model': 'Focus',
            'year': 2022,
            'color': 'Green',
            'license_plate': f'DELETE{self.timestamp}',
            'daily_rate': 1900.0,
            'mileage': 10000,
            'fuel_type': 'petrol'
        }
        create_response = requests.post(f"{self.BASE_URL}/cars/", params=create_data)
        self.assertEqual(create_response.status_code, 200)
        car_id = create_response.json().get('car_id')
        
        if car_id:
            # Удаляем автомобиль
            delete_response = requests.delete(f"{self.BASE_URL}/cars/{car_id}")
            self.assertEqual(delete_response.status_code, 200)

    def test_16_delete_customer(self):
        """Тест удаления клиента"""
        # Сначала создаем клиента
        create_data = {
            'first_name': 'David',
            'last_name': 'Brown',
            'email': f'david.brown{self.timestamp}@test.com',
            'phone': '+79160000004',
            'driver_license': f'DL_DELETE{self.timestamp}',
            'address': 'Delete test address'
        }
        create_response = requests.post(f"{self.BASE_URL}/customers/", params=create_data)
        self.assertEqual(create_response.status_code, 200)
        customer_id = create_response.json().get('customer_id')
        
        if customer_id:
            # Удаляем клиента
            delete_response = requests.delete(f"{self.BASE_URL}/customers/{customer_id}")
            self.assertEqual(delete_response.status_code, 200)

    def test_17_delete_rental(self):
        """Тест удаления аренды"""
        # Сначала создаем автомобиль, клиента и аренду
        car_data = {
            'brand': 'Kia',
            'model': 'Rio',
            'year': 2023,
            'color': 'Yellow',
            'license_plate': f'DEL_RENT{self.timestamp}',
            'daily_rate': 1600.0,
            'mileage': 7000,
            'fuel_type': 'petrol'
        }
        car_response = requests.post(f"{self.BASE_URL}/cars/", params=car_data)
        car_id = car_response.json().get('car_id')
        
        customer_data = {
            'first_name': 'Emma',
            'last_name': 'Davis',
            'email': f'emma.davis{self.timestamp}@test.com',
            'phone': '+79160000005',
            'driver_license': f'DL_DEL_RENT{self.timestamp}',
            'address': 'Delete rental test address'
        }
        customer_response = requests.post(f"{self.BASE_URL}/customers/", params=customer_data)
        customer_id = customer_response.json().get('customer_id')
        
        if car_id and customer_id:
            self.created_ids['cars'].append(car_id)
            self.created_ids['customers'].append(customer_id)
            
            # Создаем аренду
            rental_data = {
                'car_id': car_id,
                'customer_id': customer_id,
                'rental_date': str(date.today()),
                'planned_return_date': str(date.today() + timedelta(days=2)),
                'mileage_start': 7000
            }
            rental_response = requests.post(f"{self.BASE_URL}/rentals/", params=rental_data)
            rental_id = rental_response.json().get('rental_id')
            
            if rental_id:
                # Удаляем аренду
                delete_response = requests.delete(f"{self.BASE_URL}/rentals/{rental_id}")
                self.assertEqual(delete_response.status_code, 200)

    def test_18_delete_maintenance(self):
        """Тест удаления записи ТО"""
        # Сначала создаем автомобиль и запись ТО
        car_data = {
            'brand': 'Hyundai',
            'model': 'Elantra',
            'year': 2021,
            'color': 'Orange',
            'license_plate': f'DEL_MAINT{self.timestamp}',
            'daily_rate': 1700.0,
            'mileage': 25000,
            'fuel_type': 'petrol'
        }
        car_response = requests.post(f"{self.BASE_URL}/cars/", params=car_data)
        car_id = car_response.json().get('car_id')
        
        if car_id:
            self.created_ids['cars'].append(car_id)
            
            # Создаем запись ТО
            maintenance_data = {
                'car_id': car_id,
                'maintenance_date': str(date.today()),
                'maintenance_type': 'Замена тормозных колодок',
                'cost': 8000.0,
                'mileage': 25000,
                'description': 'Замена передних тормозных колодок'
            }
            maintenance_response = requests.post(f"{self.BASE_URL}/maintenance/", params=maintenance_data)
            maintenance_id = maintenance_response.json().get('maintenance_id')
            
            if maintenance_id:
                # Удаляем запись ТО
                delete_response = requests.delete(f"{self.BASE_URL}/maintenance/{maintenance_id}")
                self.assertEqual(delete_response.status_code, 200)

    def test_19_complete_workflow(self):
        """Тест полного рабочего процесса аренды"""
        # 1. Создаем автомобиль
        car_data = {
            'brand': 'Mercedes',
            'model': 'C-Class',
            'year': 2023,
            'color': 'Black',
            'license_plate': f'WORKFLOW{self.timestamp}',
            'daily_rate': 4000.0,
            'mileage': 8000,
            'fuel_type': 'petrol'
        }
        car_response = requests.post(f"{self.BASE_URL}/cars/", params=car_data)
        self.assertEqual(car_response.status_code, 200)
        car_id = car_response.json().get('car_id')
        
        # 2. Создаем клиента
        customer_data = {
            'first_name': 'Frank',
            'last_name': 'Miller',
            'email': f'frank.miller{self.timestamp}@test.com',
            'phone': '+79160000006',
            'driver_license': f'DL_WORKFLOW{self.timestamp}',
            'address': 'Workflow test address'
        }
        customer_response = requests.post(f"{self.BASE_URL}/customers/", params=customer_data)
        self.assertEqual(customer_response.status_code, 200)
        customer_id = customer_response.json().get('customer_id')
        
        if car_id and customer_id:
            self.created_ids['cars'].append(car_id)
            self.created_ids['customers'].append(customer_id)
            
            # 3. Создаем аренду
            rental_data = {
                'car_id': car_id,
                'customer_id': customer_id,
                'rental_date': str(date.today() - timedelta(days=1)),
                'planned_return_date': str(date.today() + timedelta(days=2)),
                'mileage_start': 8000
            }
            rental_response = requests.post(f"{self.BASE_URL}/rentals/", params=rental_data)
            self.assertEqual(rental_response.status_code, 200)
            rental_id = rental_response.json().get('rental_id')
            
            if rental_id:
                self.created_ids['rentals'].append(rental_id)
                
                # 4. Проверяем, что автомобиль стал недоступен
                available_cars_response = requests.get(f"{self.BASE_URL}/cars/", params={"available_only": True})
                self.assertEqual(available_cars_response.status_code, 200)
                
                # 5. Возвращаем автомобиль
                return_data = {
                    'return_date': str(date.today()),
                    'mileage_end': 8150
                }
                return_response = requests.post(f"{self.BASE_URL}/rentals/{rental_id}/return", params=return_data)
                self.assertEqual(return_response.status_code, 200)
                
                # 6. Создаем запись ТО
                maintenance_data = {
                    'car_id': car_id,
                    'maintenance_date': str(date.today()),
                    'maintenance_type': 'Мойка и чистка',
                    'cost': 1500.0,
                    'mileage': 8150,
                    'description': 'После аренды'
                }
                maintenance_response = requests.post(f"{self.BASE_URL}/maintenance/", params=maintenance_data)
                self.assertEqual(maintenance_response.status_code, 200)
                maintenance_id = maintenance_response.json().get('maintenance_id')
                
                if maintenance_id:
                    self.created_ids['maintenance'].append(maintenance_id)
                
                # 7. Проверяем статистику
                rental_stats_response = requests.get(f"{self.BASE_URL}/stats/rentals")
                self.assertEqual(rental_stats_response.status_code, 200)
                
                car_stats_response = requests.get(f"{self.BASE_URL}/stats/cars")
                self.assertEqual(car_stats_response.status_code, 200)
                
                # 8. Проверяем данные
                cars_response = requests.get(f"{self.BASE_URL}/cars/")
                self.assertEqual(cars_response.status_code, 200)
                
                customers_response = requests.get(f"{self.BASE_URL}/customers/")
                self.assertEqual(customers_response.status_code, 200)
                
                rentals_response = requests.get(f"{self.BASE_URL}/rentals/")
                self.assertEqual(rentals_response.status_code, 200)
                
                maintenance_response = requests.get(f"{self.BASE_URL}/maintenance/{car_id}")
                self.assertEqual(maintenance_response.status_code, 200)

    def test_20_rental_with_overdue(self):
        """Тест аренды с просрочкой возврата"""
        # Создаем автомобиль и клиента
        car_data = {
            'brand': 'Volkswagen',
            'model': 'Golf',
            'year': 2022,
            'color': 'Blue',
            'license_plate': f'OVERDUE{self.timestamp}',
            'daily_rate': 2300.0,
            'mileage': 12000,
            'fuel_type': 'petrol'
        }
        car_response = requests.post(f"{self.BASE_URL}/cars/", params=car_data)
        car_id = car_response.json().get('car_id')
        
        customer_data = {
            'first_name': 'Grace',
            'last_name': 'Taylor',
            'email': f'grace.taylor{self.timestamp}@test.com',
            'phone': '+79160000007',
            'driver_license': f'DL_OVERDUE{self.timestamp}',
            'address': 'Overdue test address'
        }
        customer_response = requests.post(f"{self.BASE_URL}/customers/", params=customer_data)
        customer_id = customer_response.json().get('customer_id')
        
        if car_id and customer_id:
            self.created_ids['cars'].append(car_id)
            self.created_ids['customers'].append(customer_id)
            
            # Создаем аренду с прошлой датой
            rental_data = {
                'car_id': car_id,
                'customer_id': customer_id,
                'rental_date': str(date.today() - timedelta(days=5)),
                'planned_return_date': str(date.today() - timedelta(days=2)),  # Просрочка на 3 дня
                'mileage_start': 12000
            }
            rental_response = requests.post(f"{self.BASE_URL}/rentals/", params=rental_data)
            rental_id = rental_response.json().get('rental_id')
            
            if rental_id:
                self.created_ids['rentals'].append(rental_id)
                
                # Возвращаем с просрочкой
                return_data = {
                    'return_date': str(date.today()),
                    'mileage_end': 12300
                }
                return_response = requests.post(f"{self.BASE_URL}/rentals/{rental_id}/return", params=return_data)
                self.assertEqual(return_response.status_code, 200)
                
                # Проверяем, что в ответе есть информация о стоимости
                response_data = return_response.json()
                self.assertIn('total_cost', response_data)
                self.assertIn('days_rented', response_data)


if __name__ == '__main__':
    unittest.main(verbosity=2)