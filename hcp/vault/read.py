#!/usr/bin/env python3

from logging import Logger

import hvac
from elastic.pipes.core import Pipe
from elastic.pipes.core.util import fatal
from typing_extensions import Annotated

from .common import update_url_token_from_env


@Pipe("elastic.pipes.hcp.vault.read")
def main(
    log: Logger,
    path: Annotated[
        str,
        Pipe.Config("path"),
        Pipe.Help("Vault path containing the source data"),
    ],
    vault: Annotated[
        dict,
        Pipe.State("vault", mutable=True),
        Pipe.Help("state node destination of the data"),
    ],
    url: Annotated[
        str,
        Pipe.Config("url"),
        Pipe.Help("URL of the Vault instance"),
        Pipe.Notes("default: from environment VAULT_ADDR"),
    ] = None,
    token: Annotated[
        str,
        Pipe.Config("token"),
        Pipe.Help("Vault API authentication token"),
        Pipe.Notes("default: from environment VAULT_TOKEN"),
    ] = None,
):
    """Read data from an HCP Vault instance."""

    log.info(f"path: {path}")
    url, token = update_url_token_from_env(url, token, log)

    vc = hvac.Client(url=url, token=token)
    if not vc.is_authenticated():
        fatal("vault could not authenticate")

    res = vc.read(path)
    if res is None:
        fatal(f"could not find Vault path: '{path}'")

    vault.clear()
    vault.update(res["data"])


if __name__ == "__main__":
    main()
