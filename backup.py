# remove empty lines and strip whitespace
        dockerfile = [line.strip() for line in dockerfile if line.strip()]

        # first line should be a FROM statement
        if not dockerfile[0].startswith("FROM"):
            print("The first line of the Dockerfile must be a FROM statement.")
            exit(1)

        # can't have staged builds, therefore only one CMD statement, at the very end
        cmd_count = 0
        for line in dockerfile:
            if any(line.strip().startswith(cmd) for cmd in ["CMD", "ENTRYPOINT"]):
                cmd_count += 1
        if cmd_count > 1:
            print("The Dockerfile must have only one CMD/ENTRYPOINT statement.")
            exit(1)

        if not any(
            dockerfile[-1].strip().startswith(cmd) for cmd in ["CMD", "ENTRYPOINT"]
        ):
            print("The last line of the Dockerfile must be a CMD/ENTRYPOINT statement.")
            exit(1)


        base_image_name = dockerfile[0].strip().split()[1]
        base_image_type = None
        base_image_version = None

        if base_image_name.startswith("python:"):
            base_image_type = "python"
            base_image_version = base_image_name.split(":")[1]
        else:
            print("Unsupported base image type.")
            exit(1)

        # survey the system for if the required base is present in system
        if base_image_type == "python":
            # check if the required python version is present in the system
            python_version = base_image_version.split("-")[0]
            if not os.system(f"python{python_version} --version"):
                print(f"Python {python_version} is present in the system.")
            else:
                print(
                    f"Python {python_version} is not present in the system. Please install it and try again."
                )
                exit(1)
        else:
            print("Unsupported base image type.")
            exit(1)