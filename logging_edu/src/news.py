import datetime
import logging
import requests

from src.config import API_KEY, BASE_URL


logger = logging.getLogger('news')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/news.log',encoding='UTF-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_news(query: str, exclude_words: list, api_key: str = API_KEY) -> list:
    today = datetime.datetime.today()
    params = {
        'q': query,
        'from': today.strftime('%y-%m-%d'),
        'sortBy': 'publishedAt',
        'apiKey': api_key
    }
    try:
        logger.info(f'Выполняем запрос с ключевыми словами: {query}')
        response = requests.get(
            url=BASE_URL,
            params=params
        )

        news_data = response.json()
        if news_data.get('status') != 'ok':
            logger.info('Статей не нашлось')
            return []

        articles_list = news_data.get('articles', [])

        logger.info(f'Фильтруем новости по словам исключениям: {", ".join(exclude_words)}')
        articles_result = []
        for article in articles_list:
            content = f'{article.get("title")} {article.get("content")}'.lower()

            if any(word.lower() in content for word in exclude_words):
                continue

            articles_result.append(
                {
                    'title': article.get('title'),
                    'author': article.get('author'),
                    'description': article.get('content'),
                    'url': article.get('url')
                }
            )

        return articles_result
    except requests.RequestException as ex:
        logger.error(f'Произошла ошибка: {ex}')
        return []
    except Exception as ex:
        logger.error(f'Произошла ошибка: {ex}')
        return []