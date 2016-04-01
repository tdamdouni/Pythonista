def parse_requirements(requirements, ignore=('#', 'setuptools', '-r', '--')):
    """Read dependencies from file and strip off version numbers."""
    with open(requirements) as f:
        packages = []
        for line in f:
            line = line.strip()
            if any(line.startswith(prefix) for prefix in ignore):
                continue
            if '#egg=' in line:
                packages.append(line.split('#egg=')[1])
            else:
                packages.append(line.split('==')[0])
        return packages
