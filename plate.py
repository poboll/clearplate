"""Clear Plate automation.

The original project kept all behavior in this single script.  This version
keeps that simple shape while updating the API host and adding multi-token
support, supplement check-ins, and mutual likes.
"""

# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import datetime as dt
import os
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence

import requests


API_URL = "https://clearplate-api.guangpanxingdong.com/index.php"
DEFAULT_GROUP_ID = 6372
DEFAULT_LONGITUDE = 118.578482
DEFAULT_LATITUDE = 24.33405
DEFAULT_RUN_TIMES = ("07:01", "12:01", "18:01")
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 "
    "Mobile Safari/537.36 XWEB/1340043 MMWEBSDK/20250201 "
    "MicroMessenger/8.0.57.2820(0x28003933) WeChat/arm64 "
    "Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android"
)


class ClearPlateError(RuntimeError):
    """Raised when the Clear Plate API returns an unusable response."""


@dataclass
class ClearPlateConfig:
    token_file: Path = Path("tokens.txt")
    log_file: Path = Path("plate_log.txt")
    group_id: int = DEFAULT_GROUP_ID
    longitude: float = DEFAULT_LONGITUDE
    latitude: float = DEFAULT_LATITUDE
    supplement_days: int = 7
    request_delay_seconds: float = 1.0
    timeout_seconds: float = 15.0
    run_times: Sequence[str] = DEFAULT_RUN_TIMES
    location_jitter: float = 0.001


def log(message: str, level: str = "INFO", log_file: Optional[Path] = None) -> None:
    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{level} {timestamp}] {message}"
    print(line)

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def mask_token(token: str) -> str:
    token = token.strip()
    if len(token) <= 8:
        return "*" * len(token)
    return f"{token[:4]}...{token[-4:]}"


def load_tokens(token_file: Path) -> List[str]:
    if not token_file.exists():
        token_file.write_text(
            "# One x-token per line. Lines starting with # are ignored.\n",
            encoding="utf-8",
        )
        return []

    tokens: List[str] = []
    for line in read_text_with_fallback(token_file).splitlines():
        token = line.strip()
        if token and not token.startswith("#"):
            tokens.append(token)
    return tokens


def read_text_with_fallback(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def build_headers(token: str, version: str = "8.0.11") -> Dict[str, str]:
    return {
        "User-Agent": DEFAULT_USER_AGENT,
        "x-token": token,
        "x-version": version,
        "x-access-token": "",
        "x-form-id-list": "[]",
        "x-requested-with": "XMLHttpRequest",
        "x-oauth-type": "1",
        "x-app-platform": "wx",
        "charset": "utf-8",
    }


def api_request(
    session: requests.Session,
    method: str,
    route: str,
    token: str,
    config: ClearPlateConfig,
    data: Optional[Mapping[str, str]] = None,
) -> requests.Response:
    response = session.request(
        method,
        API_URL,
        params={"r": route},
        data=data,
        headers=build_headers(token),
        timeout=config.timeout_seconds,
    )
    response.raise_for_status()
    return response


def response_payload(response: requests.Response) -> Mapping[str, object]:
    try:
        payload = response.json()
    except ValueError:
        return {"raw": response.text}

    if isinstance(payload, Mapping):
        return payload
    return {"raw": payload}


def response_message(response: requests.Response) -> str:
    payload = response_payload(response)
    for key in ("msg", "message", "raw"):
        value = payload.get(key)
        if value:
            return str(value)
    return response.text


def jittered_location(latitude: float, longitude: float, jitter: float) -> str:
    if jitter <= 0:
        return f"{latitude:.6f},{longitude:.6f}"

    next_latitude = latitude + random.uniform(-jitter, jitter)
    next_longitude = longitude + random.uniform(-jitter, jitter)
    return f"{next_latitude:.6f},{next_longitude:.6f}"


def daka(token: str, config: ClearPlateConfig, session: requests.Session) -> requests.Response:
    payload = {
        "group_id": str(config.group_id),
        "path_url": "Photo",
        "location": jittered_location(config.latitude, config.longitude, config.location_jitter),
        "ai_type": "",
        "ai_weight": "",
    }
    return api_request(session, "POST", "/user-clear-plate/clear-plate", token, config, payload)


def buka(token: str, config: ClearPlateConfig, session: requests.Session) -> List[str]:
    results: List[str] = []
    today = dt.datetime.now().date()

    for offset in range(1, config.supplement_days + 1):
        supplement_date = today - dt.timedelta(days=offset)
        payload = {"sup_date": str(supplement_date), "is_watch_video": "1"}
        response = api_request(
            session,
            "POST",
            "/user-clear-plate/clear-plate-supplement",
            token,
            config,
            payload,
        )
        results.append(response_message(response))
        if config.request_delay_seconds:
            time.sleep(config.request_delay_seconds)

    return results


def load_uid(token: str, config: ClearPlateConfig, session: requests.Session) -> Optional[int]:
    response = api_request(session, "GET", "/user/user-info", token, config)
    payload = response_payload(response)
    data = payload.get("data")

    if not isinstance(data, Mapping):
        return None

    user_id = data.get("user_id")
    if user_id is None:
        return None
    return int(user_id)


def zan(
    token: str,
    user_ids: Iterable[int],
    config: ClearPlateConfig,
    session: requests.Session,
    own_user_id: Optional[int] = None,
) -> List[str]:
    results: List[str] = []
    for user_id in user_ids:
        if own_user_id is not None and user_id == own_user_id:
            continue

        response = api_request(
            session,
            "POST",
            "/user/like",
            token,
            config,
            {"user_id": str(user_id)},
        )
        results.append(f"{user_id}: {response_message(response)}")
        if config.request_delay_seconds:
            time.sleep(config.request_delay_seconds)
    return results


def run_once(config: ClearPlateConfig, session: Optional[requests.Session] = None) -> int:
    tokens = load_tokens(config.token_file)
    if not tokens:
        log(
            f"No token found. Fill {config.token_file} with one x-token per line, then run again.",
            log_file=config.log_file,
        )
        return 0

    close_session = session is None
    session = session or requests.Session()

    try:
        token_user_ids: Dict[str, int] = {}
        for token in tokens:
            try:
                user_id = load_uid(token, config, session)
            except Exception as exc:
                log(f"Failed to load user id for {mask_token(token)}: {exc}", "ERROR", config.log_file)
                continue

            if user_id is not None:
                token_user_ids[token] = user_id
                log(f"Loaded user id {user_id} for {mask_token(token)}", log_file=config.log_file)

        all_user_ids = sorted(set(token_user_ids.values()))

        for token in tokens:
            masked = mask_token(token)
            try:
                if all_user_ids:
                    like_results = zan(
                        token,
                        all_user_ids,
                        config,
                        session,
                        own_user_id=token_user_ids.get(token),
                    )
                    log(f"Likes for {masked}: {like_results}", log_file=config.log_file)

                checkin_response = daka(token, config, session)
                log(
                    f"Check-in for {masked}, group {config.group_id}: "
                    f"{response_message(checkin_response)}",
                    log_file=config.log_file,
                )

                supplement_results = buka(token, config, session)
                log(f"Supplements for {masked}: {supplement_results}", log_file=config.log_file)
            except Exception as exc:
                log(f"Task failed for {masked}: {exc}", "ERROR", config.log_file)

        log("Run finished.", log_file=config.log_file)
        return 0
    finally:
        if close_session:
            session.close()


def parse_run_times(value: str) -> Sequence[str]:
    times = tuple(part.strip() for part in value.split(",") if part.strip())
    for item in times:
        dt.datetime.strptime(item, "%H:%M")
    return times


def seconds_until_next_run(run_times: Sequence[str]) -> float:
    now = dt.datetime.now()
    candidates: List[dt.datetime] = []

    for run_time in run_times:
        hour, minute = [int(part) for part in run_time.split(":", 1)]
        candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if candidate <= now:
            candidate += dt.timedelta(days=1)
        candidates.append(candidate)

    return max(1.0, (min(candidates) - now).total_seconds())


def run_loop(config: ClearPlateConfig) -> int:
    log(f"Scheduled daily run times: {', '.join(config.run_times)}", log_file=config.log_file)
    while True:
        wait_seconds = seconds_until_next_run(config.run_times)
        next_run = dt.datetime.now() + dt.timedelta(seconds=wait_seconds)
        log(f"Next run at {next_run:%Y-%m-%d %H:%M:%S}", log_file=config.log_file)
        time.sleep(wait_seconds)
        run_once(config)


def env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default


def env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value else default


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Clear Plate auto check-in script")
    parser.add_argument("--token-file", default=os.getenv("CLEARPLATE_TOKEN_FILE", "tokens.txt"))
    parser.add_argument("--log-file", default=os.getenv("CLEARPLATE_LOG_FILE", "plate_log.txt"))
    parser.add_argument("--group-id", type=int, default=env_int("CLEARPLATE_GROUP_ID", DEFAULT_GROUP_ID))
    parser.add_argument("--longitude", type=float, default=env_float("CLEARPLATE_LONGITUDE", DEFAULT_LONGITUDE))
    parser.add_argument("--latitude", type=float, default=env_float("CLEARPLATE_LATITUDE", DEFAULT_LATITUDE))
    parser.add_argument("--supplement-days", type=int, default=env_int("CLEARPLATE_SUPPLEMENT_DAYS", 7))
    parser.add_argument("--request-delay", type=float, default=env_float("CLEARPLATE_REQUEST_DELAY", 1.0))
    parser.add_argument("--timeout", type=float, default=env_float("CLEARPLATE_TIMEOUT", 15.0))
    parser.add_argument("--location-jitter", type=float, default=env_float("CLEARPLATE_LOCATION_JITTER", 0.001))
    parser.add_argument(
        "--run-times",
        default=os.getenv("CLEARPLATE_RUN_TIMES", ",".join(DEFAULT_RUN_TIMES)),
        help="Comma-separated HH:MM times used with --loop.",
    )
    parser.add_argument("--loop", action="store_true", help="Run every day at --run-times.")
    return parser


def config_from_args(args: argparse.Namespace) -> ClearPlateConfig:
    return ClearPlateConfig(
        token_file=Path(args.token_file),
        log_file=Path(args.log_file),
        group_id=args.group_id,
        longitude=args.longitude,
        latitude=args.latitude,
        supplement_days=args.supplement_days,
        request_delay_seconds=args.request_delay,
        timeout_seconds=args.timeout,
        run_times=parse_run_times(args.run_times),
        location_jitter=args.location_jitter,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = config_from_args(args)

    if args.loop:
        return run_loop(config)
    return run_once(config)


if __name__ == "__main__":
    sys.exit(main())
