import collections
import requests
import tqdm
from flags2_common import main, save_flag, HTTPStatus, Result

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1


def get_flag(base_url, cc):
    resp = requests.get(f"{base_url}/{cc.lower()}/{cc.lower()}.gif")
    if resp.status_code != 200:
        resp.raise_for_status()
    return resp.content


def download_one(cc, base_url, verbose=False):
    try:
        image = get_flag(base_url, cc)
    except requests.exceptions.HTTPError as exc:
        res = exc.response
        if res.status_code == 404:
            status = HTTPStatus.not_found
            msg = "not found"
        else:
            raise
    else:
        save_flag(image, cc.lower() + ".gif")
        status = HTTPStatus.ok
        msg = "OK"

    if verbose:
        print(cc, msg)
    return Result(status, cc)


def download_many(cc_list, base_url, verbose, max_req):
    counter = collections.Counter()
    cc_iter = sorted(cc_list)
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter)
    for cc in cc_iter:
        try:
            res = download_one(cc, base_url, verbose)
        except requests.exceptions.HTTPError as exc:
            error_msg = (
                f"HTTP error {exc.response.status_code} -- {exc.response.reason}"
            )
        except requests.exceptions.ConnectionError as exc:
            error_msg = "connection error"
        else:
            error_msg = ""
            status = res.status

        if error_msg:
            status = HTTPStatus.error
        counter[status] += 1

        if verbose and error_msg:
            print(f"*** Error for {cc}: {error_msg}")
    return counter


if __name__ == "__main__":
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
