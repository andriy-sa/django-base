def serialize(data):
    result = [];
    for item in data:

        object = {
            'id': item.id,
            'first_name': item.first_name,
            'last_name': item.last_name,
            'phone': item.phone,
            'address': item.address,
            'comments_count': item.comments__count,
        }
        last_comment = item.comments.first()
        if last_comment:
            object['last_comment'] = {
                'message': last_comment.message,
                'rate': last_comment.rate
            }
        result.append(object)

    return result