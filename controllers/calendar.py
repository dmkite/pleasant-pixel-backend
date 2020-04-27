from flask import jsonify, request


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
    return jsonify({'message': f'func called with {email}'})


def update_day(email, year, month, day):
    if year and month and day:
        print(year, month, day)
    else:
        return jsonify({
            'message': 'Incorrectly formatted date'
        }), 400
