import matplotlib.pyplot as plt
import requests
import json

Key = ""
api = f"https://api.politicsandwar.com/graphql?api_key={Key}"


def update_values():
    request = """{alliances(first:50) {data {name, nations {score, num_cities}}, paginatorInfo{hasMorePages}}}"""
    payload = {
        "query": request
    }
    bob = 'unhappy'
    while bob == "unhappy":
        try:
            J = requests.post(api, json=payload).text
            response = json.loads(J)["data"]["alliances"]["data"]
            bob = "happy"
        except json.decoder.JSONDecodeError:
            pass
    _temp = [{y: (len(z), sum([a['score'] for a in z])/len(z).__round__(2), sum([a['num_cities'] for a in z])/len(z)) if y == 'nations' else z for y, z in x.items()} for x in response]
    _member_count = [y['nations'][0] for y in _temp]
    _avg_score = [y['nations'][1] for y in _temp]
    _avg_cities = [y['nations'][2] for y in _temp]
    _names = [y['name'] for y in _temp]
    return _member_count, _avg_score, _names, _avg_cities


def generate_plot(_names, axis_1, axis_2):
    _fig, ax = plt.subplots()
    ax.scatter(axis_1, axis_2)

    for i, name in enumerate(_names):
        ax.annotate(name, (axis_1[i], axis_2[i]))
    plt.xlabel("Member Quantity")
    plt.ylabel("Average Cities")
    return _fig


if __name__ == '__main__':
    member_count, avg_score, names, avg_cities = update_values()
    fig = generate_plot(names, member_count, avg_cities)
    # plt.yscale("log")
    plt.xscale("log")
    plt.show()
