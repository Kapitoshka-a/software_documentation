from abc import ABC, abstractmethod
import redis
from kafka import KafkaProducer
import json


class StorageStrategy(ABC):
    @abstractmethod
    def write(self, data: list):
        pass


class ConsoleStrategy(StorageStrategy):
    def write(self, data: list):
        print("\n[CONSOLE] Exporting data to console...:")
        for row in data[:5]:
            print(row)


class RedisStrategy(StorageStrategy):
    def __init__(self, host, port):
        self.client = redis.Redis(host=host, port=port)

    def write(self, data: list):
        print(f"[REDIS] exporting {len(data)} rows to redis...")
        for row in data:
            self.client.rpush('salary_data', json.dumps(row))


class KafkaStrategy(StorageStrategy):
    def __init__(self, bootstrap_servers, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def write(self, data: list):
        print(f"[KAFKA] Exporting {len(data)} rows to kafka...")
        for row in data:
            self.producer.send(self.topic, row)
        self.producer.flush()


class DataExporter:
    def __init__(self, strategy: StorageStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: StorageStrategy):
        self._strategy = strategy

    def export(self, data: list):
        self._strategy.write(data)
