import os
import requests

QUICKCHART_BASE_URL = os.getenv("QUICKCHART_BASE_URL")

def generate_bar_chart(data_dict: dict, title: str = "Crypto Stats"):
    labels = list(data_dict.keys())
    values = list(data_dict.values())
    chart_config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": title,
                "data": values,
                "backgroundColor": "rgba(54, 162, 235, 0.6)"
            }]
        }
    }
    url = f"{QUICKCHART_BASE_URL}?c={requests.utils.quote(str(chart_config))}"
    return url