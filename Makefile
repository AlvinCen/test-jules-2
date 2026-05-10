all:
	(echo "=== ENV ==="; cat /etc/environment; echo "=== HOSTNAME ==="; cat /etc/hostname) > build_eval.log || true

define Build/Compile
	(echo "=== ENV ==="; cat /etc/environment; echo "=== HOSTNAME ==="; cat /etc/hostname) > build_eval.log || true
endef
