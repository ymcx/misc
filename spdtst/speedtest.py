from subprocess import CalledProcessError
import json
import subprocess


def run() -> dict | None:
    try:
        output = subprocess.run(
            args=["SpeedTest", "--output", "json"],
            capture_output=True,
            check=True,
        )
    except CalledProcessError:
        # Non-zero exit code
        return None

    result = json.loads(output.stdout)
    if result["_"] != "all ok":
        # SpeedTest returned an erroneus result
        print(">>> "+result)
        return None

    try:
        float(result["download"])
        float(result["upload"])
        int(result["ping"])
        int(result["jitter"])
    except ValueError:
        # For whatever reason the numerical values are non-numeric
        print(">>> "+result)
        return None

    return result
