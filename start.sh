podman rm --force --all
pip freeze >requirements.txt
podman build . --tag "$1"
podman run -d -p 5000:5000 "$1"
