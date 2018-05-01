#!/usr/bin/python3
#
# Update stage-packages in manifest.yaml to ensure core gets
# the benefits from the new USN tracker.

import sys
import yaml


if __name__ == "__main__":
    root = sys.argv[1]

    with open(root+"/prime/snap/manifest.yaml") as fp:
        data = yaml.load(fp)
    # sync dpkg.list
    pkgs = []
    with open(root+"/prime/usr/share/snappy/dpkg.list") as fp:
        for line in fp.readlines():
            if not line.startswith("ii "):
                continue
            l = line.split()
            pkgs.append("%s=%s" % (l[1], l[2]))
    # update stage-packages
    data["parts"]["manifest"]["stage-packages"] = pkgs
    with open(root+"/prime/snap/manifest.yaml", "w") as fp:
        yaml.dump(data, fp)
