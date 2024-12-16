def to_dict(instance):
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}
