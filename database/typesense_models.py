songs_schema = {
    "name": "songs",
    "fields": [
        {"name": "title", "type": "string"},
        {"name": "artist", "type": "string"},
        {"name": "lyrics", "type": "string"},
        {
            "name": "embedding",
            "type": "float[]",
            "embed": {
                "from": ["lyrics"],
                "model_config": {"model_name": "ts/all-MiniLM-L12-v2"},
            },
        },
    ],
}
