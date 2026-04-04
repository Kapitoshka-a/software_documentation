from core.config import settings
from reader import JSONDataReader
from strategies import DataExporter, ConsoleStrategy, RedisStrategy, KafkaStrategy


def main():
    data = JSONDataReader.read(settings.EXPORTER_DATA_FILE)
    if not data:
        print("No data found.")
        return

    storage_type = settings.EXPORTER_STRATEGY

    if storage_type == "console":
        strategy = ConsoleStrategy()
    elif storage_type == "redis":
        strategy = RedisStrategy(host=settings.REDIS_HOST, port=settings.REDIS_PORT, namespace=settings.REDIS_NAMESPACE)
    elif storage_type == "kafka":
        strategy = KafkaStrategy(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS, topic=settings.KAFKA_TOPIC)
    else:
        print("Unknown storage type.")
        return

    exporter = DataExporter(strategy)
    exporter.export(data)


if __name__ == "__main__":
    main()