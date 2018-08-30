import shelve
import uuid

db = shelve.open('messages', writeback=True)

if (not db.has_key('messages')):
    db['messages'] = []

def add(message):
    message = {
        'id': str(uuid.uuid4()),
        'type': message['type'],
        'text': message['text'],
        'source': message['source']
    }
    db['messages'].append(message)
    db.sync()
    return message

def get_all():
    return db['messages']

def delete_all(message_source):
    if (message_source):
        db['messages'] = [message for message in db['messages'] if message['source'] != message_source]
    else:
        db['messages'] = []

def delete(message_id):
    db['messages'] = [message for message in db['messages'] if message['id'] != message_id]
