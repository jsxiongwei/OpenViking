# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: AGPL-3.0

from openviking.resource.github_radar.gh_cli import GhCli, GhCliError


def test_local_timeout_is_retryable():
    assert GhCli._retryable(
        GhCliError("gh timed out after 120.0s: gh api repos/volcengine/OpenViking/issues")
    )


def test_rate_limited_403_is_retryable():
    assert GhCli._retryable(
        GhCliError("gh exited 1: HTTP 403: API rate limit exceeded for user")
    )


def test_plain_403_is_not_retryable():
    # Permission errors are permanent; retrying would just burn the attempt budget.
    assert not GhCli._retryable(
        GhCliError("gh exited 1: 403 You are not authorized to perform this action")
    )


def test_status_code_classification_is_unchanged():
    assert GhCli._retryable(GhCliError("gh exited 1: 429 too many requests"))
    assert GhCli._retryable(GhCliError("gh exited 1: 502 Bad Gateway"))
    assert not GhCli._retryable(GhCliError("gh exited 1: 401 Bad credentials"))
