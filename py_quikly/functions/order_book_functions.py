"""
Order book functions for QUIK interaction
"""


from typing import Optional
from .base_functions import BaseFunctions
from ..data_structures import OrderBook


class OrderBookFunctions(BaseFunctions):
    """
    Функции для работы со стаканом котировок
    """

    async def subscribe(self, class_code: str, sec_code: str) -> bool:
        """
        Функция заказывает на сервер получение стакана по указанному классу и бумаге.

        Args:
            class_code: Код класса
            sec_code: Код инструмента

        Returns:
            True если подписка успешна
        """
        result = await self.call_function("Subscribe_Level_II_Quotes", class_code, sec_code)
        return bool(result['data']) if result else False


    async def unsubscribe(self, class_code: str, sec_code: str) -> bool:
        """
        Функция отменяет заказ на получение с сервера стакана по указанному классу и бумаге.

        Args:
            class_code: Код класса
            sec_code: Код инструмента

        Returns:
            True если отписка успешна
        """
        result = await self.call_function("Unsubscribe_Level_II_Quotes", class_code, sec_code)
        return bool(result['data']) if result else False


    async def is_subscribed(self, class_code: str, sec_code: str) -> bool:
        """
        Функция позволяет узнать, заказан ли с сервера стакан по указанному классу и бумаге.

        Args:
            class_code: Код класса
            sec_code: Код инструмента

        Returns:
            True если есть подписка
        """
        result = await self.call_function("IsSubscribed_Level_II_Quotes", class_code, sec_code)
        return bool(result['data']) if result else False


    async def get_quote_level2(self, class_code: str, sec_code: str) -> Optional[dict]:
        import pandas as pd
        
        response = await self.call_function("GetQuoteLevel2", class_code, sec_code)
        
        if not response or 'data' not in response or not response['data']:
            return None
        
        order_book = OrderBook.from_dict(response['data'])
        
        ask_df = pd.DataFrame([
            {'price': quote.price, 'quantity': quote.quantity} 
            for quote in getattr(order_book, 'offer', order_book.offer)
        ]).sort_values('price', ascending=True).iloc[::-1]
        
        bid_df = pd.DataFrame([
            {'price': quote.price, 'quantity': quote.quantity} 
            for quote in order_book.bid
        ]).sort_values('price', ascending=False)
        
        return {'ask': ask_df, 'bid': bid_df}
    
        # return OrderBook.from_dict(result['data']) if result['data'] else None

