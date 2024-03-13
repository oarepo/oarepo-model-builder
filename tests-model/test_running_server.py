from pprint import pprint

import requests
import yaml


def test_running_server():
    while True:
        data = requests.get(
            "https://127.0.0.1:5000/api/complex-model", verify=False  # NOSONAR
        ).json()
        if not data["hits"]["hits"]:
            break
        for hit in data["hits"]["hits"]:
            requests.delete(hit["links"]["self"], verify=False)  # NOSONAR

    assert data == {
        "hits": {"hits": [], "total": 0},
        "aggregations": {
            "metadata_d": {"buckets": [], "label": "metadata/d.label"},
            "metadata_dt": {"buckets": [], "label": "metadata/dt.label"},
            "metadata_ed": {"buckets": [], "label": "metadata/ed.label"},
            "metadata_edt": {"buckets": [], "label": "metadata/ed.label"},
            "metadata_f": {"buckets": [], "label": "metadata/f.label"},
            "metadata_i": {"buckets": [], "label": "metadata/i.label"},
            "metadata_kw": {"buckets": [], "label": "metadata/kw.label"},
            "metadata_t": {"buckets": [], "label": "metadata/t.label"},
        },
        "sortBy": "newest",
        "links": {
            "self": "https://127.0.0.1:5000/api/complex-model/?page=1&size=25&sort=newest"
        },
    }

    records = []
    with open("complex-model/data/sample_data.yaml") as f:
        sample_data = list(yaml.safe_load_all(f))
        for d in sample_data:
            resp = requests.post(
                "https://127.0.0.1:5000/api/complex-model",
                json=d,
                verify=False,  # NOSONAR
            )
            data = resp.json()
            assert (
                resp.status_code == 201
            ), f"Bad status code {resp.status_code} {data}, {d}"
            records.append(data)

    pprint(records)

    for r, d in zip(records, sample_data):
        record = requests.get(r["links"]["self"], verify=False).json()  # NOSONAR
        assert record["metadata"] == d["metadata"]

    record = requests.get(
        records[0]["links"]["self"],
        headers={
            "Accept-Language": "cs",
            "Accept": "application/vnd.inveniordm.v1+json",
        },
        verify=False,  # NOSONAR
    ).json()
    pprint(record)
    # czech locale and default locale differs, so just test it
    assert record["metadata"]["d"] != sample_data[0]["metadata"]["d"]
    assert record["metadata"]["dt"] != sample_data[0]["metadata"]["dt"]
