user_status = [
    {"id": 1, "name": "active"},
    {"id": 2, "name": "inactive"},
    {"id": 3, "name": "suspended"}
]

gender = [
    {"id": 1, "name": "male"},
    {"id": 2, "name": "female"},
    {"id": 3, "name": "other"}
]


def get_static_data():
    """
    This function returns static data created in this file
    :param:
    :return:
    """
    static_data = {
        "user_status": user_status,
        "gender": gender
    }
    return static_data
