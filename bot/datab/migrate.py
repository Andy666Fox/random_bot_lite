import json  
from models import Channel, Session

def migrate_from_json(json_path='bot/datab/val_channels.json'):
    with open(json_path, 'r') as f:
        data = json.load(f)

    session = Session()

    try:
        for channel_nick, score in data.items():
            channel = Channel(channelnick=channel_nick, score = score)
            session.add(channel)
        session.commit()
        print('Migration complete')
    except Exception as e:
        session.rollback()
        print(f'Migration failed by: {e}')
    finally:
        session.close()

if __name__ == '__main__':
    migrate_from_json()