import os
import yaml

### DOCKER TO SYSTEMD CONVERTER


# check if docker-compose.yml exists
if not os.path.exists("docker-compose.yml"):
    print("docker-compose.yml not found, exiting...")
    exit(1)

with open("docker-compose.yml", "r") as f:
    compose: dict = yaml.safe_load(f)


# end of file read


name: str | None = compose.get("name")


for service_name, service in compose["services"].items():
    print(f"Processing service: {service_name}")

    def get_svc_value(key: str, default=None):
        if key in service:
            return service[key]
        else:
            return default

    # service logs
    attach: str | None = get_svc_value("attach", True)

    build = get_svc_value("build", None)

    if type(build) == str:
        context = build
        dockerfile = "Dockerfile"

    if type(build) == dict:
        context = build.get("context", ".")
        dockerfile = build.get("dockerfile", "Dockerfile")

        unsupported_keys = [
            "args",
            "additional_contexts",
            "cache_from",
            "cache_to",
            "dockerfile_inline",
            "entitlements",
            "extra_hosts",
            "isolation",
            "labels",
            "network",
            "no_cache",
            "platforms",
            "privileged",
            "provenance",
            "pull",
            "sbom",
            "secrets",
            "ssh",
            "shm_size",
            "tags",
            "target",
            "ulimits",
        ]

        for key in unsupported_keys:
            if key in build:
                print(
                    f"Service ({service_name}) has unsupported build key: ({key})"
                    "\nIgnoring the unsupported build key."
                )
