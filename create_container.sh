podman build -t django_acs_img .

podman pod create --name acs_pod \
	--publish 5432:5432 \
	--publish 8000:8000

podman run --name postgres_acs \
	--pod acs_pod \
	-e POSTGRES_USER=dev_user \
	-e POSTGRES_PASSWORD=secret \
	-e POSTGRES_DB=acs_db \
	-d postgres

podman run --name django_acs \
	--pod acs_pod \
	--volume $(pwd)/src:/app/src:Z \
	-it hpacm_img bash

