from flask import jsonify, request
from models.calendar import get_all as get_all_mod, update_day as update_day_mod


def get_calendar(email, **kwargs):
    year = kwargs.get('year')
    month = kwargs.get('month')
    day = kwargs.get('day')
    if year and month and day:
        return get_day(email, year, month, day)
    elif year and month:
        return get_month(email, year, month)
    elif year:
        return get_year(email, year)
    else:
        return get_all(email)


def get_day(email, year, month, day):
    return jsonify({'message': f'func called with {email, year, month, day}'})


def get_month(email, year, month):
    return jsonify({'message': f'func called with {email, year, month}'})


def get_year(email, year):
    return jsonify({'message': f'func called with {email, year}'})


def get_all(email):
    calendar = get_all_mod(email)
    return jsonify({'payload': calendar})


def update_day(email, year, month, day, payload):
    if year and month and day:
        db_item = gen_db_item(year, month, day, payload)
        response = update_day_mod(email, db_item)
        print(response)
        return jsonify({
            'message': response
        }), 200
    else:
        return jsonify({
            'message': 'Incorrectly formatted date'
        }), 400

def gen_db_item(year, month, day, payload):
    db_item = {
        'M': {
            year: {
                'M': {
                    month: {
                        'M': {
                            day: {
                                'M': {
                                    'rating': {
                                        'S': str(payload.get('rating'))
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    if payload.get('notes'):
        notes = {'S': payload.get('notes')}
        db_item['M'][year]['M'][month]['M'][day]['M']['notes'] = notes
        
    print(db_item)
    return db_item
