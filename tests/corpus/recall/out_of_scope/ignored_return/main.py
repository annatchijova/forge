def persist(client, record):
    client.save(record)
    return "ok"
