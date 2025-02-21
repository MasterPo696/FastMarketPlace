import requests
from requests.auth import HTTPBasicAuth
import uuid
import json
import toml
import os 
from urllib.parse import urlparse
from icrawler.builtin import GoogleImageCrawler

# Load config from secrets/config.toml
config = toml.load('secrets/config.toml')

CLIENT = config['CLIENT_ID']
SECRET = config['CLIENT_SECRET']

class GigaChatAPI:
    def __init__(self):
        self.client = CLIENT
        self.secret = SECRET
        self.url_oath = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"


    def get_access_token(self) -> str:
        payload = {"scope": "GIGACHAT_API_PERS"}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4())
        }
        result = requests.post(
            url=self.url_oath, 
            headers=headers, 
            auth=HTTPBasicAuth(CLIENT, SECRET), 
            data=payload,
            verify=False
        )
        return result.json()["access_token"]
    

    json_path = "static/categories.json"

    def get_categories(self, json_path=json_path) -> dict:
            with open(json_path, 'r') as f:
                data = json.load(f)
            return data['categories']

    def create_items_by_categories(self) -> list:
        categories = self.get_categories()
        access_token = self.get_access_token()
        all_items = []
        
        for category in categories:
            category_name = category['name']
            for subcategory in category['subcategories']:
                prompt = f"""Create 3 items for category '{category_name}', subcategory '{subcategory}'.
                Return ONLY valid JSON array in this format. NO COMMENTS!!!:
                [
                    {{
                        "name": "product name",
                        "description": "detailed product description",
                        "price": float number between 1-1000,
                        "weight": float number between 0.1-10 (in kilograms!),
                        "discount": integer between 0-30,
                        "subcategory": "{subcategory}",
                        "category": "{category_name}"
                    }}
                ]"""

                try:
                    response = self.send_prompt(prompt, access_token)
                    
                    # Пытаемся извлечь JSON из ответа
                    try:
                        # Находим JSON массив в ответе
                        start_idx = response.find('[')
                        end_idx = response.rfind(']') + 1
                        if start_idx != -1 and end_idx != -1:
                            json_str = response[start_idx:end_idx]
                            items = json.loads(json_str)
                            
                            # Валидируем каждый item
                            for item in items:
                                if self.validate_item(item):
                                    all_items.append(item)
                                else:
                                    print(f"Invalid item format: {item}")
                                    
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse JSON for {category_name}/{subcategory}: {str(e)}")
                    except Exception as e:
                        print(f"Error processing items for {category_name}/{subcategory}: {str(e)}")
                    
                except Exception as e:
                    print(f"Error processing {category_name}/{subcategory}: {str(e)}")
                    continue

        # Сохраняем все валидные items в один JSON файл
        if all_items:
            output_file = "static/items_gen.json"
            try:
                # Добавляем изображения к каждому товару
                for item in all_items:
                    search_query = f"{item['name']} product white background"
                    image_path = self.get_picture_from_web(search_query, item['name'])
                    item['image_path'] = image_path
                
                # Сохраняем обновленный JSON
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({"items": all_items}, f, indent=4, ensure_ascii=False)
                print(f"\nAll valid items have been saved to '{output_file}'")
                print(f"Total items generated: {len(all_items)}")
            except Exception as e:
                print(f"Error saving items to JSON: {str(e)}")

            return all_items

    def send_prompt(self, msg: str, access_token: str):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": msg}]
        }

        response = requests.post(
            url=self.url,
            headers=headers,
            json=payload,
            verify=False
        )

        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")

        try:
            return response.json()["choices"][0]["message"]["content"]
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {response.text}") from e
        except KeyError as e:
            raise Exception(f"Unexpected response format: {response.json()}") from e


    def translate_prompt(self, prompt: str) -> str:
        access_token = self.get_access_token()
        prompt = f"Переведи на английский, не давай никаких пояснений: {prompt}"
        response = self.send_prompt(prompt, access_token)
        print(response)
        return response
    

    def validate_item(self, item: dict) -> bool:
        """Validate generated item structure"""
        required_fields = {
            'name': str,
            'description': str,
            'price': (int, float),
            'weight': (int, float),
            'discount': int,
            'subcategory': str,
            'category': str
        }
        
        try:
            # Проверяем наличие всех полей и их типы
            for field, field_type in required_fields.items():
                if field not in item:
                    print(f"Missing field '{field}' in item: {item}")
                    return False
                if not isinstance(item[field], field_type):
                    print(f"Invalid type for '{field}' in item {item['name']}: expected {field_type}, got {type(item[field])}")
                    return False
            
            # Проверяем диапазоны значений
            if not (1 <= float(item['price']) <= 1000):
                print(f"Price out of range for {item['name']}: {item['price']} (should be between 1 and 1000)")
                return False
            if not (0.1 <= float(item['weight']) <= 10):
                print(f"Weight out of range for {item['name']}: {item['weight']} kg (should be between 0.1 and 10)")
                return False
            if not (0 <= int(item['discount']) <= 30):
                print(f"Discount out of range for {item['name']}: {item['discount']} (should be between 0 and 30)")
                return False
            
            return True
        except Exception as e:
            print(f"Validation error for item: {item}")
            print(f"Error: {str(e)}")
            return False


    def get_picture_from_web(self, query: str, item_name: str = None) -> str:
        """
        Get picture using icrawler
        Returns local path to saved image
        Args:
            query: search query for image
            item_name: original item name for file naming
        """
        try:
            # Создаем директорию для изображений если её нет
            output_dir = 'static/product_images'
            os.makedirs(output_dir, exist_ok=True)
            
            # Формируем безопасное имя файла для директории и итогового файла
            safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = "".join(c for c in (item_name or query) if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_').lower()
            
            product_dir = os.path.join(output_dir, safe_query)
            
            # Настраиваем краулер
            google_crawler = GoogleImageCrawler(
                feeder_threads=1,
                parser_threads=1,
                downloader_threads=1,
                storage={'root_dir': product_dir}
            )
            
            # Задаем фильтры для поиска
            filters = {
                'size': 'medium',
                'type': 'photo',
                'color': 'white'
            }
            
            # Скачиваем только 1 изображение
            google_crawler.crawl(
                keyword=query,
                filters=filters,
                max_num=1,
                file_idx_offset=0
            )
            
            # Получаем путь к скачанному файлу
            downloaded_files = os.listdir(product_dir)
            if downloaded_files:
                # Берем первый файл
                image_file = downloaded_files[0]
                # Формируем новое имя файла используя оригинальное название товара
                new_filename = f"{safe_name}{os.path.splitext(image_file)[1]}"
                old_path = os.path.join(product_dir, image_file)
                new_path = os.path.join(output_dir, new_filename)
                
                # Перемещаем файл из временной папки в основную
                os.rename(old_path, new_path)
                # Удаляем временную папку
                os.rmdir(product_dir)
                
                # Возвращаем относительный путь для сохранения в БД
                relative_path = os.path.join('product_images', new_filename)
                print(f"Successfully downloaded image for {item_name or query}")
                return relative_path
                
        except Exception as e:
            print(f"Error getting image for {item_name or query}: {str(e)}")
        
        # Возвращаем путь к дефолтному изображению в случае ошибки
        return 'images/default_product.jpg'

    def download_all_images(self):
        """
        Download images for all items from items_gen.json
        """
        try:
            # Проверяем существование JSON файла
            json_file = "static/items_gen.json"
            if not os.path.exists(json_file):
                print(f"Error: File {json_file} not found")
                return
            
            # Загружаем JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'items' not in data:
                print("Error: No 'items' key in JSON file")
                return
            
            items = data['items']
            total_items = len(items)
            print(f"\nStarting download of {total_items} images...")
            
            # Счетчики для статистики
            success_count = 0
            error_count = 0
            
            # Скачиваем изображения для каждого товара
            for i, item in enumerate(items, 1):
                try:
                    name = item.get('name')
                    if not name:
                        print(f"Warning: Item {i} has no name")
                        continue
                    
                    print(f"\nProcessing item {i}/{total_items}: {name}")
                    search_query = f"{name} product white background"
                    image_path = self.get_picture_from_web(search_query, name)
                    
                    # Обновляем путь к изображению в JSON
                    item['image_path'] = image_path
                    
                    # Проверяем результат
                    if image_path != 'images/default_product.jpg':
                        success_count += 1
                    else:
                        error_count += 1
                    
                except Exception as e:
                    error_count += 1
                    print(f"Error processing item {name}: {str(e)}")
            
            # Сохраняем обновленный JSON
            try:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                print("\nJSON file updated successfully")
            except Exception as e:
                print(f"\nError updating JSON file: {str(e)}")
            
            # Выводим статистику
            print(f"\nDownload complete!")
            print(f"Successfully downloaded: {success_count}")
            print(f"Errors: {error_count}")
            print(f"Total processed: {total_items}")
            
        except Exception as e:
            print(f"Error in download_all_images: {str(e)}")

    def create_initial_items(self) -> list:
        """
        Create initial items for empty database
        Returns list of first 5 items with images
        """
        try:
            # Получаем первые 5 товаров из конфига
            categories = self.get_categories()
            access_token = self.get_access_token()
            initial_items = []
            items_needed = 5
            
            for category in categories:
                if len(initial_items) >= items_needed:
                    break
                    
                category_name = category['name']
                for subcategory in category['subcategories']:
                    if len(initial_items) >= items_needed:
                        break
                        
                    prompt = f"""Create 1 item for category '{category_name}', subcategory '{subcategory}'.
                    Return ONLY valid JSON array in this format. NO COMMENTS!!!:
                    [
                        {{
                            "name": "product name",
                            "description": "detailed product description",
                            "price": float number between 1-1000,
                            "weight": float number between 0.1-10 (in kilograms!),
                            "discount": integer between 0-30,
                            "subcategory": "{subcategory}",
                            "category": "{category_name}"
                        }}
                    ]"""

                    try:
                        response = self.send_prompt(prompt, access_token)
                        
                        # Извлекаем JSON из ответа
                        start_idx = response.find('[')
                        end_idx = response.rfind(']') + 1
                        if start_idx != -1 and end_idx != -1:
                            json_str = response[start_idx:end_idx]
                            items = json.loads(json_str)
                            
                            # Валидируем item и добавляем изображение
                            for item in items:
                                if self.validate_item(item):
                                    # Пробуем скачать изображение
                                    search_query = f"{item['name']} product white background"
                                    image_path = self.get_picture_from_web(search_query, item['name'])
                                    
                                    # Если изображение не удалось скачать, используем дефолтное
                                    if image_path == 'images/default_product.jpg':
                                        image_path = 'images/banana.jpg'
                                    
                                    item['image_path'] = image_path
                                    initial_items.append(item)
                                    
                                    if len(initial_items) >= items_needed:
                                        break
                            
                    except Exception as e:
                        print(f"Error processing {category_name}/{subcategory}: {str(e)}")
                        continue

            return initial_items
            
        except Exception as e:
            print(f"Error in create_initial_items: {str(e)}")
            return []


# Запуск массовой загрузки изображений
# giga = GigaChatAPI()
# giga.download_all_images()
